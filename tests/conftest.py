"""
Pytest configuration and fixtures for end-to-end testing.
Contains fixtures for Flask app, test client, and domain model objects.
"""

import pytest
import os
from music import create_app
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.album import Album
from music.adapters.repository import AbstractRepo
import music.adapters.repository as repo


@pytest.fixture
def app():
    """
    Create and configure a test Flask application.
    Uses testing configuration to disable CSRF protection and enable testing mode.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask application.
    Allows making HTTP requests to the app without running a live server.
    """
    return app.test_client()


@pytest.fixture
def app_context(app):
    """
    Create an application context for accessing Flask globals and teardown functions.
    """
    with app.app_context():
        yield app


@pytest.fixture
def test_user():
    """
    Create a test User object with valid credentials.
    User ID: 1, Username: testuser, Password: password123
    """
    return User(1, 'testuser', 'password123')


@pytest.fixture
def test_user_2():
    """
    Create a second test User object for comparison/multi-user scenarios.
    User ID: 2, Username: reviewuser, Password: reviewer456
    """
    return User(2, 'reviewuser', 'reviewer456')


@pytest.fixture
def test_artist():
    """
    Create a test Artist object.
    Artist ID: 1, Name: Test Artist
    """
    return Artist(1, 'Test Artist')


@pytest.fixture
def test_genre():
    """
    Create a test Genre object.
    Genre ID: 1, Name: Electronic
    """
    return Genre(1, 'Electronic')


@pytest.fixture
def test_album():
    """
    Create a test Album object.
    Album ID: 1, Name: Test Album, Artist: Test Artist
    """
    album = Album(1, 'Test Album')
    return album


@pytest.fixture
def test_track(test_artist, test_genre, test_album):
    """
    Create a test Track object with artist, genre, and album.
    Track ID: 1, Title: Test Track
    Pre-configured with artist, genre, and album for realistic testing.
    """
    track = Track(1, 'Test Track')
    track.artist = test_artist
    track.add_genre(test_genre)
    track.album = test_album
    track.track_duration = 240
    track.track_url = 'https://example.com/track/1'
    track.cover_art = 'test_cover.jpg'
    return track


@pytest.fixture
def test_track_2(test_artist, test_genre):
    """
    Create a second test Track object for search/filtering scenarios.
    Track ID: 2, Title: Another Track
    """
    track = Track(2, 'Another Track')
    track.artist = test_artist
    track.add_genre(test_genre)
    track.track_duration = 180
    return track


@pytest.fixture
def test_track_3():
    """
    Create a third test Track object with different artist/genre for diverse testing.
    Track ID: 3, Title: Jazz Classic
    """
    artist = Artist(2, 'Jazz Musician')
    genre = Genre(2, 'Jazz')
    track = Track(3, 'Jazz Classic')
    track.artist = artist
    track.add_genre(genre)
    track.track_duration = 300
    return track


@pytest.fixture
def populated_repository(app_context, test_track, test_track_2, test_track_3):
    """
    Populate the test repository with sample tracks.
    Returns the repository instance from the app context.
    Used for end-to-end tests that require multiple tracks for search/filtering.
    """
    # Access the global repo instance
    repo_instance = repo.repo_instance
    
    # Clear any existing tracks (in case of test isolation)
    if hasattr(repo_instance, '_tracks'):
        repo_instance._tracks.clear()
    
    # Add test tracks
    repo_instance.add_track(test_track)
    repo_instance.add_track(test_track_2)
    repo_instance.add_track(test_track_3)
    
    return repo_instance


@pytest.fixture
def authenticated_user_session(client, test_user):
    """
    Create an authenticated user session in the test client.
    Simulates a logged-in user by setting session data.
    Note: Requires authentication endpoints to be implemented.
    """
    with client.session_transaction() as sess:
        sess['user_id'] = test_user.user_id
        sess['user_name'] = test_user.user_name
    return client
