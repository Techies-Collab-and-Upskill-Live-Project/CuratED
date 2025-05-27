from rest_framework import serializers
from .models import WatchedVideo

class WatchedVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedVideo
        fields = [
            'video_id', 'title', 'description', 'thumbnail',
            'channel_title', 'published_at', 'watched_at', 'likes',
            'comment_count', 'duration'
        ]
        read_only_fields = ['watched_at', 'user']

    def validate(self, data):
        required_fields = ['video_id', 'title', 'published_at']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: f"{field} is required."})
        return data