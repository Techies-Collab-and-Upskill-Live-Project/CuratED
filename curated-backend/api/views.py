from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView

from rest_framework.response import Response
from rest_framework import status
from .youtube import fetch_videos_by_keyword 
from .serializers import WatchedVideoSerializer
from .models import WatchedVideo
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers


class YouTubeSearchAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Processing search request for: '{query}'")
        results = fetch_videos_by_keyword(query)
        
        if "error" in results:
            print(f"Error in fetch_videos_by_keyword: {results['error']}")
            return Response({"error": results["error"]}, status=status.HTTP_502_BAD_GATEWAY)
        
        # The results are expected to be already processed by fetch_videos_by_keyword.
        # Return the results as-is with an appropriate HTTP status.
        return Response(results, status=status.HTTP_200_OK)
    
# View for marking a video as watched. Data is typically provided by the frontend.
class MarkVideoWatchedAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchedVideoSerializer

    def perform_create(self, serializer):
        """
        This endpoint receives video properties for a video the user is watching 
        and stores them in the database.
        User authentication is handled by the IsAuthenticated permission class.
        If the video is already marked as watched by the user, a validation error is raised,
        preventing duplicate entries for the same user and video.
        
        The typical user flow:
        1. User searches for a video.
        2. Results are fetched from the YouTube API.
        3. User selects a video.
        4. Frontend collects video details and sends them to this endpoint.
        5. This endpoint stores the details in the WatchedVideo table.
        
        Swagger UI can be useful for testing this endpoint, as it facilitates login 
        for authenticated requests. Uncomment related paths in urls.py if needed.
        """
        video_id = self.request.data.get('video_id')
        if WatchedVideo.objects.filter(user=self.request.user, video_id=video_id).exists():
            raise serializers.ValidationError({"video_id": "Video already marked as watched."})
        serializer.save(user=self.request.user)


"""
This view lists all videos that the authenticated user has marked as watched.
"""
class WatchedVideoListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class =  WatchedVideoSerializer
    
    def get_queryset(self):
        # Returns only videos watched by the current user, ordered by the most recent.
        return WatchedVideo.objects.filter(user=self.request.user).order_by('-watched_at')
