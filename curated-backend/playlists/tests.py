from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Playlist, PlaylistItem
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class PlaylistManagementTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            is_active=True
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        
        # Set up test URLs and data
        self.playlist_list_create_url = reverse('playlist-list-create')
        self.playlist_data = {
            'name': 'Test Playlist',
            'description': 'Test Description'
        }
        self.video_data = {
            'video_id': 'test123',
            'title': 'Test Video',
            'thumbnail_url': 'http://example.com/thumb.jpg',
            'channel_title': 'Test Channel'
        }

    def test_create_playlist(self):
        response = self.client.post(self.playlist_list_create_url, self.playlist_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 1)
        self.assertEqual(Playlist.objects.first().name, 'Test Playlist')

    def test_list_playlists(self):
        # Create a playlist first
        Playlist.objects.create(user=self.user, **self.playlist_data)
        
        response = self.client.get(self.playlist_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_add_video_to_playlist(self):
        # Create a playlist first
        playlist = Playlist.objects.create(user=self.user, **self.playlist_data)
        add_video_url = reverse('playlist-add-item', kwargs={'playlist_pk': playlist.pk})
        
        response = self.client.post(add_video_url, self.video_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlaylistItem.objects.count(), 1)

    def test_reorder_playlist_items(self):
        playlist = Playlist.objects.create(user=self.user, **self.playlist_data)
        
        # Create multiple items
        items = []
        for i in range(3):
            video_data = self.video_data.copy()
            video_data['video_id'] = f'test{i}'
            video_data['title'] = f'Test Video {i}'
            items.append(PlaylistItem.objects.create(
                playlist=playlist,
                order=i+1,
                **video_data
            ))
        
        reorder_url = reverse('playlist-reorder-items', kwargs={'playlist_pk': playlist.pk})
        
        # Send all item IDs in the new desired order
        new_order = [items[2].id, items[0].id, items[1].id]  # Reorder: 3,1,2
        response = self.client.patch(reorder_url, 
            {'item_ids': new_order},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify new order
        items_after = PlaylistItem.objects.filter(playlist=playlist).order_by('order')
        self.assertEqual(items_after[0].id, items[2].id)  # First item should be original third
        self.assertEqual(items_after[1].id, items[0].id)  # Second item should be original first
        self.assertEqual(items_after[2].id, items[1].id)  # Third item should be original second

    def test_create_playlist_duplicate_name(self):
        # First playlist
        self.client.post(self.playlist_list_create_url, self.playlist_data)
        # Attempt to create second playlist with same name
        response = self.client.post(self.playlist_list_create_url, self.playlist_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_playlist_unauthenticated(self):
        self.client.credentials()  # Remove authentication
        response = self.client.post(self.playlist_list_create_url, self.playlist_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
