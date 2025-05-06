from django.urls import path
from .views import *

urlpatterns = [
    path('api/search/', YouTubeSearchAPIView.as_view(), name='youtube_search'),
    path('api/progress/mark/', MarkVideoWatchedAPIView.as_view(), name='mark_video_watched'),
]

