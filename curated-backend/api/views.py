from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .youtube import fetch_videos_by_keyword 

class YouTubeSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({"error": "Search query is required."}, status=status.HTTP_400_BAD_REQUEST)

        results = fetch_videos_by_keyword(query)
        if "error" in results:
            return Response({"error": "Failed to fetch YouTube."}, status=status.HTTP_502_BAD_GATEWAY)
        
        videos = []
        for item in results.get("items", []):
            videos.append({
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "channel": item["snippet"]["channelTitle"],
            })
        return Response({"results": videos}, status=status.HTTP_200_OK)
