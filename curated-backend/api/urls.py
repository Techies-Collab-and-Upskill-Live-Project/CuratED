from django.urls import path
from .views import *

urlpatterns = [
    path('search/', YouTubeSearchAPIView.as_view(), name='youtube_search'),
    path('progress/mark/', MarkVideoWatchedAPIView.as_view(), name='mark_video_watched'),
    path('progress/list/', WatchedVideoListView.as_view(), name='watched-videos-list'),
    path('feedback/', VideoFeedbackCreateView.as_view(), name='video-feedback-create'),
    path('feedback/<str:video_id>/', VideoFeedbackDetailView.as_view(), name='video-feedback-detail'),
    # path('videos/<str:video_id>/comments/', VideoCommentListCreateView.as_view(), name='video-comments'),
    # path('videos/<str:video_id>/comments/<int:pk>/', VideoCommentDetailView.as_view(), name='comment-detail'),
    path('videos/<str:video_id>/progress/', VideoProgressUpdateView.as_view(), name='video-progress'),
]

