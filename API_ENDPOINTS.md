# 📚 CuratED API Endpoints Reference

This document lists all major API endpoints, their HTTP methods, payloads, and expected responses for frontend integration.

---

## Authentication

### Register User
- **POST** `/api/v1/users/register/`
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "YourPassword123"
  }
  ```
- **Response:**  
  `201 Created`  
  ```json
  { "detail": "User registered. OTP sent to your email." }
  ```

---

### Login (JWT)
- **POST** `/api/v1/users/login/`
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "password": "YourPassword123"
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  {
    "refresh": "refresh_token",
    "access": "access_token"
  }
  ```

---

### Verify OTP
- **POST** `/api/v1/users/verify-otp/`
- **Payload:**
  ```json
  {
    "email": "user@example.com",
    "otp": "1234"
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  { "message": "Account verified successfully" }
  ```

---

### Resend OTP
- **POST** `/api/v1/users/resend-verification/`
- **Payload:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  { "detail": "OTP sent to your email." }
  ```

---

### Password Reset Request
- **POST** `/api/v1/users/password-reset/`
- **Payload:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  { "message": "If this email exists, password reset instructions have been sent." }
  ```

---

### Password Reset Confirm
- **POST** `/api/v1/users/password-reset/confirm/`
- **Payload:**
  ```json
  {
    "uid": "base64_user_id",
    "token": "reset_token",
    "new_password": "NewPassword123"
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  { "message": "Password reset successful" }
  ```

---

### Change Password (Authenticated)
- **PUT** `/api/v1/users/password/change/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "old_password": "OldPassword123",
    "new_password": "NewPassword123"
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  { "message": "Password updated successfully" }
  ```

---

## YouTube & Video Content

### Search YouTube
- **GET** `/api/v1/search/?q=python&max_results=10&educational_focus=true`
- **Query Params:**
  - `q` (required): Search keywords
  - `max_results` (optional): Default 25
  - `educational_focus` (optional): Default true
  - `content_filter` (optional): none/moderate/strict
  - `min_duration` (optional): seconds
  - `max_duration` (optional): seconds
  - `sort_by` (optional): relevance/date/viewCount/rating
  - `page_token` (optional): for pagination
- **Response:**  
  `200 OK`  
  ```json
  {
    "results": [ ...video objects... ],
    "query": "python",
    "total_results": 25,
    "next_page_token": "string_or_null",
    "prev_page_token": "string_or_null"
  }
  ```

---

### Mark Video as Watched
- **POST** `/api/v1/progress/mark/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "video_id": "abc123",
    "title": "Video Title",
    "description": "Video description",
    "thumbnail": "https://...",
    "channel_title": "Channel Name",
    "published_at": "2024-01-01T00:00:00Z",
    "likes": 100,
    "comment_count": 10,
    "duration": "12:34"
  }
  ```
- **Response:**  
  `201 Created`  
  ```json
  { ...watched video object... }
  ```

---

### Get Watched Videos
- **GET** `/api/v1/progress/list/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Response:**  
  `200 OK`  
  ```json
  [ ...list of watched video objects... ]
  ```

---

### Submit Video Feedback
- **POST** `/api/v1/feedback/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "video_id": "abc123",
    "rating": 5,
    "comment": "Great video!",
    "helpful": true
  }
  ```
- **Response:**  
  `201 Created`  
  ```json
  { ...feedback object... }
  ```

---

### Get/Update/Delete Video Feedback
- **GET/PUT/DELETE** `/api/v1/feedback/<video_id>/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Response:**  
  - GET: Feedback object
  - PUT: Updated feedback object
  - DELETE: 204 No Content

---

### Update Video Progress
- **PUT** `/api/v1/videos/<video_id>/progress/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "current_time": 120,
    "duration": 600,
    "percentage_watched": 20
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  { ...progress object... }
  ```

---

## Playlists

### Create Playlist
- **POST** `/api/v1/playlists/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "name": "My Playlist",
    "description": "A collection of my favorite videos"
  }
  ```
- **Response:**  
  `201 Created`  
  ```json
  { ...playlist object... }
  ```

---

### List User Playlists
- **GET** `/api/v1/playlists/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Response:**  
  `200 OK`  
  ```json
  [ ...list of playlist objects... ]
  ```

---

### Add Video to Playlist
- **POST** `/api/v1/playlists/<playlist_id>/add/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "video_id": "abc123",
    "title": "Video Title",
    "description": "Video description",
    "thumbnail": "https://...",
    "channel_title": "Channel Name",
    "published_at": "2024-01-01T00:00:00Z"
  }
  ```
- **Response:**  
  `201 Created`  
  ```json
  { ...playlist item object... }
  ```

---

### Remove Video from Playlist
- **DELETE** `/api/v1/playlists/<playlist_id>/remove/<video_id>/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Response:**  
  `204 No Content`

---

### Get Playlist Details
- **GET** `/api/v1/playlists/<playlist_id>/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Response:**  
  `200 OK`  
  ```json
  { ...playlist object with items... }
  ```

---

### Reorder Playlist Items
- **POST** `/api/v1/playlists/<playlist_id>/reorder/`
- **Headers:**  
  `Authorization: Bearer <access_token>`
- **Payload:**
  ```json
  {
    "item_ids": ["item_id1", "item_id2", "item_id3"]
  }
  ```
- **Response:**  
  `200 OK`  
  ```json
  { "message": "Playlist reordered successfully" }
  ```

---

## Notes

- All endpoints return errors in the format:
  ```json
  { "error": "Error message" }
  ```
- For authenticated endpoints, always include the `Authorization: Bearer <access_token>` header.
- Pagination tokens (`next_page_token`, `prev_page_token`) are used for YouTube search pagination.

---

**For further details, see the main README or Swagger/Redoc API docs.**
