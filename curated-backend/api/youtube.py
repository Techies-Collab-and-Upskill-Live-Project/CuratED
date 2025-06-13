import requests
from decouple import config
import re
import json
from django.core.cache import cache
import time
import hashlib

API_KEY = config("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"


def generate_cache_key(query, params):
    """Generate a unique cache key based on query and parameters."""
    param_string = json.dumps(params, sort_keys=True)
    key_string = f"{query}:{param_string}"
    return hashlib.md5(key_string.encode()).hexdigest()


def fetch_videos_by_keyword(query, max_results=10, educational_focus=True, content_filter='moderate',
                          min_duration=None, max_duration=None, sort_by='relevance', page_token=None):
    """
    Enhanced search function with caching, pagination, and advanced filtering.

    Args:
        query (str): The search term.
        max_results (int): Maximum number of results to return.
        educational_focus (bool): Whether to apply educational content filtering.
        content_filter (str): Content filtering level ('none', 'moderate', 'strict').
        min_duration (int): Minimum video duration in seconds.
        max_duration (int): Maximum video duration in seconds.
        sort_by (str): Sorting criteria ('relevance', 'date', 'viewCount', 'rating').
        page_token (str): Token for pagination.

    Returns:
        dict: Processed search results with educational relevance and pagination info.
    """
    # Generate cache key
    params = {
        'part': 'snippet',
        'q': query,
        'maxResults': max_results,
        'type': 'video',
        'relevanceLanguage': 'en',
        'videoEmbeddable': 'true',
        'safeSearch': content_filter,
        'videoDefinition': 'high',
        'videoDuration': 'medium',
        'order': sort_by,
    }
    if page_token:
        params['pageToken'] = page_token

    cache_key = generate_cache_key(query, params)
    cached_result = cache.get(cache_key)
    
    if cached_result:
        print(f"Cache hit for key: {cache_key}")
        return cached_result

    # Add educational keywords if educational_focus is True
    search_query = query
    if educational_focus:
        edu_terms = ['tutorial', 'learn', 'course', 'education', 'how to']
        if not any(term in query.lower() for term in edu_terms):
            search_query = f"{query} tutorial"

    print(f"Searching YouTube for: '{search_query}'")

    params['q'] = search_query
    
    try:
        response = requests.get(SEARCH_URL, params=params)
        print(f"YouTube API request URL: {response.url.replace(API_KEY, 'API_KEY_HIDDEN')}")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            search_data = response.json()
            item_count = len(search_data.get('items', []))
            print(f"YouTube API returned {item_count} items")

            if item_count == 0:
                print("YouTube API returned zero videos")
                result = {
                    "results": [],
                    "message": "No videos found for your search",
                    "next_page_token": search_data.get('nextPageToken'),
                    "prev_page_token": search_data.get('prevPageToken')
                }
                cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
                return result

            video_ids = []
            for item in search_data.get('items', []):
                try:
                    if 'id' in item and 'videoId' in item['id']:
                        video_ids.append(item['id']['videoId'])
                except (KeyError, TypeError) as e:
                    print(f"Error extracting video ID: {e}")

            if not video_ids:
                print("No valid video IDs found in the response")
                result = {
                    "results": [],
                    "message": "No valid videos found",
                    "debug_info": {
                        "response_structure": str(search_data.keys()),
                        "item_count": item_count
                    },
                    "next_page_token": search_data.get('nextPageToken'),
                    "prev_page_token": search_data.get('prevPageToken')
                }
                cache.set(cache_key, result, timeout=3600)
                return result

            detailed_results = get_video_details(video_ids)
            processed_results = process_search_results(
                search_data, detailed_results, query, min_duration, max_duration
            )

            if not processed_results and item_count > 0:
                print("All videos were filtered out, using basic results")
                basic_results = []
                for item in search_data.get('items', []):
                    try:
                        video_id = item['id']['videoId']
                        snippet = item['snippet']
                        basic_results.append({
                            'id': video_id,
                            'title': snippet.get('title', ''),
                            'description': snippet.get('description', ''),
                            'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                            'channelTitle': snippet.get('channelTitle', ''),
                            'publishedAt': snippet.get('publishedAt', ''),
                        })
                    except (KeyError, TypeError) as e:
                        print(f"Error extracting basic video data: {e}")

                result = {
                    "results": basic_results,
                    "query": query,
                    "total_results": len(basic_results),
                    "note": "Using unfiltered results due to filter removing all items",
                    "next_page_token": search_data.get('nextPageToken'),
                    "prev_page_token": search_data.get('prevPageToken')
                }
                cache.set(cache_key, result, timeout=3600)
                return result

            result = {
                "results": processed_results,
                "query": query,
                "total_results": len(processed_results),
                "next_page_token": search_data.get('nextPageToken'),
                "prev_page_token": search_data.get('prevPageToken')
            }
            cache.set(cache_key, result, timeout=3600)
            return result
        else:
            print(f"YouTube API Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": "Failed to fetch videos from YouTube", "status": response.status_code}

    except Exception as e:
        print(f"Exception in fetch_videos_by_keyword: {str(e)}")
        return {"error": "An unexpected error occurred", "details": str(e)}


def get_video_details(video_ids):
    """Get additional details about videos with caching."""
    if not video_ids:
        return {}

    cache_key = f"video_details:{','.join(video_ids)}"
    cached_details = cache.get(cache_key)
    
    if cached_details:
        print(f"Cache hit for video details: {cache_key}")
        return cached_details

    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': ','.join(video_ids),
        'key': API_KEY
    }

    try:
        response = requests.get(VIDEO_URL, params=params)
        if response.status_code == 200:
            result = response.json()
            print(f"Retrieved details for {len(result.get('items', []))} videos")
            cache.set(cache_key, result, timeout=86400)  # Cache for 24 hours
            return result
        else:
            print(f"Error fetching video details: {response.status_code}")
            print(f"Response: {response.text}")
        return {}
    except Exception as e:
        print(f"Error fetching video details: {str(e)}")
        return {}


