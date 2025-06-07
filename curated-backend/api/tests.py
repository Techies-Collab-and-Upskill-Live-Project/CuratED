from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import WatchedVideo
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class YouTubeSearchTests(APITestCase):
    def setUp(self):
        self.search_url = reverse('youtube_search')
        self.mock_search_response = {
            'items': [{
                'id': {'videoId': 'test123'},
                'snippet': {
                    'title': 'Test Video',
                    'description': 'Test Description',
                    'thumbnails': {'high': {'url': 'http://example.com/thumb.jpg'}},
                    'channelTitle': 'Test Channel',
                    'publishedAt': '2024-01-01T00:00:00Z'
                }
            }]
        }
        self.mock_details_response = {
            'items': [{
                'id': 'test123',
                'statistics': {
                    'likeCount': '1500',
                    'commentCount': '150'
                },
                'contentDetails': {
                    'duration': 'PT15M'
                }
            }]
        }

    @patch('api.youtube.requests.get')
    def test_search_success(self, mock_get):
        # Configure mock to return different responses for search and details
        def mock_response(url, params):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            
            if 'search' in url:
                mock_resp.json.return_value = self.mock_search_response
            elif 'videos' in url:
                mock_resp.json.return_value = self.mock_details_response
            
            mock_resp.url = url
            return mock_resp
            
        mock_get.side_effect = mock_response
        
        response = self.client.get(f"{self.search_url}?q=python tutorial")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_search_without_query(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class WatchedVideoTests(APITestCase):
    def setUp(self):
        # Create test user and authenticate
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        
        # Set up test URLs and data
        self.mark_watched_url = reverse('mark_video_watched')
        self.watched_list_url = reverse('watched-videos-list')
        
        self.video_data = {
            'video_id': 'test123',
            'title': 'Test Video',
            'description': 'Test Description',
            'thumbnail': 'http://example.com/thumb.jpg',
            'channel_title': 'Test Channel',
            'published_at': '2024-01-01T00:00:00Z'
        }

    def test_mark_video_watched(self):
        response = self.client.post(self.mark_watched_url, self.video_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(WatchedVideo.objects.filter(video_id='test123').exists())

    def test_list_watched_videos(self):
        # Create a watched video
        WatchedVideo.objects.create(user=self.user, **self.video_data)
        
        response = self.client.get(self.watched_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
