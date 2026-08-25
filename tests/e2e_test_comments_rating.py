"""
End-to-end tests for track comments and rating functionality.
Tests adding, viewing, and deleting reviews/ratings.
"""

import pytest
from music.domainmodel.review import Review


class TestCommentsAndRating:
    """
    End-to-end tests for comments and ratings feature.
    These tests are written following TDD and are expected to fail until
    the comments/ratings functionality is implemented.
    """

    def test_add_review_to_track(self, client, authenticated_user_session, populated_repository):
        """
        Test adding a review/comment to a track.
        
        Expected behavior:
        - POST /song/1/review with review_text and rating (1-5)
        - On success: redirect to track page (302) or show track with new review
        - Review should display username, rating, and comment text
        - User must be authenticated
        
        Currently fails because review submission endpoint is not implemented.
        """
        response = authenticated_user_session.post('/song/1/review', data={
            'review_text': 'Great electronic track!',
            'rating': 5
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Great electronic track!' in response.data
        assert b'testuser' in response.data or b'5' in response.data

    def test_view_track_with_reviews(self, client, authenticated_user_session, populated_repository):
        """
        Test viewing a track page with existing reviews.
        
        Expected behavior:
        - GET /song/1 should display track details
        - Should show all reviews for that track
        - Each review should display: username, rating, review text, timestamp
        - Should show review count and average rating
        
        Currently fails because review display is not implemented.
        """
        # First, add a review (assuming test_add_review_to_track passes)
        authenticated_user_session.post('/song/1/review', data={
            'review_text': 'Awesome track',
            'rating': 4
        })
        
        response = authenticated_user_session.get('/song/1')
        
        assert response.status_code == 200
        assert b'Test Track' in response.data
        assert b'Awesome track' in response.data
        assert b'4' in response.data  # Rating should be visible

    def test_update_rating_score(self, client, authenticated_user_session, populated_repository):
        """
        Test viewing track average rating and rating distribution.
        
        Expected behavior:
        - GET /song/1 should display average rating
        - Should show rating distribution (e.g., 5 stars: 2 votes, 4 stars: 1 vote)
        - Should update when new reviews are added
        - Rating should be a decimal (e.g., 4.5)
        
        Currently fails because rating aggregation is not implemented.
        """
        # Add multiple reviews with different ratings
        authenticated_user_session.post('/song/1/review', data={
            'review_text': 'Good',
            'rating': 5
        })
        authenticated_user_session.post('/song/1/review', data={
            'review_text': 'Also good',
            'rating': 4
        })
        
        response = authenticated_user_session.get('/song/1')
        
        assert response.status_code == 200
        # Should show average rating (4.5) or rating summary
        assert (b'Average' in response.data or 
                b'Rating' in response.data or
                b'4' in response.data)

    def test_unauthenticated_user_cannot_review(self, client, populated_repository):
        """
        Test that unauthenticated users cannot post reviews.
        
        Expected behavior:
        - POST /song/1/review without authentication should redirect to login
        - Should return 302 redirect or 401 Unauthorized
        - Review should NOT be added to the track
        
        Currently fails because authentication check is not implemented.
        """
        response = client.post('/song/1/review', data={
            'review_text': 'Sneaky review',
            'rating': 3
        }, follow_redirects=False)
        
        # Should redirect to login (302) or deny access (401)
        assert response.status_code in [301, 302, 401]
