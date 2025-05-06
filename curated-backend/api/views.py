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
        
        # The results should already be processed by fetch_videos_by_keyword
        # Just return it as-is with appropriate status
        return Response(results, status=status.HTTP_200_OK)
    
# The View for marking a video as watched. The data is feed from the frontend
class MarkVideoWatchedAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchedVideoSerializer

    def perform_create(self, serializer):
        """
        This endpoint gets the video property that the user is watching and stores them in the database.
        The user is authenticated using the IsAuthenticated permission class.
        If the video is already marked as watched, a validation error is raised.
        That means the user is not allowed to mark the same video as watched twice.
        
        The journey from the search is that when the user searches for a video, the results are fetched from the YouTube API.
        The user selects one of the videos, and then the frontend collects the details of the video and sends it to this endpoint.
        This endpoint stores it in the WatchedVideo Table.
        
        Also, I used the swagger ui because I wanted to test the endpoint and I'll have to login to be able to do that which normal 
        browser testing would not allow me to do so. You can uncomment if needed.
        """
        video_id = self.request.data.get('video_id')
        if WatchedVideo.objects.filter(user=self.request.user, video_id=video_id).exists():
            raise serializers.ValidationError({"video_id": "Video already marked as watched."})
        serializer.save(user=self.request.user)


"""
Create the Listing view here. This view is used to list all the videos that the user has watched.

"""