from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class WatchedVideo(models.Model):
    # I used settings.AUTH_USER_MODEL instead of directly referencing User because of the custom user model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='watched_videos')
    video_id = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    channel_title = models.CharField(max_length=255, blank=True)
    published_at = models.DateTimeField()
    watched_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    duration = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ('user', 'video_id') 
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.title} watched by {self.user.get_full_name()}"

class VideoFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1-5"
    )
    comment = models.TextField(blank=True)
    helpful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email}'s feedback on {self.video_id}"

class VideoComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=100)
    text = models.TextField()
    timestamp = models.FloatField(help_text="Video timestamp in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp', 'created_at']

    def __str__(self):
        return f"Comment by {self.user.email} at {self.timestamp}s"

class VideoProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=100)
    current_time = models.FloatField(default=0)
    duration = models.FloatField()
    percentage_watched = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video_id')
        ordering = ['-last_watched']

    def __str__(self):
        return f"{self.user.email}'s progress on {self.video_id}"
