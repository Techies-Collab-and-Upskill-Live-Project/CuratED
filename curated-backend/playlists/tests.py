from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
from .models import Playlist

class PlaylistTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        self.client.force_authenticate(user=self.user)
        
        self.playlist_data = {
            'name': 'Test Playlist',
            'description': 'Test Description'
        }

    def test_create_playlist(self):
        url = reverse('playlist-list')
        response = self.client.post(url, self.playlist_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertEqual(Playlist.objects.get().name, 'Test Playlist')

    def test_share_playlist(self):
        playlist = Playlist.objects.create(
            user=self.user,
            name='Test Playlist',
            description='Test Description'
        )
        # Use correct URL pattern
        url = f'/api/v1/playlists/{str(playlist.id)}/share/'  # Convert UUID to string
        response = self.client.post(url, {'email': 'share@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {'email': self.other_user.email}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            playlist.shared_with.filter(id=self.other_user.id).exists()
        )

    # ...more test methods...
