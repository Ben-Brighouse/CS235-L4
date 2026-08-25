"""
End-to-end tests for user favourites functionality.
Tests adding, removing, and viewing favourite tracks.
"""

import pytest


class TestUserFavourites:
    """
    End-to-end tests for user favourites feature.
    These tests are written following TDD and are expected to fail until
    the favourites functionality is implemented.
    """

    def test_add_track_to_favourites(self, client, authenticated_user_session, populated_repository):
        """
        Test adding a track to user favourites.
        
        Expected behavior:
        - POST /song/1/favourite should add track to user's favourites
        - On success: redirect to song page or return 200 with updated page
        - Favourite button should change appearance (e.g., filled heart)
        - Track should appear in user's favourites list
        
        Currently fails because favourite endpoint is not implemented.
        """
        response = authenticated_user_session.post('/song/1/favourite', 
                                                    follow_redirects=True)
        
        assert response.status_code == 200
        # Should show that track is now favourited
        assert (b'Unfavourite' in response.data or 
                b'favorited' in response.data.lower() or
                b'favourite' in response.data.lower())

    def test_view_user_favourites(self, client, authenticated_user_session, populated_repository):
        """
        Test viewing user's favourite tracks list.
        
        Expected behavior:
        - GET /favourites should display all tracks user has marked as favourite
        - Should show track title, artist, and genre
        - Should have option to remove from favourites
        - Should be empty initially or show previously added favourites
        
        Currently fails because /favourites endpoint is not implemented.
        """
        # First add some tracks to favourites
        authenticated_user_session.post('/song/1/favourite')
        authenticated_user_session.post('/song/2/favourite')
        
        response = authenticated_user_session.get('/favourites')
        
        assert response.status_code == 200
        assert b'Test Track' in response.data
        assert b'Another Track' in response.data
        assert b'Test Artist' in response.data

    def test_remove_track_from_favourites(self, client, authenticated_user_session, populated_repository):
        """
        Test removing a track from favourites.
        
        Expected behavior:
        - POST /song/1/unfavourite should remove track from favourites
        - Track should no longer appear in /favourites
        - Favourite button should return to unfilled state
        - User should be redirected to previous page or show updated page
        
        Currently fails because unfavourite endpoint is not implemented.
        """
        # First add to favourites
        authenticated_user_session.post('/song/1/favourite')
        
        # Then remove
        response = authenticated_user_session.post('/song/1/unfavourite',
                                                   follow_redirects=True)
        
        assert response.status_code == 200
        # Should show unfavourite button or confirmation
        assert (b'Favourite' in response.data or 
                b'Add to' in response.data)
        
        # Verify it's removed from favourites list
        response = authenticated_user_session.get('/favourites')
        assert b'Test Track' not in response.data or response.data.count(b'Test Track') == 0

    def test_favourites_persist_across_sessions(self, client, authenticated_user_session, populated_repository):
        """
        Test that favourites are saved and persist across sessions.
        
        Expected behavior:
        - Add track to favourites
        - Logout and login again
        - Favourites should still be there
        - Favourites should be associated with user_id
        
        Currently fails because favourites persistence is not implemented.
        """
        # Add to favourites
        authenticated_user_session.post('/song/1/favourite')
        
        # Logout
        authenticated_user_session.get('/logout')
        
        # Login again
        response = authenticated_user_session.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Check favourites are still there
        response = authenticated_user_session.get('/favourites')
        
        assert response.status_code == 200
        assert b'Test Track' in response.data
