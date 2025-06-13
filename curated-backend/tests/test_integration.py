from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

class IntegrationTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'SecurePass123!'
        }
        
    def test_complete_user_journey(self):
        # 1. Register
        register_response = self.client.post(
            reverse('register'),
            self.user_data
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        # 2. Verify Email
        user = self.User.objects.get(email=self.user_data['email'])
        verify_response = self.client.post(
            reverse('verify-otp'),
            {'email': self.user_data['email'], 'otp': user.otp}
        )
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        
        # 3. Login
        login_response = self.client.post(
            reverse('login'),
            self.user_data
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access']
        
        # 4. Search Videos
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        search_response = self.client.get(
            reverse('youtube_search'),
            {'q': 'python tutorial'}
        )
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        
        # 5. Create Playlist
        video_id = search_response.data['results'][0]['id']
        playlist_response = self.client.post(
            reverse('playlist-list'),
            {
                'name': 'Python Learning',
                'description': 'My Python tutorials'
            }
        )
        self.assertEqual(playlist_response.status_code, status.HTTP_201_CREATED)
        
        # 6. Add to Playlist
        playlist_id = playlist_response.data['id']
        add_video_response = self.client.post(
            reverse('playlist-items', kwargs={'pk': playlist_id}),
            {'video_id': video_id}
        )
        self.assertEqual(add_video_response.status_code, status.HTTP_201_CREATED)

    # ...more integration test methods...
