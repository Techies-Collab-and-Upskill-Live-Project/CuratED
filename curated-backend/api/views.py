from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .youtube import fetch_videos_by_keyword 

class YouTubeSearchAPIView(APIView):
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
