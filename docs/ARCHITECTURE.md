# CuratED Architecture

## System Components

### Authentication (accounts/)
- Custom User model with email authentication
- JWT-based authentication
- OTP verification system
- Password reset functionality

### Content Management (api/)
- YouTube API integration
- Search result processing
- Watch history tracking
- Progress persistence
- Content filtering

### Playlist System (playlists/)
- Playlist CRUD operations
- Sharing functionality
- Access control 
- Video organization

## Data Models

### User Model
```python
class CustomUser:
    email          # Primary identifier
    is_active      # Email verification status
    otp           # Verification code
    otp_created   # OTP timestamp
```

### Video Progress
```python
class VideoProgress:
    user           # ForeignKey to User
    video_id      # YouTube video ID
    current_time  # Playback position
    duration      # Total video length
    percentage    # Watch percentage
```

### Playlist
```python
class Playlist:
    user        # Owner
    name        # Playlist name
    is_public   # Visibility
    shared_with # Many-to-many with User
```

## Security Features

1. **Authentication**
   - JWT with rotation
   - Token blacklisting
   - Rate limiting

2. **Data Protection**
   - Input validation
   - CORS configuration
   - API quotas

3. **Email Security**
   - OTP expiration
   - Secure reset links
   - Rate-limited verification
