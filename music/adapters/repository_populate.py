from music.adapters.repository import AbstractRepo
from music.domainmodel.track import Track

def populate_repo(repo: AbstractRepo):
    sample_tracks = [(1, "Kilt", "Kettama", "Buckland Bridge", 287, "Bucklyn Bridge - Single.jpg", "House"),
                     (2, "Feeling Emotions", "Kettama", "Fallen Angel", 216, "Fallen Angel.jpg", "House"),
                     (3, "Stay With Me", "X-Club", "Stay With Me - EP", 227, "Stay With Me - EP.jpg", "House"),
                     (4, "Good Lies", "Overmono", "Good Lies", 223, "Good Lies.jpg", "House"),
                     (5, "Love Reigns", "Mall Grab", "What I Breathe", 294, "What I Breathe (Deluxe).jpg", "House"),
                     (6, "A Fresh Energy - Single", "Gaskin", "A Fresh Energy", 250, "A Fresh Energy - Single.jpg","House")]

    for track_id, title, artist, album, duration, cover_art, genre in sample_tracks:
        track = Track(track_id, title)
        track.track_duration = duration
        track.genre = genre
        track.artist_name = artist
        track.album_title = album
        track.cover_art = cover_art
        repo.add_track(track)
