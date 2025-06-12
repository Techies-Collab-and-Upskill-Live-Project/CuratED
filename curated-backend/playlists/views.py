from rest_framework import generics, status, serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Playlist, PlaylistItem
from .serializers import (
    PlaylistSerializer,
    PlaylistCreateSerializer,
    PlaylistItemSerializer,
    PlaylistItemCreateSerializer,
    PlaylistItemReorderSerializer
)
from django.shortcuts import get_object_or_404
from django.db import transaction

class PlaylistListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PlaylistCreateSerializer
        return PlaylistSerializer

    def get_queryset(self):
        # Fix: Avoid filtering by user if this is a schema (Swagger) generation request
        if getattr(self, 'swagger_fake_view', False):
            return Playlist.objects.none()
        return Playlist.objects.filter(user=self.request.user).prefetch_related('items')

    def perform_create(self, serializer):
        serializer.save() # The user is passed in the serializer context or handled in the serializer's create method.

class PlaylistRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PlaylistCreateSerializer # Reusing PlaylistCreateSerializer for updates.
        return PlaylistSerializer # Using PlaylistSerializer for GET requests.

    def get_queryset(self):
        # Fix: Avoid filtering by user if this is a schema (Swagger) generation request
        if getattr(self, 'swagger_fake_view', False):
            return Playlist.objects.none()
        return Playlist.objects.filter(user=self.request.user).prefetch_related('items')

    def get_object(self):
        # Ensures that users can only retrieve/update/delete their own playlists.
        playlist = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'], user=self.request.user)
        return playlist

class AddVideoToPlaylistAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistItemCreateSerializer

    def perform_create(self, serializer):
        playlist_pk = self.kwargs.get('playlist_pk')
        playlist = get_object_or_404(Playlist, pk=playlist_pk, user=self.request.user)

        # Check if the video already exists in the playlist.
        video_id = serializer.validated_data.get('video_id')
        if PlaylistItem.objects.filter(playlist=playlist, video_id=video_id).exists():
            # Prevents duplicate videos in a playlist by raising a validation error.
            # Alternative approaches could include returning the existing item or a specific message.
            raise serializers.ValidationError({"video_id": "This video already exists in this playlist."})

        # Determine the order for the new item.
        last_item = playlist.items.order_by('-order').first()
        order = (last_item.order + 1) if last_item else 1
        
        serializer.save(playlist=playlist, order=order)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            # Returns the full playlist item details upon successful creation.
            # This involves serializing the created instance with PlaylistItemSerializer.
            created_item_serializer = PlaylistItemSerializer(serializer.instance)
            headers = self.get_success_headers(created_item_serializer.data)
            return Response(created_item_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

class PlaylistItemDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Ensures items are queried within the context of the user's playlist.
        playlist_pk = self.kwargs.get('playlist_pk')
        # Ensures the playlist belongs to the current authenticated user.
        playlist = get_object_or_404(Playlist, pk=playlist_pk, user=self.request.user)
        return PlaylistItem.objects.filter(playlist=playlist)

    def get_object(self):
        # Standard object lookup; the queryset is already filtered by user and playlist.
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['item_pk'])
        return obj

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        # Optional: Re-ordering remaining items if 'order' needs to be contiguous.
        # This can be complex and might be better handled separately or omitted.
        # Currently, deleting an item will leave a gap in 'order' numbers if they were contiguous.

# Future enhancements could include views for updating playlist items (e.g., reordering).
# For example, a PlaylistItemUpdateAPIView could be implemented.

class PlaylistReorderItemsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistItemReorderSerializer

    def patch(self, request, *args, **kwargs):
        playlist_pk = self.kwargs.get('playlist_pk')
        playlist = get_object_or_404(Playlist, pk=playlist_pk, user=request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        item_ids_ordered_input = serializer.validated_data['item_ids']

        # --- Comprehensive Validation for Full Reorder ---

        # 1. Check for duplicate item IDs in the input list.
        if len(item_ids_ordered_input) != len(set(item_ids_ordered_input)):
            return Response(
                {"error": "Duplicate item IDs found in the reorder list. Each item ID must be unique."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Check if the provided item IDs exactly match all items in the playlist.
        # This ensures a full reorder: no items missing from the input, and no extraneous items included.
        current_playlist_item_pks = set(playlist.items.values_list('pk', flat=True))
        input_item_pks = set(item_ids_ordered_input)

        if current_playlist_item_pks != input_item_pks:
            missing_items = current_playlist_item_pks - input_item_pks
            extra_items = input_item_pks - current_playlist_item_pks
            error_messages = []
            if missing_items:
                error_messages.append(f"The following item IDs from the playlist are missing in the input: {list(missing_items)}.")
            if extra_items:
                error_messages.append(f"The following input item IDs do not belong to this playlist: {list(extra_items)}.")
            
            return Response(
                {"error": "The provided list of item IDs does not exactly match the items in the playlist. " + " ".join(error_messages) + " A full list of all items in their new order is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- Perform Reorder Operation ---
        try:
            with transaction.atomic():
                # Create a mapping of pk to item instance for efficient updates
                items_map = {item.pk: item for item in playlist.items.all()}
                for index, item_id in enumerate(item_ids_ordered_input):
                    item_to_update = items_map.get(item_id)
                    # This check is a safeguard, though previous validation should ensure item_to_update is found.
                    if item_to_update is None: 
                        # This state should not be reached if above validations are correct.
                        # Consider logging this as a server-side anomaly.
                        raise PlaylistItem.DoesNotExist(f"PlaylistItem with id {item_id} not found in playlist during reorder, despite passing validation.")
                    item_to_update.order = index + 1 # Assuming 1-based order for client-facing display or consistency.
                    item_to_update.save(update_fields=['order'])
        except PlaylistItem.DoesNotExist as e:
            # Log this exception, as it indicates a potential flaw in validation logic if reached.
            print(f"Error during reorder: {str(e)}") # Replace with actual logging
            return Response(
                {"error": "An internal error occurred: one or more item IDs became invalid during the reorder process."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR 
            )
        except Exception as e:
            # Log the generic exception for server-side diagnostics.
            print(f"Unexpected error during reorder: {str(e)}") # Replace with actual logging
            return Response(
                {"error": "An unexpected error occurred while reordering items."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        # Return the updated playlist, reflecting the new order.
        # Fetching the playlist again to ensure items are correctly ordered in the serializer.
        updated_playlist = Playlist.objects.prefetch_related('items').get(pk=playlist.pk)
        updated_playlist_serializer = PlaylistSerializer(updated_playlist)
        return Response(updated_playlist_serializer.data, status=status.HTTP_200_OK)

class PlaylistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        playlist = self.get_object()
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if playlist.share_with_user(email):
            return Response({'message': 'Playlist shared successfully'})
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
