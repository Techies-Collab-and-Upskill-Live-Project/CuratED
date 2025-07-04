# CuratED API Endpoints Documentation

This document provides a detailed overview of all API endpoints available in the CuratED platform.

## Authentication Endpoints

### User Registration
- **URL**: `/api/v1/users/register/`
- **Method**: `POST`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- **Response**: `201 Created` with confirmation message

### OTP Verification
- **URL**: `/api/v1/users/verify-otp/`
- **Method**: `POST`
- **Description**: Verify email with OTP code
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "otp": "1234"
  }
  ```
- **Response**: `200 OK` with success message

### Resend Verification
- **URL**: `/api/v1/users/resend-verification/`
- **Method**: `POST`
- **Description**: Resend OTP to user's email
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**: `200 OK` with confirmation message

### Login
- **URL**: `/api/v1/login/`
- **Method**: `POST`
- **Description**: Obtain JWT tokens
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response**: `200 OK` with access and refresh tokens

### Refresh Token
- **URL**: `/api/v1/token/refresh/`
- **Method**: `POST`
- **Description**: Refresh access token
- **Request Body**:
  ```json
  {
    "refresh": "refresh_token_here"
  }
  ```
- **Response**: `200 OK` with new access token

### Password Reset Request
- **URL**: `/api/v1/users/password-reset/`
- **Method**: `POST`
- **Description**: Request password reset
- **Request Body**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response**: `200 OK` with confirmation message

### Password Reset Confirm
- **URL**: `/api/v1/users/password-reset/confirm/`
- **Method**: `POST`
- **Description**: Confirm password reset
- **Request Body**:
  ```json
  {
    "uid": "encoded_user_id",
    "token": "reset_token",
    "new_password": "NewSecurePassword123!"
  }
  ```
- **Response**: `200 OK` with success message

### Change Password
- **URL**: `/api/v1/users/password/change/`
- **Method**: `PUT`
- **Description**: Change user password (authenticated)
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "old_password": "OldPassword123!",
    "new_password": "NewPassword123!"
  }
  ```
- **Response**: `200 OK` with success message

## Content & Search Endpoints

### Search Videos
- **URL**: `/api/v1/search/`
- **Method**: `GET`
- **Description**: Search educational videos
- **Headers**: `Authorization: Bearer <access_token>`
- **Query Parameters**: `q=search_term`
- **Response**: `200 OK` with list of videos

### Mark Video as Watched
- **URL**: `/api/v1/progress/mark/`
- **Method**: `POST`
- **Description**: Mark video as watched
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "video_id": "youtube_video_id",
    "title": "Video Title",
    "thumbnail_url": "https://example.com/thumbnail.jpg",
    "channel_title": "Channel Name",
    "published_at": "2023-01-01T00:00:00Z"
  }
  ```
- **Response**: `201 Created` with video details

### Get Watch History
- **URL**: `/api/v1/progress/list/`
- **Method**: `GET`
- **Description**: Get user watch history
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with list of watched videos

### Submit Video Feedback
- **URL**: `/api/v1/feedback/`
- **Method**: `POST`
- **Description**: Submit feedback for a video
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "video_id": "youtube_video_id",
    "rating": 5,
    "comment": "Great educational content!",
    "helpful": true
  }
  ```
- **Response**: `201 Created` with feedback details

### Get Video Feedback
- **URL**: `/api/v1/feedback/{video_id}/`
- **Method**: `GET`
- **Description**: Get feedback for a specific video
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with feedback details

### Update Video Progress
- **URL**: `/api/v1/videos/{video_id}/progress/`
- **Method**: `PUT`
- **Description**: Update video progress
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "current_time": 120.5,
    "duration": 300.0,
    "percentage_watched": 40.0
  }
  ```
- **Response**: `200 OK` with updated progress

## Playlist Management Endpoints

### List User Playlists
- **URL**: `/api/v1/playlists/`
- **Method**: `GET`
- **Description**: List all playlists owned by user
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with list of playlists

### Create Playlist
- **URL**: `/api/v1/playlists/`
- **Method**: `POST`
- **Description**: Create a new playlist
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "name": "My Learning Path",
    "description": "Collection of educational videos"
  }
  ```
- **Response**: `201 Created` with playlist details

### Get Playlist Details
- **URL**: `/api/v1/playlists/{id}/`
- **Method**: `GET`
- **Description**: Get detailed playlist information
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with playlist and items

### Update Playlist
- **URL**: `/api/v1/playlists/{id}/`
- **Method**: `PUT`
- **Description**: Update playlist information
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "name": "Updated Name",
    "description": "Updated description"
  }
  ```
- **Response**: `200 OK` with updated playlist

### Delete Playlist
- **URL**: `/api/v1/playlists/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a playlist
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `204 No Content`

### Add Video to Playlist
- **URL**: `/api/v1/playlists/{id}/items/`
- **Method**: `POST`
- **Description**: Add video to playlist
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "video_id": "youtube_video_id",
    "title": "Video Title",
    "thumbnail_url": "https://example.com/thumbnail.jpg",
    "channel_title": "Channel Name"
  }
  ```
- **Response**: `201 Created` with playlist item details

### Remove Video from Playlist
- **URL**: `/api/v1/playlists/{id}/items/{item_id}/`
- **Method**: `DELETE`
- **Description**: Remove video from playlist
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `204 No Content`

### Reorder Playlist Items
- **URL**: `/api/v1/playlists/{id}/reorder-items/`
- **Method**: `PATCH`
- **Description**: Reorder videos within playlist
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "item_ids": [
      "item_id_3",
      "item_id_1",
      "item_id_2"
    ]
  }
  ```
- **Response**: `200 OK` with updated order

### Share Playlist
- **URL**: `/api/v1/playlists/{id}/share/`
- **Method**: `POST`
- **Description**: Share playlist with another user
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "email": "friend@example.com"
  }
  ```
- **Response**: `200 OK` with confirmation

### Make Playlist Public
- **URL**: `/api/v1/playlists/{id}/make_public/`
- **Method**: `POST`
- **Description**: Make playlist publicly accessible
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` with updated playlist
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
