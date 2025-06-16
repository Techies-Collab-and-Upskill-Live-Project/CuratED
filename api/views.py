from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import APIException
from rest_framework.mixins import CreateModelMixin
from .youtube import fetch_videos_by_keyword, invalidate_cache
from .serializers import (
    YouTubeSearchSerializer, WatchedVideoSerializer, 
    VideoFeedbackSerializer, VideoProgressSerializer
)
from .models import WatchedVideo, VideoFeedback, VideoProgress


class YouTubeSearchAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = YouTubeSearchSerializer

    def get_queryset(self):
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        query = validated_data.pop('q') # Extract 'q' as query
        
        results = fetch_videos_by_keyword(query, **validated_data) # Pass query positionally
        
        if "error" in results:
            raise APIException(detail=results["error"], code=status.HTTP_502_BAD_GATEWAY)
        
        return results.get('results', [])
    
    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        params_serializer = self.get_serializer(data=self.request.query_params)
        params_serializer.is_valid(raise_exception=True)
        
        return Response({
            'results': results,
            'query': params_serializer.validated_data['q'],
            'total_results': len(results),
            'next_page_token': getattr(self, 'pagination_token', None),
            'prev_page_token': getattr(self, 'prev_token', None)
        }, status=status.HTTP_200_OK)
        

class MarkVideoWatchedAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchedVideoSerializer

    def perform_create(self, serializer):
        video_id = self.request.data.get('video_id')
        if WatchedVideo.objects.filter(user=self.request.user, video_id=video_id).exists():
            raise serializers.ValidationError({"video_id": "Video already marked as watched."})
        serializer.save(user=self.request.user)
        # Invalidate video details cache
        invalidate_cache(video_id=video_id)


class WatchedVideoListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchedVideoSerializer
    
    def get_queryset(self):
        return WatchedVideo.objects.filter(user=self.request.user).order_by('-watched_at')


class VideoFeedbackCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoFeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Invalidate video details cache
        invalidate_cache(video_id=self.request.data.get('video_id'))


class VideoFeedbackDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoFeedbackSerializer
    lookup_field = 'video_id'

    def get_queryset(self):
        return VideoFeedback.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        invalidate_cache(video_id=self.kwargs.get('video_id'))


class VideoProgressUpdateView(CreateModelMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoProgressSerializer
    lookup_field = 'video_id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return VideoProgress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        invalidate_cache(video_id=self.kwargs.get('video_id'))
        invalidate_cache(video_id=self.kwargs.get('video_id'))


class VideoProgressUpdateView(CreateModelMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoProgressSerializer
    lookup_field = 'video_id'

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return VideoProgress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        invalidate_cache(video_id=self.kwargs.get('video_id'))
