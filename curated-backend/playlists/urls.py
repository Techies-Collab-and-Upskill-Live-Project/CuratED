from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PlaylistListCreateAPIView,
    PlaylistRetrieveUpdateDestroyAPIView,
    AddVideoToPlaylistAPIView,
    PlaylistItemDestroyAPIView,
    PlaylistReorderItemsAPIView,
    PlaylistViewSet
)

router = DefaultRouter()
router.register('playlists', PlaylistViewSet, basename='playlist')

urlpatterns = router.urls

urlpatterns += [
    path('playlists/', PlaylistListCreateAPIView.as_view(), name='playlist-list-create'),
    path('playlists/<uuid:pk>/', PlaylistRetrieveUpdateDestroyAPIView.as_view(), name='playlist-detail'), 
    path('playlists/<uuid:playlist_pk>/items/', AddVideoToPlaylistAPIView.as_view(), name='playlist-add-item'),
    path('playlists/<uuid:playlist_pk>/items/<int:item_pk>/', PlaylistItemDestroyAPIView.as_view(), name='playlist-remove-item'),
    path('playlists/<uuid:playlist_pk>/reorder-items/', PlaylistReorderItemsAPIView.as_view(), name='playlist-reorder-items'),
]
