from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from unittest.mock import patch, MagicMock
import uuid

User = get_user_model()

class AuthenticationTests(APITestCase):
    """Authentication-related tests"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.verify_otp_url = reverse('verify-otp')
        self.resend_otp_url = reverse('resend-verification')
        self.password_reset_url = reverse('password-reset-request')
        
        # Test user data
        self.user_data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    @patch('accounts.views.send_mail')
    def test_registration_and_verification(self, mock_send_mail):
        """Test full registration and verification flow"""
        # Test registration
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        
        # Verify user was created but inactive
        user = User.objects.get(email=self.user_data['email'])
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.otp)
        
        # Test OTP verification
        otp_response = self.client.post(self.verify_otp_url, {
            'email': self.user_data['email'],
            'otp': user.otp
        })
        self.assertEqual(otp_response.status_code, status.HTTP_200_OK)
        
        # Verify user is now active
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        
        # Test login
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

class PlaylistTests(APITestCase):
    """Playlist management tests"""
    
    def setUp(self):
        self.client = APIClient()
        self.playlists_url = reverse('playlist-list')
        
        # Create and authenticate a user
        self.user = User.objects.create_user(
            email='playlist_test@example.com',
            password='StrongPass123!',
            is_active=True
        )
        
        # Get auth token
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'playlist_test@example.com',
            'password': 'StrongPass123!'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Test playlist data
        self.playlist_data = {
            'name': 'Test Playlist',
            'description': 'A test playlist'
        }
    
    def test_create_and_list_playlists(self):
        """Test creating and listing playlists"""
        # Create a playlist
        response = self.client.post(self.playlists_url, self.playlist_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.playlist_data['name'])
        
        # Create another playlist
        second_playlist = {
            'name': 'Another Playlist',
            'description': 'Another test playlist'
        }
        self.client.post(self.playlists_url, second_playlist)
        
        # List playlists
        list_response = self.client.get(self.playlists_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 2)
    
    def test_add_video_to_playlist(self):
        """Test adding a video to a playlist"""
        # Create a playlist first
        playlist_response = self.client.post(self.playlists_url, self.playlist_data)
        playlist_id = playlist_response.data['id']
        
        # Add video with unique ID to avoid conflicts
        unique_video_id = f"test_video_{uuid.uuid4()}"
        video_data = {
            'video_id': unique_video_id,
            'title': 'Test Video',
            'thumbnail_url': 'https://example.com/thumbnail.jpg',
            'channel_title': 'Test Channel'
        }
        
        # Use direct URL since we confirmed this works
        response = self.client.post(
            f'/api/v1/playlists/{playlist_id}/items/',
            video_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify video is in playlist
        playlist_detail = self.client.get(f'/api/v1/playlists/{playlist_id}/')
        self.assertEqual(len(playlist_detail.data['items']), 1)
        self.assertEqual(playlist_detail.data['items'][0]['video_id'], unique_video_id)

# This test class is commented out because it depends on external YouTube API
# Uncomment and update as needed for the implementation
"""
class YouTubeAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.search_url = '/api/v1/search/'
        
        # Create and authenticate user
        self.user = User.objects.create_user(
            email='api_test@example.com',
            password='StrongPass123!',
            is_active=True
        )
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'api_test@example.com',
            'password': 'StrongPass123!'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    @patch('api.youtube.fetch_videos_by_keyword')
    def test_search_videos(self, mock_fetch):
        # Mock the API response
        mock_fetch.return_value = {
            'results': [
                {
                    'id': 'test_video_1',
                    'title': 'Test Video 1',
                    'description': 'Test Description 1'
                }
            ]
        }
        
        response = self.client.get(f'{self.search_url}?q=test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
"""
