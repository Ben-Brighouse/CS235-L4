# AGENTS.md: Music Library Application Guide

## Architecture Overview

This is a **Flask-based music library application** built with a layered architecture (Domain Model, Adapters, UI):

- **Domain Model** (`music/domainmodel/`): Core business objects (Track, Artist, User, Genre, Album, Review, Favourite) with strict input validation and ID-based equality/hashing
- **Adapters** (`music/adapters/`): Repository pattern for data access; `MemoryRepo` stores tracks in a dict indexed by track_id
- **UI Layer** (`music/home/`, `music/tracks/`): Flask blueprints serving HTML templates; `services.py` bridges controllers and repository
- **Data Loading**: `repository_populate.py` seeds sample tracks on app startup; `csvdatareader.py` reads from FMA dataset CSVs

## Critical Domain Model Patterns

### Validation & Immutability
- **Constructor validation required**: All domain classes validate inputs. Use `type(x) is <type>` checks, not `isinstance()`, for strict type enforcement
- **Immutable IDs**: Track/Artist/User IDs are read-only properties after construction; never modify
- **Private attributes**: All data uses double-underscore (e.g., `self.__track_id`) to enforce encapsulation
- **Setters reject invalid state silently**: e.g., `add_genre()` returns without error if genre already exists

### Equality, Sorting, Hashing
All domain objects override `__eq__`, `__lt__`, and `__hash__` based on **ID only**, not name/properties:
```python
# Track equality is based on track_id
track1 = Track(1, "Song A")
track2 = Track(1, "Song B")
assert track1 == track2  # Same ID = equal, despite different titles
```
This enables domain objects to be sorted, used in sets, and stored in repository dicts.

### Optional vs. Required
- **Optional properties** (e.g., `track.artist`, `track.album`): Setters accept `None`
- **Required properties** (e.g., `track.title`): Setters raise `ValueError` for invalid/empty values
- Check test cases in `tests/unit/test_domainmodel.py` for exact validation rules per class

## Repository Pattern & Data Access

- **Abstract Interface** (`repository.py`): Defines `AbstractRepo` with methods `add_track()`, `get_track(id)`, `get_all_tracks()`
- **Memory Implementation** (`memory_repository.py`): Stores tracks in `self._tracks: dict[int, Track]`
- **Global Instance** (`repo.repo_instance`): Set at app startup in `music/__init__.py`; imported via `import music.adapters.repository as repo` and accessed as `repo.repo_instance`

When adding new repository methods:
1. Add abstract method to `AbstractRepo`
2. Implement in `MemoryRepo`
3. Import and call via `repo.repo_instance` in service/blueprint

## Flask Structure & Blueprints

- **App Factory** (`music/__init__.py`): `create_app()` initializes Flask, registers blueprints, populates repository
- **Blueprints** (`home.py`, `tracks.py`): Define routes; import services for business logic
- **Services** (`services.py`): Thin layer between blueprints and repository—take repo as argument, call repo methods
- **Entry Point** (`wsgi.py`): `from music import create_app` and instantiate

Example flow: Route → Service (uses `AbstractRepo`) → Repository implementation

## Testing Patterns

- **Unit tests in `tests/unit/test_domainmodel.py`**: Test each domain class in isolation; constructor validation, property setters, equality/sorting, collections
- **CSV reader tests**: Verify data loads from FMA CSVs (2000 tracks, 263 artists, 427 albums, 60 genres in real dataset)
- **Run tests**: `python -m pytest tests` or via PyCharm test runner
- **No mocking**: Tests use real domain objects; MemoryRepo is the only mock needed for repo tests

## Data Pipeline

1. **CSV files** in `music/adapters/data/` are read by `CSVDataReader`
2. `repository_populate.py` creates Track objects with sample data, setting title, artist_name, album_title, duration, cover_art, genre
3. Tracks are added to repository on startup
4. Web UI retrieves tracks via `services.get_tracks(repo.repo_instance)` → displays in `browse.html`

## Common Tasks

**Add a new domain property to Track:**
1. Add private attribute in `__init__`
2. Add `@property` getter
3. Add `@<property>.setter` with validation (raise `ValueError` for invalid input)
4. Add test case to `TestTrack` in `test_domainmodel.py`

**Add a new repository method:**
1. Declare abstract method in `AbstractRepo`
2. Implement in `MemoryRepo`
3. Call via `repo.repo_instance.<method>()` in services/blueprints

**Add a new Flask route:**
1. Add route in blueprint (e.g., `music/tracks/tracks.py`)
2. Call service function to retrieve data
3. Pass data to template via `render_template('template.html', data=...)`

## Development Workflow

- **Virtual environment**: `python3 -m venv venv && source venv/bin/activate` (macOS) or `venv\Scripts\activate` (Windows)
- **Install deps**: `pip install -r requirements.txt` (Flask 3.0.3, Werkzeug 3.1.3, pytest)
- **Run app**: `flask run` from project root (uses `wsgi.py` entry point)
- **Run tests**: `python -m pytest tests` from project root
- **Environment config**: `.env` sets `FLASK_APP=wsgi.py`, `FLASK_ENV=development`, `SECRET_KEY`, etc.

## Key Files to Know

- `music/domainmodel/track.py`, `artist.py`, `user.py` — Core domain logic
- `music/adapters/memory_repository.py` — Data storage implementation
- `music/adapters/repository_populate.py` — Sample data seeding
- `music/tracks/services.py` — Business logic bridge
- `tests/unit/test_domainmodel.py` — Validation rules and test patterns
