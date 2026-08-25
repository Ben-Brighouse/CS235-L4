from music.adapters.repository import AbstractRepo
from music.domainmodel.track import Track

class MemoryRepo(AbstractRepo):
    def __init__(self):
        self._tracks: dict[int, Track] = {}

    def add_track(self, track: Track) -> None:
        self._tracks[track.track_id] = track

    def get_track(self, track_id: int) -> Track:
        return self._tracks[track_id]

    def get_all_tracks(self) -> list[Track]:
        return [self._tracks[key] for key in self._tracks.keys()]