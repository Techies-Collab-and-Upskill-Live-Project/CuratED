import requests
from decouple import config
import re
import json
from django.core.cache import cache
import hashlib
import math
import traceback # For more detailed error logging

API_KEY = config("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Cache timeouts
SEARCH_CACHE_TIMEOUT = 3600  # 1 hour
VIDEO_DETAILS_CACHE_TIMEOUT = 86400  # 24 hours
CHANNEL_DETAILS_CACHE_TIMEOUT = 86400  # 24 hours


def generate_cache_key(prefix, identifier_string):
    """Generate a unique cache key."""
    key_string = f"{prefix}:{identifier_string}"
    return hashlib.md5(key_string.encode()).hexdigest()


def get_channel_details_map(channel_ids):
    """
    Get details (especially thumbnails) for a list of channel IDs.
    Items are cached individually.
    Returns a map of channelId to its medium profile picture URL.
    """
    if not channel_ids:
        return {}

    unique_channel_ids = sorted(list(set(channel_ids)))
    channel_details_map = {}
    ids_to_fetch = []

    for channel_id in unique_channel_ids:
        cache_key = generate_cache_key("channel_detail", channel_id)
        cached_channel_data = cache.get(cache_key)
        if cached_channel_data:
            channel_details_map[channel_id] = cached_channel_data
            print(f"Cache hit for channel_detail: {channel_id}")
        else:
            ids_to_fetch.append(channel_id)

    if ids_to_fetch:
        print(f"Cache miss for channel_details: {ids_to_fetch}. Fetching from API.")
        chunk_size = 50
        for i in range(0, len(ids_to_fetch), chunk_size):
            chunk = ids_to_fetch[i:i + chunk_size]
            params = {
                'part': 'snippet',
                'id': ','.join(chunk),
                'key': API_KEY
            }
            try:
                response = requests.get(CHANNEL_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('items', []):
                        fetched_channel_id = item['id']
                        thumbnails = item.get('snippet', {}).get('thumbnails', {})
                        profile_pic_url = thumbnails.get('medium', {}).get('url') or \
                                          thumbnails.get('default', {}).get('url')
                        if profile_pic_url:
                            channel_details_map[fetched_channel_id] = profile_pic_url
                            # Cache individually
                            individual_cache_key = generate_cache_key("channel_detail", fetched_channel_id)
                            cache.set(individual_cache_key, profile_pic_url, timeout=CHANNEL_DETAILS_CACHE_TIMEOUT)
                            print(f"Cached channel_detail: {fetched_channel_id}")
                else:
                    print(f"Error fetching channel details: {response.status_code} for IDs {','.join(chunk)}")
                    print(f"Response: {response.text}")
            except Exception as e:
                print(f"Exception fetching channel details for IDs {','.join(chunk)}: {str(e)}")
    
    return channel_details_map


def fetch_videos_by_keyword(query, max_results=10, educational_focus=True, content_filter='moderate',
                          min_duration=None, max_duration=None, sort_by='viewCount', page_token=None):
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
    api_params = {
        'part': 'snippet',
        'q': query, # This will be updated to effective_query before API call
        'maxResults': max_results,
        'type': 'video',
        'key': API_KEY,
        'relevanceLanguage': 'en',
        'videoEmbeddable': 'true',
        'safeSearch': content_filter,
        'videoDefinition': 'high',
        'order': sort_by,
        'regionCode': 'US',
        'videoDuration': 'any'
    }
    if page_token:
        api_params['pageToken'] = page_token

    effective_query = query
    if educational_focus:
        edu_terms = ['tutorial', 'learn', 'course', 'education', 'how to']
        if not any(term in query.lower() for term in edu_terms):
            effective_query = f"{query} tutorial"
    
    # Use effective_query for the API call and for part of the cache key logic
    api_params_for_call = api_params.copy()
    api_params_for_call['q'] = effective_query

    # Cache key for the overall search result
    # Hash includes the effective_query used in the actual API call.
    api_params_hash = hashlib.md5(json.dumps(api_params_for_call, sort_keys=True).encode()).hexdigest()
    # Using original_query in prefix for human readability if desired, but hash ensures uniqueness
    search_cache_key = generate_cache_key(f"search:{query}", api_params_hash) 
    
    cached_result = cache.get(search_cache_key)
    if cached_result:
        print(f"Cache hit for search query '{query}' (effective: '{effective_query}') with params hash: {api_params_hash}")
        return cached_result

    print(f"Searching YouTube for: '{effective_query}'")
    
    try:
        response = requests.get(SEARCH_URL, params=api_params_for_call)
        print(f"YouTube API request URL: {response.url.replace(API_KEY, 'API_KEY_HIDDEN')}")
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            search_data = response.json()
            item_count = len(search_data.get('items', []))
            print(f"YouTube API returned {item_count} items")

            if item_count == 0:
                result = { # Define result before caching
                    "results": [],
                    "message": "No videos found for your search",
                    "next_page_token": search_data.get('nextPageToken'),
                    "prev_page_token": search_data.get('prevPageToken')
                }
                cache.set(search_cache_key, result, timeout=SEARCH_CACHE_TIMEOUT)
                return result

            video_ids = []
            source_channel_ids = []
            for item in search_data.get('items', []):
                try:
                    if 'id' in item and 'videoId' in item['id']:
                        video_ids.append(item['id']['videoId'])
                        if 'channelId' in item['snippet']:
                             source_channel_ids.append(item['snippet']['channelId'])
                except (KeyError, TypeError) as e:
                    print(f"Error extracting video ID or source channel ID: {e}")
            
            if not video_ids:
                result = { # Define result before caching
                    "results": [],
                    "message": "No valid videos found",
                    "debug_info": {
                        "response_structure": str(search_data.keys()),
                        "item_count": item_count
                    },
                    "next_page_token": search_data.get('nextPageToken'),
                    "prev_page_token": search_data.get('prevPageToken')
                }
                cache.set(search_cache_key, result, timeout=SEARCH_CACHE_TIMEOUT)
                return result

            detailed_videos_map = get_video_details(video_ids)
            channel_profile_pics_map = get_channel_details_map(source_channel_ids)

            processed_results = process_search_results(
                search_data, detailed_videos_map, channel_profile_pics_map, 
                query, min_duration, max_duration
            )

            final_result_data = {} # Define before conditional assignment
            if not processed_results and item_count > 0:
                print("All videos were filtered out, using basic results")
                basic_results = []
                for item_basic in search_data.get('items', []): # Renamed item to item_basic
                    try:
                        video_id_basic = item_basic['id']['videoId'] # Renamed
                        snippet_basic = item_basic['snippet'] # Renamed
                        basic_results.append({
                            'id': video_id_basic,
                            'title': snippet_basic.get('title', ''),
                            'description': snippet_basic.get('description', ''),
                            'thumbnail': snippet_basic.get('thumbnails', {}).get('high', {}).get('url', ''),
                            'channelTitle': snippet_basic.get('channelTitle', ''),
                            'publishedAt': snippet_basic.get('publishedAt', ''),
                            # Add channelProfileImageUrl if available, even for basic
                            'channelProfileImageUrl': channel_profile_pics_map.get(snippet_basic.get('channelId')),
                        })
                    except (KeyError, TypeError) as e:
                        print(f"Error extracting basic video data: {e}")


                final_result_data = {
                    "results": basic_results,
                    "query": query,
                    "total_results": len(basic_results),
                    "note": "Using unfiltered results due to filter removing all items",
                    "next_page_token": search_data.get('nextPageToken'),
                    "prev_page_token": search_data.get('prevPageToken')
                }
            else:
                final_result_data = {
                    "results": processed_results,
                    "query": query,
                    "total_results": len(processed_results),
                    "next_page_token": search_data.get('nextPageToken'),
                    "prev_page_token": search_data.get('prevPageToken')
                }
            
            cache.set(search_cache_key, final_result_data, timeout=SEARCH_CACHE_TIMEOUT)
            return final_result_data
        else:
            print(f"YouTube API Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": "Failed to fetch videos from YouTube", "status": response.status_code}

    except Exception as e:
        print(f"Exception in fetch_videos_by_keyword: {str(e)}")
        traceback.print_exc() # Add traceback for better debugging
        return {"error": "An unexpected error occurred", "details": str(e)}


def get_video_details(video_ids):
    """Get additional details about videos. Items are cached individually. Returns a map."""
    if not video_ids:
        return {}

    unique_video_ids = sorted(list(set(video_ids)))
    video_details_map = {}
    ids_to_fetch = []

    for video_id in unique_video_ids:
        cache_key = generate_cache_key("video_detail", video_id)
        cached_video_data = cache.get(cache_key)
        if cached_video_data:
            video_details_map[video_id] = cached_video_data
            print(f"Cache hit for video_detail: {video_id}")
        else:
            ids_to_fetch.append(video_id)

    if ids_to_fetch:
        print(f"Cache miss for video_details: {ids_to_fetch}. Fetching from API.")
        chunk_size = 50
        for i in range(0, len(ids_to_fetch), chunk_size):
            chunk = ids_to_fetch[i:i + chunk_size]
            params = {
                'part': 'snippet,contentDetails,statistics',
                'id': ','.join(chunk),
                'key': API_KEY
            }
            try:
                response = requests.get(VIDEO_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('items', []):
                        fetched_video_id = item['id']
                        video_details_map[fetched_video_id] = item
                        # Cache individually
                        individual_cache_key = generate_cache_key("video_detail", fetched_video_id)
                        cache.set(individual_cache_key, item, timeout=VIDEO_DETAILS_CACHE_TIMEOUT)
                        print(f"Cached video_detail: {fetched_video_id}")
                else:
                    print(f"Error fetching video details: {response.status_code} for IDs {','.join(chunk)}")
            except Exception as e:
                print(f"Exception fetching video details for IDs {','.join(chunk)}: {str(e)}")
    
    return video_details_map


def process_search_results(search_data, detailed_videos_map, channel_profile_pics_map, 
                           original_query, min_duration=None, max_duration=None):
    """Process and rank search results with enhanced relevance scoring."""
    processed_results = []
    edu_keywords = {
        'tutorial', 'learn', 'lesson', 'course', 'education', 'training',
        'guide', 'explanation', 'explained', 'introduction', 'basics',
        'how to', 'beginner', 'instructor', 'teaching', 'class', 'lecture',
        'masterclass', 'workshop', 'insights', 'analysis'
    }
    # Keywords/patterns that might indicate lower quality or clickbait for educational content
    spammy_title_keywords = {
        'must watch!!!', 'shocking', 'secret revealed', 'ultimate guide', 'easy way',
        'guaranteed', 'free money', 'hack your', 'top 10 secrets' # Be cautious with these
    }
    query_terms = set(original_query.lower().split())

    if not search_data.get('items'):
        print("No items in search_data to process")
        return processed_results

    print(f"Processing {len(search_data.get('items', []))} search results")

    for item in search_data.get('items', []): # item here is from search_data (initial search)
        try:
            video_id = item['id']['videoId']
            snippet = item['snippet'] # Snippet from initial search
            title = snippet.get('title', '')
            description = snippet.get('description', '')
            channel_title = snippet.get('channelTitle', '')
            source_channel_id = snippet.get('channelId', '')

            relevance_score = 0.0
            title_lower = title.lower()
            content_text = (title_lower + " " + description.lower())

            # Penalize spammy/clickbait titles
            for spam_keyword in spammy_title_keywords:
                if spam_keyword in title_lower:
                    relevance_score -= 2.5 # Slightly increased penalty
                    print(f"Penalizing title for spammy keyword '{spam_keyword}': {title}")
                    break # Apply penalty once per video for title

            # Boost score for educational keywords
            for keyword in edu_keywords:
                if keyword in content_text:
                    relevance_score += 1.5 # Slightly reduced from 2, to balance with engagement

            # Boost score for query term matches
            title_words = set(title_lower.split())
            query_match_count = len(query_terms.intersection(title_words))
            relevance_score += query_match_count * 2.0 # Adjusted weight for direct query match

            likes = 0
            comment_count = 0
            view_count = 0
            duration = "Unknown"
            duration_seconds = 0
            # Get profile pic from the map passed into this function
            channel_profile_image_url = channel_profile_pics_map.get(source_channel_id) 

            # Get detailed video statistics from the map passed into this function
            video_specific_details = detailed_videos_map.get(video_id) 
            if video_specific_details:
                if 'statistics' in video_specific_details:
                    stats = video_specific_details['statistics']
                    likes = int(stats.get('likeCount', 0))
                    comment_count = int(stats.get('commentCount', 0))
                    view_count = int(stats.get('viewCount', 0))

                    # Significantly boost recognizable/notable videos based on high engagement
                    # Using higher multipliers and thresholds for "notability"
                    if view_count > 50000:  # Notable view count
                        relevance_score += math.log10(view_count) * 1.2 # Stronger view bonus
                    elif view_count > 1000: 
                        relevance_score += math.log10(view_count) * 0.8 
                    elif view_count < 500 and view_count > 0:
                        relevance_score -= 0.75 # Stronger penalty for very low views

                    if likes > 10000:  # Notable like count
                        relevance_score += math.log10(likes) * 1.0 # Stronger like bonus
                    elif likes > 500:
                        relevance_score += math.log10(likes) * 0.6
                    elif likes < 100 and likes > 0:
                        relevance_score -= 0.5 # Stronger penalty for very low likes
                    
                    # Add a "notability" bonus if both views and likes are very high
                    if view_count > 100000 and likes > 20000:
                        relevance_score += 2.0 # Extra notability boost
                    elif view_count > 50000 and likes > 10000:
                        relevance_score += 1.0


                    if comment_count > 1000: # Notable comment count
                        relevance_score += math.log10(comment_count) * 0.5 # Stronger comment bonus
                    elif comment_count > 50:
                        relevance_score += math.log10(comment_count) * 0.3
                
                if 'contentDetails' in video_specific_details:
                    duration_str = video_specific_details['contentDetails'].get('duration', '')
                    duration_match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
                    if duration_match:
                        hours = int(duration_match.group(1) or 0)
                        minutes = int(duration_match.group(2) or 0)
                        seconds = int(duration_match.group(3) or 0)
                        duration_seconds = hours * 3600 + minutes * 60 + seconds
                        duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"
                        
                        if min_duration and duration_seconds < min_duration:
                            print(f"Video '{title}' too short ({duration_seconds}s), skipping.")
                            continue
                        if max_duration and duration_seconds > max_duration:
                            print(f"Video '{title}' too long ({duration_seconds}s), skipping.")
                            continue
            
            # Adjusted MIN_RELEVANCE_THRESHOLD logic
            # A video with extremely high engagement might pass even if its base score is low.
            # A video with moderate engagement needs a decent base score.
            MIN_BASE_RELEVANCE_FOR_MODERATE_ENGAGEMENT = 1.0 
            EXTREME_ENGAGEMENT_VIEWS = 500000 # Example: half a million views
            EXTREME_ENGAGEMENT_LIKES = 50000   # Example: 50k likes

            is_extremely_engaging = view_count > EXTREME_ENGAGEMENT_VIEWS and likes > EXTREME_ENGAGEMENT_LIKES

            if not is_extremely_engaging and relevance_score < MIN_BASE_RELEVANCE_FOR_MODERATE_ENGAGEMENT:
                 # For videos that aren't "viral hits", they need some topical relevance.
                 if not (view_count > 20000 and likes > 2000): # Allow moderately popular videos with some relevance
                    print(f"Video '{title}' below relevance threshold ({relevance_score}) and not extremely engaging, skipping.")
                    continue

            processed_results.append({
                'id': video_id,
                'title': title,
                'description': description,
                'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'channelTitle': channel_title,
                'channelProfileImageUrl': channel_profile_image_url,
                'publishedAt': snippet.get('publishedAt', ''),
                'relevance_score': round(relevance_score, 2),
                'likes': likes,
                'comment_count': comment_count,
                'view_count': view_count,
                'duration': duration,
                'duration_seconds': duration_seconds
            })
        except (KeyError, TypeError) as e:
            print(f"Error processing search result item: {e}")
            traceback.print_exc()

    print(f"After filtering, {len(processed_results)} videos remain")
    processed_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    return processed_results


def invalidate_cache(video_id=None, channel_id=None): # Removed query, added channel_id
    """Invalidate cache for specific video or channel ID."""
    if video_id:
        video_cache_key = generate_cache_key("video_detail", video_id)
        cache.delete(video_cache_key)
        print(f"Invalidated cache for video_detail: {video_id}")

    if channel_id:
        channel_cache_key = generate_cache_key("channel_detail", channel_id)
        cache.delete(channel_cache_key)
        print(f"Invalidated cache for channel_detail: {channel_id}")

    # Note: Invalidating search results that might contain this video/channel
    # is complex and not handled here. Search results rely on their own TTL.
    # If a video's underlying channel changes, its channel_id might change,
    # or its profile pic. For simplicity, we only invalidate the direct channel_id cache.
