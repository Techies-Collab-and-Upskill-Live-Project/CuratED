from django.db import models
from django.conf import settings
from django.utils import timezone
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