def process_search_results(search_data, detailed_results, original_query, min_duration=None, max_duration=None):
    """Process and rank search results with enhanced relevance scoring."""
    processed_results = []
    edu_keywords = {
        'tutorial', 'learn', 'lesson', 'course', 'education', 'training',
        'guide', 'explanation', 'explained', 'introduction', 'basics',
        'how to', 'beginner', 'instructor', 'teaching', 'class', 'lecture'
    }
    query_terms = set(original_query.lower().split())

    if not search_data.get('items'):
        print("No items in search_data to process")
        return processed_results

    video_details = {}
    if detailed_results and 'items' in detailed_results:
        for item in detailed_results['items']:
            video_details[item['id']] = item

    print(f"Processing {len(search_data.get('items', []))} search results")

    for item in search_data['items']:
        try:
            video_id = item['id']['videoId']
            snippet = item['snippet']
            title = snippet.get('title', '')
            description = snippet.get('description', '')

            if any(term in title.lower() for term in ['prank', 'funny fail', 'clickbait']):
                print(f"Skipping non-educational video: {title}")
                continue

            # Enhanced relevance scoring
            relevance_score = 0
            content_text = (title + " " + description).lower()
            for keyword in edu_keywords:
                if keyword in content_text:
                    relevance_score += 2  # Increased weight for educational keywords

            title_words = set(title.lower().split())
            query_match_count = len(query_terms.intersection(title_words))
            relevance_score += query_match_count * 3  # Higher weight for query matches

            likes = 0
            comment_count = 0
            duration = "Unknown"
            duration_seconds = 0

            if video_id in video_details:
                details = video_details[video_id]
                if 'statistics' in details:
                    stats = details['statistics']
                    likes = int(stats.get('likeCount', 0))
                    comment_count = int(stats.get('commentCount', 0))
                    # Engagement scoring
                    if likes > 1000:
                        relevance_score += 2
                    if comment_count > 100:
                        relevance_score += 1

                if 'contentDetails' in details:
                    duration = details['contentDetails'].get('duration', '')
                    # Convert ISO 8601 duration to seconds
                    duration_match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
                    if duration_match:
                        hours = int(duration_match.group(1) or 0)
                        minutes = int(duration_match.group(2) or 0)
                        seconds = int(duration_match.group(3) or 0)
                        duration_seconds = hours * 3600 + minutes * 60 + seconds
                        
                        # Apply duration filters
                        if min_duration and duration_seconds < min_duration:
                            continue
                        if max_duration and duration_seconds > max_duration:
                            continue

            processed_results.append({
                'id': video_id,
                'title': title,
                'description': description,
                'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'channelTitle': snippet.get('channelTitle', ''),
                'publishedAt': snippet.get('publishedAt', ''),
                'relevance_score': relevance_score,
                'likes': likes,
                'comment_count': comment_count,
                'duration': duration,
                'duration_seconds': duration_seconds
            })
        except (KeyError, TypeError) as e:
            print(f"Error processing search result item: {e}")

    print(f"After filtering, {len(processed_results)} videos remain")
    
    # Sort by relevance_score or other criteria basedsmouth

    processed_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    return processed_results


def invalidate_cache(query=None, video_id=None):
    """Invalidate cache for specific query or video ID."""
    if query:
        # Invalidate all cache keys containing the query
        cache_key_pattern = f"{query}:*"
        cache.delete_pattern(cache_key_pattern)
    if video_id:
        cache.delete(f"video_details:{video_id}")