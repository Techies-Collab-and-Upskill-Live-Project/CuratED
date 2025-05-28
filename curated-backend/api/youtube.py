import requests
from decouple import config
import re
import json

API_KEY = config("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"


def fetch_videos_by_keyword(query, max_results=10, educational_focus=True, content_filter='moderate'):
    """
    Enhanced search function that prioritizes educational content based on PRD requirements.
    
    Args:
        query (str): The search term.
        max_results (int): Maximum number of results to return.
        educational_focus (bool): Whether to apply educational content filtering.
        content_filter (str): Content filtering level ('none', 'moderate', 'strict').
    
    Returns:
        dict: Processed search results with educational relevance.
    """
    # Add educational keywords if educational_focus is True.
    search_query = query
    if educational_focus:
        # Only add educational terms if they're not already in the query.
        edu_terms = ['tutorial', 'learn', 'course', 'education', 'how to']
        if not any(term in query.lower() for term in edu_terms):
            search_query = f"{query} tutorial"
    
    print(f"Searching YouTube for: '{search_query}'")
    
    params = {
        'part': 'snippet',
        'q': search_query,
        'key': API_KEY,
        'maxResults': max_results,
        'type': 'video',
        'relevanceLanguage': 'en',  # Can be made configurable based on user preference.
        'videoEmbeddable': 'true',  # Ensures videos can be embedded.
        'safeSearch': content_filter,
        'videoDefinition': 'high',   # Prefers high quality videos.
        'videoDuration': 'medium',   # Duration categories: short <4m, medium 4-20m, long >20m.
    }
    
    try:
        response = requests.get(SEARCH_URL, params=params)
        
        # Debug: Log API request details.
        print(f"YouTube API request URL: {response.url.replace(API_KEY, 'API_KEY_HIDDEN')}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            search_data = response.json()
            
            # Debug: Log the number of items returned by the API.
            item_count = len(search_data.get('items', []))
            print(f"YouTube API returned {item_count} items")
            
            if item_count == 0:
                print("YouTube API returned zero videos")
                return {"results": [], "message": "No videos found for your search"}
            
            # Extract video IDs, handling potential format issues.
            video_ids = []
            for item in search_data.get('items', []):
                try:
                    if 'id' in item and 'videoId' in item['id']:
                        video_ids.append(item['id']['videoId'])
                except (KeyError, TypeError) as e:
                    print(f"Error extracting video ID: {e}")
            
            if not video_ids:
                print("No valid video IDs found in the response")
                # Return original data for debugging if no valid video IDs are found.
                return {
                    "results": [], 
                    "message": "No valid videos found",
                    "debug_info": {
                        "response_structure": str(search_data.keys()),
                        "item_count": item_count
                    }
                }
            
            # Get additional video details for better filtering.
            detailed_results = get_video_details(video_ids)
            
            # Process and rank results by educational relevance.
            processed_results = process_search_results(search_data, detailed_results, query)
            
            # If all results were filtered out, return original search items as a fallback.
            if not processed_results and item_count > 0:
                print("All videos were filtered out by educational criteria, using basic results")
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
                
                return {
                    "results": basic_results,
                    "query": query,
                    "total_results": len(basic_results),
                    "note": "Using unfiltered results due to educational filter removing all items"
                }
                
            return {
                "results": processed_results,
                "query": query,
                "total_results": len(processed_results)
            }
        else:
            print(f"YouTube API Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return {"error": "Failed to fetch videos from YouTube", "status": response.status_code}
            
    except Exception as e:
        print(f"Exception in fetch_videos_by_keyword: {str(e)}")
        return {"error": "An unexpected error occurred", "details": str(e)}

def get_video_details(video_ids):
    """Get additional details about videos to help with educational relevance filtering."""
    if not video_ids:
        return {}
        
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
            return result
        else:
            print(f"Error fetching video details: {response.status_code}")
            print(f"Response: {response.text}")
        return {}
    except Exception as e:
        print(f"Error fetching video details: {str(e)}")
        return {}

def process_search_results(search_data, detailed_results, original_query):
    """Process and rank search results by educational relevance."""
    processed_results = []
    
    # Create a set of educational keywords for filtering.
    edu_keywords = {
        'tutorial', 'learn', 'lesson', 'course', 'education', 'training',
        'guide', 'explanation', 'explained', 'introduction', 'basics',
        'how to', 'beginner', 'instructor', 'teaching', 'class', 'lecture'
    }
    
    # Get original query terms for relevance matching.
    query_terms = set(original_query.lower().split())
    
    if not search_data.get('items'):
        print("No items in search_data to process")
        return processed_results
        
    # Store detailed video data in a dictionary for easier access.
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
            
            # Skip videos that are clearly not educational (this list can be expanded).
            if any(term in title.lower() for term in ['prank', 'funny fail', 'clickbait']):
                print(f"Skipping non-educational video: {title}")
                continue
            
            # Calculate an educational relevance score.
            relevance_score = 0
            
            # Check title and description for educational keywords.
            content_text = (title + " " + description).lower()
            for keyword in edu_keywords:
                if keyword in content_text:
                    relevance_score += 1
                    
            # Add a bonus for exact query matches in the title.
            title_words = set(title.lower().split())
            query_match_count = len(query_terms.intersection(title_words))
            relevance_score += query_match_count * 2
            
            # Get additional metrics from detailed results.
            likes = 0
            comment_count = 0
            duration = "Unknown"
            
            if video_id in video_details:
                details = video_details[video_id]
                # Parse statistics if available.
                if 'statistics' in details:
                    stats = details['statistics']
                    likes = int(stats.get('likeCount', 0))
                    comment_count = int(stats.get('commentCount', 0))
                    
                    # Videos with higher engagement are often more helpful.
                    if likes > 1000:
                        relevance_score += 1
                    if comment_count > 100:
                        relevance_score += 1
                        
                # Get video duration.
                if 'contentDetails' in details:
                    duration = details['contentDetails'].get('duration', '')
            
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
                'duration': duration
            })
        except (KeyError, TypeError) as e:
            print(f"Error processing search result item: {e}")
    
    print(f"After filtering, {len(processed_results)} videos remain")
    
    # Sort results by the calculated educational relevance score.
    processed_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    return processed_results
