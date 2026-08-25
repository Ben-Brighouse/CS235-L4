from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.album import Album


class Track:
    def __init__(self, track_id: int, track_title: str):
        if type(track_id) is not int or track_id < 0:
            raise ValueError("Track ID should be a non negative integer.")
        self.__track_id = track_id

        if type(track_title) is not str or track_title.strip() == '':
            raise ValueError("Track title should be a non-empty string.")
        self.__title = track_title.strip()

        self.__artist = None
        self.__album: Album | None = None
        self.__track_url: str | None = None
        # duration in seconds
        self.__track_duration: int | None = None
        self.__genres: list = []

        self.__album_title: str | None = None
        self.__cover_art: str | None = None
        self.__artist_name: str | None = None
        self.__genre: str | None = None

    @property
    def album_title(self) -> str:
        return self.__album_title

    @album_title.setter
    def album_title(self, album_title: str) -> None:
        self.__album_title = album_title

    @property
    def cover_art(self) -> str:
        return self.__cover_art

    @cover_art.setter
    def cover_art(self, cover_art: str) -> None:
        self.__cover_art = cover_art

    @property
    def artist_name(self) -> str:
        return self.__artist_name

    @artist_name.setter
    def artist_name(self, artist_name: str) -> None:
        self.__artist_name = artist_name

    @property
    def genre(self) -> str:
        return self.__genre

    @genre.setter
    def genre(self, genre: str) -> None:
        self.__genre = genre

    @property
    def track_id(self) -> int:
        return self.__track_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        if type(new_title) is not str or new_title.strip() == '':
            raise ValueError("Track title should be a non-empty string.")
        self.__title = new_title.strip()

    @property
    def artist(self) -> Artist:
        return self.__artist

    @artist.setter
    def artist(self, new_artist: Artist | None):
        if new_artist is None:
            self.__artist = None
        elif isinstance(new_artist, Artist):
            self.__artist = new_artist
        else:
            raise ValueError("artist must be an Artist instance or None.")

    @property
    def album(self) -> Album | None:
        return self.__album

    @album.setter
    def album(self, new_album: Album | None):
        if new_album is None:
            self.__album = None
        elif isinstance(new_album, Album):
            self.__album = new_album
        else:
            raise ValueError("album must be an Album instance or None.")

    @property
    def track_url(self) -> str | None:
        return self.__track_url

    @track_url.setter
    def track_url(self, new_track_url: str | None):
        if new_track_url is None:
            self.__track_url = None
        elif type(new_track_url) is str and new_track_url.strip() != '':
            self.__track_url = new_track_url.strip()
        else:
            raise ValueError("track_url must be a non-empty string or None.")

    @property
    def track_duration(self) -> int | None:
        return self.__track_duration

    @track_duration.setter
    def track_duration(self, new_duration: int | None):
        if new_duration is None:
            self.__track_duration = None
        elif type(new_duration) is int and new_duration >= 0:
            self.__track_duration = new_duration
        else:
            raise ValueError("track_duration must be a non-negative int or None.")

    @property
    def genres(self) -> list:
        return self.__genres

    def add_genre(self, new_genre):
        if not isinstance(new_genre, Genre) or new_genre in self.__genres:
            return
        self.__genres.append(new_genre)

    def remove_genre(self, genre):
        if not isinstance(genre, Genre) or genre not in self.__genres:
            return
        self.__genres.remove(genre)

    def __repr__(self):
        return f"<Track {self.title}, track id = {self.track_id}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.track_id == other.track_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.track_id < other.track_id

    def __hash__(self):
        return hash(self.track_id)

    @genre.setter
    def genre(self, value):
        self._genre = value
