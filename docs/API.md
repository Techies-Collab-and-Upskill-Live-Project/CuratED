# CuratED API Documentation

## Authentication Endpoints

### Register User
```http
POST /api/v1/users/register/
```
Register a new user with email verification.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "secure_password",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Login
```http
POST /api/v1/token/
```
Obtain JWT tokens for authentication.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "secure_password",
    "remember_me": true
}
```

## Content Endpoints

### Search Videos
```http
GET /api/v1/search/
```
Search for educational videos with advanced filtering.

**Query Parameters:**
- `q` (required): Search query
- `max_results`: Maximum results (default: 10)
- `educational_focus`: Filter for educational content (default: true)
- `content_filter`: Content filtering level (none/moderate/strict)
- `min_duration`: Minimum video duration in seconds
- `max_duration`: Maximum video duration in seconds
- `sort_by`: Sorting criteria (relevance/date/viewCount/rating)

### Track Progress
```http
POST /api/v1/videos/{video_id}/progress/
```
Update video watching progress.

**Request Body:**
```json
{
    "current_time": 120.5,
    "duration": 300.0,
    "percentage_watched": 40.0
}
```

## Playlist Management

### Create Playlist
```http
POST /api/v1/playlists/
```
Create a new playlist.

**Request Body:**
```json
{
    "name": "Python Tutorials",
    "description": "Collection of Python tutorials",
    "is_public": false
}
```

### Share Playlist
```http
POST /api/v1/playlists/{playlist_id}/share/
```
Share playlist with another user.

**Request Body:**
```json
{
    "email": "friend@example.com"
}
```
