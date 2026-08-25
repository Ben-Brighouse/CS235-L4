"""
End-to-end tests for user authentication functionality.
Tests user registration, login, and session management.
"""

import pytest
from music.domainmodel.user import User


class TestUserAuthentication:
    """
    End-to-end tests for user authentication.
    These tests are written following TDD and are expected to fail until
    the authentication functionality is implemented.
    """

    def test_user_registration(self, client):
        """
        Test new user registration.
        
        Expected behavior:
        - POST /register with username, password, password_confirm
        - On success: redirect to login page or home with 302/200 status
        - Username should be unique (lowercase stored)
        - Password must be at least 7 characters
        - Session should NOT be set yet (user needs to log in)
        
        Currently fails because /register endpoint is not implemented.
        """
        response = client.post('/register', data={
            'username': 'newuser',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should show login page or success message
        assert (b'login' in response.data.lower() or 
                b'registered' in response.data.lower())

    def test_user_login(self, client, test_user):
        """
        Test user login with valid credentials.
        
        Expected behavior:
        - POST /login with username and password
        - On success: redirect to home page (302) with session set
        - Session should contain user_id and user_name
        - User can access protected pages after login
        
        Currently fails because /login endpoint is not implemented.
        """
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to home or show welcome message
        assert b'testuser' in response.data or b'Home' in response.data
        
        # Check session was set
        with client.session_transaction() as sess:
            assert 'user_id' in sess
            assert sess['user_name'] == 'testuser'

    def test_user_login_invalid_password(self, client, test_user):
        """
        Test login with incorrect password.
        
        Expected behavior:
        - POST /login with wrong password should fail
        - Response should be 200 with error message
        - Session should NOT be set
        - User should remain on login page
        
        Currently fails because login validation is not implemented.
        """
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert (b'error' in response.data.lower() or 
                b'invalid' in response.data.lower())
        
        # Session should not be set
        with client.session_transaction() as sess:
            assert 'user_id' not in sess

    def test_user_logout(self, client, authenticated_user_session):
        """
        Test user logout.
        
        Expected behavior:
        - GET /logout should clear session
        - Should redirect to home page (302) or login
        - Session should be empty after logout
        - User should not have access to protected pages
        
        Currently fails because /logout endpoint is not implemented.
        """
        # Verify user is logged in first
        with client.session_transaction() as sess:
            assert sess.get('user_id') == 1
        
        response = client.get('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        
        # Session should be cleared
        with client.session_transaction() as sess:
            assert 'user_id' not in sess
            assert 'user_name' not in sess
