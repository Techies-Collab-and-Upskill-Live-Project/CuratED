from rest_framework import serializers
from .models import WatchedVideo, VideoFeedback, VideoComment, VideoProgress



class YouTubeSearchSerializer(serializers.Serializer):
    q = serializers.CharField(required=True)
    max_results = serializers.IntegerField(default=10, min_value=1)
    educational_focus = serializers.BooleanField(default=True)
    content_filter = serializers.ChoiceField(choices=['none', 'moderate', 'strict'], default='moderate')
    min_duration = serializers.IntegerField(required=False, allow_null=True, default=None)
    max_duration = serializers.IntegerField(required=False, allow_null=True, default=None)
    sort_by = serializers.ChoiceField(choices=['relevance', 'date', 'viewCount', 'rating'], default='viewCount')  # Changed default
    page_token = serializers.CharField(required=False, allow_null=True, default=None)

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

class VideoFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFeedback
        fields = ['id', 'video_id', 'rating', 'comment', 'helpful', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_video_id(self, value):
        # Ensure video exists in watched videos
        user = self.context['request'].user
        if not WatchedVideo.objects.filter(user=user, video_id=value).exists():
            raise serializers.ValidationError("You can only provide feedback for videos you've watched.")
        return value

class VideoCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = VideoComment
        fields = ['id', 'video_id', 'text', 'timestamp', 'created_at', 
                 'updated_at', 'user_email', 'parent', 'replies', 'is_edited']
        read_only_fields = ['created_at', 'updated_at', 'user_email', 'is_edited']

    def get_replies(self, obj):
        if obj.parent is None:  # Only get replies for parent comments
            replies = obj.replies.all()
            return VideoCommentSerializer(replies, many=True).data
        return []

class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ['video_id', 'current_time', 'duration', 'percentage_watched', 'last_watched']
        read_only_fields = ['last_watched']
