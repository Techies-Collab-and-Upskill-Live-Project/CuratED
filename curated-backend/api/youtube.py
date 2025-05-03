import requests
from decouple import config


API_KEY = config("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def fetch_videos_by_keyword(query, max_results=10):
    params = {
        'part': 'snippet',
        'q': query,
        'key': API_KEY,
        'maxResults': max_results,
        'type': 'video',
    }
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return  {"error":"Failed to fetch from Youtube"}
