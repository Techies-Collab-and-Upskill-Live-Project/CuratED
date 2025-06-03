from django.urls import path
from .views import (
    PlaylistListCreateAPIView,
    PlaylistRetrieveUpdateDestroyAPIView,
    AddVideoToPlaylistAPIView,
    PlaylistItemDestroyAPIView,
    PlaylistReorderItemsAPIView
)

urlpatterns = [
    path('playlists/', PlaylistListCreateAPIView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', PlaylistRetrieveUpdateDestroyAPIView.as_view(), name='playlist-detail'), 
    path('playlists/<int:playlist_pk>/items/', AddVideoToPlaylistAPIView.as_view(), name='playlist-add-item'),
    path('playlists/<int:playlist_pk>/items/<int:item_pk>/', PlaylistItemDestroyAPIView.as_view(), name='playlist-remove-item'),
    path('playlists/<int:playlist_pk>/reorder-items/', PlaylistReorderItemsAPIView.as_view(), name='playlist-reorder-items'),
    path('playlists/progress/', PlaylistProgressAPIView.as_view(), name='playlist-progress'),

]

