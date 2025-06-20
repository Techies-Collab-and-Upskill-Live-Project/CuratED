from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .models import WatchedVideo, VideoProgress, VideoFeedback

class YouTubeSearchTests(APITestCase):
    def setUp(self):
        self.search_url = reverse('youtube_search')
        self.search_params = {'q': 'python tutorial'}
        self.mock_response = {
            'results': [
                {
                    'id': 'test123',
                    'title': 'Test Video',
                    'description': 'Test Description'
                }
            ]
        }

    @patch('api.youtube.fetch_videos_by_keyword')
    def test_search_success(self, mock_fetch):
        mock_fetch.return_value = self.mock_response
        response = self.client.get(self.search_url, self.search_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data)

class VideoProgressTests(APITestCase):
    def setUp(self):
        # Create test user
        User = get_user_model()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        self.client.force_authenticate(user=self.user)
        
        # Test data
        self.video_id = 'test123'
        self.progress_data = {
            'video_id': self.video_id,
            'current_time': 120.5,
            'duration': 300.0,
            'percentage_watched': 40.0
        }
        
        # URL for progress endpoint
        self.progress_url = reverse('video-progress', kwargs={'video_id': self.video_id})

    def test_create_progress(self):
        response = self.client.post(
            reverse('video-progress', kwargs={'video_id': self.video_id}),
            self.progress_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VideoProgress.objects.count(), 1)
        self.assertEqual(VideoProgress.objects.get().current_time, 120.5)

    def test_update_progress(self):
        # First create progress
        VideoProgress.objects.create(user=self.user, **self.progress_data)
        
        # Update progress
        update_data = {
            'current_time': 150.0,
            'percentage_watched': 50.0
        }
        response = self.client.patch(self.progress_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(VideoProgress.objects.get().current_time, 150.0)

    def test_get_progress(self):
        # Create progress
        VideoProgress.objects.create(user=self.user, **self.progress_data)
        
        # Get progress
        response = self.client.get(self.progress_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_time'], 120.5)

    def test_unauthorized_access(self):
        # Logout
        self.client.force_authenticate(user=None)
        response = self.client.get(self.progress_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class VideoFeedbackTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        self.client.force_authenticate(user=self.user)
        self.feedback_url = reverse('video-feedback-create')
        
    def test_create_feedback(self):
        # First create watched video
        watched = WatchedVideo.objects.create(
            user=self.user,
            video_id='test123',
            title='Test Video',
            published_at='2024-01-01T00:00:00Z'
        )
        
        feedback_data = {
            'video_id': 'test123',
            'rating': 5,
            'comment': 'Great video!'
        }
        response = self.client.post(self.feedback_url, feedback_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
