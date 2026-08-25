from music.domainmodel.track import Track
from music.adapters.repository import AbstractRepo


def get_tracks(repo: AbstractRepo) -> list[Track]:
    return repo.get_all_tracks()

def get_track_by_id(track_id: int, repo: AbstractRepo) -> Track:
    return repo.get_track(track_id)