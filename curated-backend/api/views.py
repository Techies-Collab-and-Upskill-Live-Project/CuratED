from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .youtube import fetch_videos_by_keyword


@api_view(['GET'])
def search_videos(request):
    quesry = request.GET.get('q')
    if not query:
        return Response
