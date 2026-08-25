import abc

from music.domainmodel.track import Track

repo_instance = None

class AbstractRepo(abc.ABC):
    @abc.abstractmethod
    def add_track(self, track: Track) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_track(self, track_id: int) -> Track:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_tracks(self) -> list[Track]:
        raise NotImplementedError()

