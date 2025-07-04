from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(
        User,
        related_name='shared_playlists',
        blank=True
    )

    def share_with_user(self, user_email):
        try:
            user = User.objects.get(email=user_email)
            self.shared_with.add(user)
            return True
        except User.DoesNotExist:
            return False

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'name') # A user cannot have two playlists with the same name

    def __str__(self):
        return f"{self.name} by {self.user.email}"

class PlaylistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    video_id = models.CharField(max_length=100) # YouTube video ID
    title = models.CharField(max_length=255)
    thumbnail_url = models.URLField(blank=True, null=True)
    channel_title = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField() # To maintain order of videos in playlist
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['playlist', 'order']
        unique_together = ('playlist', 'video_id') # A video can only appear once in a playlist
        # If re-ordering is frequent, consider removing 'order' from unique_together if video_id should be unique per playlist
        # Or, if a video can be added multiple times, remove unique_together on ('playlist', 'video_id')
        # For now, assuming a video is unique per playlist.

    def __str__(self):
        return f"{self.order}. {self.title} in {self.playlist.name}"

    def save(self, *args, **kwargs):
        if self.order is None:  # Auto-increment order if not set
            last_item = PlaylistItem.objects.filter(playlist=self.playlist).order_by('-order').first()
            self.order = (last_item.order + 1) if last_item else 1
        super().save(*args, **kwargs)
