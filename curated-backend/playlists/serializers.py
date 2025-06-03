from rest_framework import serializers
from .models import Playlist, PlaylistItem

class PlaylistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistItem
        fields = ['id', 'video_id', 'title', 'thumbnail_url', 'channel_title', 'order', 'added_at']
        read_only_fields = ['id', 'order', 'added_at'] # Order is managed by the backend

class PlaylistSerializer(serializers.ModelSerializer):
    items = PlaylistItemSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True, source='user.id')
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ['id', 'user_id', 'name', 'description', 'created_at', 'updated_at', 'items', 'progress']
        read_only_fields = ['id', 'user_id', 'created_at', 'updated_at', 'items']

    def get_progress(self, obj):
        user = self.context['request'].user
        return obj.get_progress_for_user(user)

class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['name', 'description']

    def create(self, validated_data):
        user = self.context['request'].user
        # Check for uniqueness constraint manually if needed, though model's unique_together handles it at DB level
        if Playlist.objects.filter(user=user, name=validated_data['name']).exists():
            raise serializers.ValidationError({"name": "You already have a playlist with this name."})
        playlist = Playlist.objects.create(user=user, **validated_data)
        return playlist

class PlaylistItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistItem
        fields = ['video_id', 'title', 'thumbnail_url', 'channel_title']
        # 'playlist' and 'order' will be set in the view or by model's save method

class PlaylistItemReorderSerializer(serializers.Serializer):
    item_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="A list of PlaylistItem IDs in the desired new order."
    )

    def validate_item_ids(self, value):
        # This serializer-level validation ensures the basic structure and type of 'item_ids'.
        # It confirms 'item_ids' is a list and contains integers.
        # Business logic validation, such as ensuring these IDs belong to the specific playlist,
        # that all items from the playlist are present, and that there are no duplicate IDs within the list,
        # is handled in the API view where database context is available.
        if not value:
            raise serializers.ValidationError("item_ids list cannot be empty.")
        # Basic check for type consistency if child=serializers.IntegerField() wasn't enough (it usually is)
        # For example, ensuring all elements are indeed integers if mixed types were possible.
        # However, ListField with child=IntegerField already handles this.
        return value
