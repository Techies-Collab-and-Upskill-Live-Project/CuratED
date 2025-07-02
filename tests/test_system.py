import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta
from unittest.mock import patch, MagicMock

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.verify_otp_url = reverse('verify-otp')
        self.resend_otp_url = reverse('resend-verification')
        self.password_reset_url = reverse('password-reset')
        self.password_reset_confirm_url = reverse('password-reset-confirm')
        self.change_password_url = reverse('password-change')
        
        # Test user data
        self.user_data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
    @patch('accounts.views.send_mail')
    def test_user_registration(self, mock_send_mail):
        """Test user registration flow"""
        # Test successful registration
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertIn('OTP sent', response.data['message'])
        
        # Verify email was sent
        self.assertTrue(mock_send_mail.called)
        
        # Test duplicate registration
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    @patch('accounts.views.send_mail')
    def test_otp_verification(self, mock_send_mail):
        """Test OTP verification flow"""
        # Register a user first
        self.client.post(self.register_url, self.user_data)
        
        # Get the user and their OTP
        user = User.objects.get(email=self.user_data['email'])
        otp = user.otp
        
        # Test valid OTP verification
        response = self.client.post(self.verify_otp_url, {
            'email': self.user_data['email'],
            'otp': otp
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify user is now active
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        
        # Test invalid OTP
        new_user_data = {
            'email': 'test2@example.com',
            'password': 'StrongPass123!',
        }
        self.client.post(self.register_url, new_user_data)
        
        response = self.client.post(self.verify_otp_url, {
            'email': new_user_data['email'],
            'otp': '0000'  # Wrong OTP
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch('accounts.views.send_mail')
    def test_resend_otp(self, mock_send_mail):
        """Test OTP resend functionality"""
        # Register a user first
        self.client.post(self.register_url, self.user_data)
        
        # Reset the mock to check only the resend email
        mock_send_mail.reset_mock()
        
        # Request OTP resend
        response = self.client.post(self.resend_otp_url, {
            'email': self.user_data['email']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify email was sent again
        self.assertTrue(mock_send_mail.called)
        
    def test_login(self):
        """Test user login flow"""
        # Register and verify a user first
        with patch('accounts.views.send_mail'):
            self.client.post(self.register_url, self.user_data)
            user = User.objects.get(email=self.user_data['email'])
            user.is_active = True
            user.save()
        
        # Test successful login
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # Test invalid credentials
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': 'WrongPassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    @patch('accounts.views.send_mail')
    def test_password_reset(self, mock_send_mail):
        """Test password reset flow"""
        # Create and activate a user
        user = User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            is_active=True
        )
        
        # Request password reset
        response = self.client.post(self.password_reset_url, {
            'email': self.user_data['email']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify email was sent
        self.assertTrue(mock_send_mail.called)
        
        # For the confirm step, we'd need the actual token and uid which would require mocking
        # that part of the implementation. This is a limitation of the test since we can't 
        # easily extract those values from the email that would be sent in a real scenario.

class PlaylistTests(TestCase):
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
    
    def test_create_playlist(self):
        """Test playlist creation"""
        response = self.client.post(self.playlists_url, self.playlist_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.playlist_data['name'])
        self.assertEqual(response.data['description'], self.playlist_data['description'])
    
    def test_list_playlists(self):
        """Test listing user playlists"""
        # Create some playlists first
        self.client.post(self.playlists_url, self.playlist_data)
        self.client.post(self.playlists_url, {
            'name': 'Another Playlist',
            'description': 'Another test playlist'
        })
        
        # List playlists
        response = self.client.get(self.playlists_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_add_video_to_playlist(self):
        """Test adding a video to a playlist"""
        # Create a playlist first
        playlist_response = self.client.post(self.playlists_url, self.playlist_data)
        playlist_id = playlist_response.data['id']
        
        # Add video to playlist
        video_data = {
            'video_id': 'test_video_id',
            'title': 'Test Video',
            'thumbnail_url': 'https://example.com/thumbnail.jpg',
            'channel_title': 'Test Channel'
        }
        response = self.client.post(
            reverse('playlist-items', kwargs={'pk': playlist_id}),
            video_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify video is in playlist
        playlist_response = self.client.get(
            reverse('playlist-detail', kwargs={'pk': playlist_id})
        )
        self.assertEqual(len(playlist_response.data['items']), 1)
        self.assertEqual(playlist_response.data['items'][0]['video_id'], video_data['video_id'])

class YouTubeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.search_url = reverse('youtube-search')
        
        # Create and authenticate a user
        self.user = User.objects.create_user(
            email='api_test@example.com',
            password='StrongPass123!',
            is_active=True
        )
        
        # Get auth token
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'api_test@example.com',
            'password': 'StrongPass123!'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    @patch('api.views.youtube_search')
    def test_search_videos(self, mock_youtube_search):
        """Test searching for videos"""
        # Mock the YouTube API response
        mock_results = [
            {
                'id': {'videoId': 'test_video_1'},
                'snippet': {
                    'title': 'Test Video 1',
                    'description': 'Test Description 1',
                    'thumbnails': {'default': {'url': 'https://example.com/thumb1.jpg'}},
                    'channelTitle': 'Test Channel 1',
                    'publishedAt': '2023-01-01T00:00:00Z'
                }
            },
            {
                'id': {'videoId': 'test_video_2'},
                'snippet': {
                    'title': 'Test Video 2',
                    'description': 'Test Description 2',
                    'thumbnails': {'default': {'url': 'https://example.com/thumb2.jpg'}},
                    'channelTitle': 'Test Channel 2',
                    'publishedAt': '2023-01-02T00:00:00Z'
                }
            }
        ]
        mock_youtube_search.return_value = mock_results
        
        # Search for videos
        response = self.client.get(f'{self.search_url}?q=test+query')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(mock_results))
    
    def test_mark_video_watched(self):
        """Test marking a video as watched"""
        # Mark a video as watched
        video_data = {
            'video_id': 'test_video_id',
            'title': 'Test Video',
            'thumbnail': 'https://example.com/thumbnail.jpg',
            'channel_title': 'Test Channel'
        }
        response = self.client.post(reverse('mark-watched'), video_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check watched videos list
        response = self.client.get(reverse('watched-videos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['video_id'], video_data['video_id'])
