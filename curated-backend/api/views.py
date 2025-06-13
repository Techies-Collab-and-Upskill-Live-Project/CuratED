from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .youtube import fetch_videos_by_keyword, invalidate_cache
from .serializers import YouTubeSearchSerializer, WatchedVideoSerializer, VideoFeedbackSerializer, VideoProgressSerializer
from .models import WatchedVideo, VideoFeedback, VideoProgress
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers
from rest_framework.exceptions import APIException


class YouTubeSearchAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = YouTubeSearchSerializer

    def get_queryset(self):
        # Get query parameters
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)  
        
        # Extract validated data
        params = serializer.validated_data
        
        
        # Call fetch_videos_by_keyword
        results = fetch_videos_by_keyword(
            query=params['q'],
            max_results=params['max_results'],
            educational_focus=params['educational_focus'],
            content_filter=params['content_filter'],
            min_duration=params['min_duration'],
            max_duration=params['max_duration'],
            sort_by=params['sort_by'],
            page_token=params['page_token']
        )
        
        # Handle errors
        if "error" in results:
            print(f"Error in fetch_videos_by_keyword: {results['error']}")
            # Raise an exception to return 502
            raise APIException(detail=results["error"], code=status.HTTP_502_BAD_GATEWAY)
        
        # Return results as a "queryset" (list of dicts)
        return results.get('results', [])
    
    def list(self, request, *args, **kwargs):
        results = self.get_queryset()
        serializer = self.get_serializer(self.request.query_params)
        return Response({
            'results': results,
            'query': serializer.validated_data['q'],
            'total_results': len(results),
            'next_page_token': results.get('next_page_token'),
            'prev_page_token': results.get('prev_page_token')
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


class VideoProgressUpdateView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoProgressSerializer
    lookup_field = 'video_id'

    def get_queryset(self):
        return VideoProgress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        invalidate_cache(video_id=self.kwargs.get('video_id'))