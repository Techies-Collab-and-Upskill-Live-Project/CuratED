from django.db import models


# This is Model created by Damilola Olawoore "WatchedVideo"
class WatchedVideo(models.Model):
    video_id = models.CharField(max_length=255)
    video_title = models.CharField(max_length=255)
    video_description = models.TextField()
    channel = models.CharField(max_length=255)
    video_thumbnail = models.URLField()
    watched_marker = models.BooleanField(default=False)
   