"""
End-to-end tests for track search functionality.
Tests search by title, artist, and genre.
"""

import pytest
from music.domainmodel.track import Track


class TestTrackSearch:
    """
    End-to-end tests for track search feature.
    These tests are written following TDD and are expected to fail until
    the search functionality is implemented.
    """

    def test_search_tracks_by_title(self, client, populated_repository):
        """
        Test searching for tracks by title.
        
        Expected behavior:
        - GET /search?query=Test should return tracks with 'Test' in the title
        - Response should be 200 OK
        - Response should contain track title and artist name
        
        Currently fails because /search endpoint is not implemented.
        """
        response = client.get('/search?query=Test')
        
        assert response.status_code == 200
        assert b'Test Track' in response.data
        assert b'Test Artist' in response.data

    def test_search_tracks_by_artist(self, client, populated_repository):
        """
        Test searching for tracks by artist name.
        
        Expected behavior:
        - GET /search?artist=Jazz%20Musician should return Jazz Classic track
        - Response should contain artist name and track title
        - Should match partial artist names
        
        Currently fails because artist search is not implemented.
        """
        response = client.get('/search?artist=Jazz%20Musician')
        
        assert response.status_code == 200
        assert b'Jazz Classic' in response.data
        assert b'Jazz Musician' in response.data

    def test_search_tracks_by_genre(self, client, populated_repository):
        """
        Test searching for tracks by genre.
        
        Expected behavior:
        - GET /search?genre=Electronic should return all Electronic genre tracks
        - Response should list 'Test Track' and 'Another Track'
        - Should not return Jazz tracks
        
        Currently fails because genre search is not implemented.
        """
        response = client.get('/search?genre=Electronic')
        
        assert response.status_code == 200
        assert b'Test Track' in response.data
        assert b'Another Track' in response.data
        assert b'Jazz Classic' not in response.data

    def test_search_no_results(self, client, populated_repository):
        """
        Test search that returns no results.
        
        Expected behavior:
        - GET /search?query=NonExistent should return 200 OK
        - Response should display a "No results found" message or empty list
        
        Currently fails because search endpoint is not implemented.
        """
        response = client.get('/search?query=NonExistent')
        
        assert response.status_code == 200
        # Should either show no results message or empty list
        assert (b'No results' in response.data or 
                b'found' not in response.data or
                response.data.count(b'<tr') <= 1)  # Only header row
