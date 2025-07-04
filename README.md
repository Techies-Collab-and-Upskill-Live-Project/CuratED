# 🎓 CuratED: Educational Content Platform

CuratED is an educational content curation and learning management system designed to help users discover, organize, and track their learning journey using educational videos from YouTube.

## 🌟 Key Features

- **Smart Video Search**: Find educational content with advanced filtering and relevance ranking
- **Learning Playlists**: Create, share, and organize educational content in custom playlists
- **Progress Tracking**: Track video watch history and completion status
- **Feedback System**: Rate and comment on educational videos
- **Secure Authentication**: Email verification, OTP authentication, and password management

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2 + Django REST Framework
- **Authentication**: JWT with token rotation (Simple JWT)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Caching**: Redis for production, Local Memory Cache for development
- **API Documentation**: Swagger/OpenAPI (drf-yasg)
- **Email**: SMTP with Gmail integration
- **External APIs**: YouTube Data API v3

### Core Libraries
- **django-cors-headers**: Cross-Origin Resource Sharing
- **python-decouple**: Environment configuration
- **Pillow**: Image processing
- **django-redis**: Redis cache integration
- **psycopg2**: PostgreSQL adapter
- **requests**: HTTP library for API calls
- **whitenoise**: Static file serving

## 🏗️ System Architecture

### Component Organization
- **accounts/**: User authentication, registration, password management
- **api/**: YouTube integration, video search, history tracking
- **playlists/**: Playlist CRUD, sharing, item management
- **backend/**: Core settings and configuration
- **templates/**: Email templates for auth flows

### Data Models Overview
- **CustomUser**: Email-based authentication with OTP support
- **Playlist**: User-created collections of educational videos
- **PlaylistItem**: Videos within playlists with ordering support
- **WatchedVideo**: User watch history
- **VideoProgress**: Tracking view progress of videos
- **VideoFeedback**: User ratings and comments

## 🚀 Installation Guide

### Prerequisites
- Python 3.11+
- pip and virtualenv
- YouTube API Key
- Gmail account (for email notifications)
- PostgreSQL (for production)
- Redis (optional, for production caching)

### Development Setup
1. **Clone & Setup Virtual Environment**
```bash
git clone https://github.com/Techies-Collab-and-Upskill-Live-Project/CuratED.git
cd CuratED
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
cp .env.example .env
# Generate a secure key with: python keygen.py
# Add your YouTube API key and other settings to .env
```

3. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. **Run Development Server**
```bash
python manage.py runserver
```

## 📚 Core Functionality

### Authentication System
- **Registration**: Email-based with OTP verification
- **Login**: JWT token authentication
- **Password Management**: Reset and change workflows
- **Token Security**: Rotation, blacklisting, and short expiry

### Video Search & Recommendation
- **Smart Search**: Educational content filtering
- **Relevance Ranking**: Algorithm to prioritize educational videos
- **Metadata Enhancement**: Video duration, engagement metrics
- **Caching**: Performance optimization for repeated searches

### Playlist Management
- **Creation & Organization**: Personal collections of videos
- **Video Management**: Add, remove, reorder
- **Sharing**: Share with other users or make public
- **Access Control**: Private, shared, or public status

### Learning Progress
- **Watch History**: Track viewed videos
- **Progress Tracking**: Current position in videos
- **Completion Status**: Calculate watch percentage

## 🔑 API Reference

Detailed API documentation is available via Swagger UI at `/swagger/` or ReDoc at `/redoc/` when running the server.

### Authentication Endpoints
```http
POST /api/v1/users/register/             # Register new user
POST /api/v1/users/verify-otp/           # Verify email with OTP
POST /api/v1/users/resend-verification/  # Resend OTP
POST /api/v1/login/                      # Obtain JWT tokens
POST /api/v1/token/refresh/              # Refresh access token
POST /api/v1/users/password-reset/       # Request password reset
POST /api/v1/users/password-reset/confirm/ # Confirm password reset
PUT  /api/v1/users/password/change/      # Change password (authenticated)
```

### Content & Search Endpoints
```http
GET  /api/v1/search/                     # Search educational videos
POST /api/v1/progress/mark/              # Mark video as watched
GET  /api/v1/progress/list/              # Get watch history
POST /api/v1/feedback/                   # Submit video feedback
GET  /api/v1/feedback/{video_id}/        # Get video feedback
PUT  /api/v1/videos/{video_id}/progress/ # Update video progress
```

### Playlist Management Endpoints
```http
GET    /api/v1/playlists/                # List user playlists
POST   /api/v1/playlists/                # Create playlist
GET    /api/v1/playlists/{id}/           # Get playlist details
PUT    /api/v1/playlists/{id}/           # Update playlist
DELETE /api/v1/playlists/{id}/           # Delete playlist
POST   /api/v1/playlists/{id}/items/     # Add video to playlist
DELETE /api/v1/playlists/{id}/items/{item_id}/ # Remove video from playlist
PATCH  /api/v1/playlists/{id}/reorder-items/ # Reorder playlist items
POST   /api/v1/playlists/{id}/share/     # Share playlist with user
POST   /api/v1/playlists/{id}/make_public/ # Make playlist public
```

## 📊 Environment Variables

The following environment variables are required in your `.env` file:

```
# Security
SECRET_KEY=your_secret_key_here

# Debug
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME

# Redis
REDIS_URL=redis://:PASSWORD@HOST:PORT/0

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password

# YouTube API
YOUTUBE_API_KEY=your_youtube_api_key_here
```

## 🧪 Testing

The project includes comprehensive test suites:

```bash
# Run all tests
python manage.py test

# Run specific test categories
python manage.py test accounts
python manage.py test api
python manage.py test playlists

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔧 Development Guidelines

### Code Organization
- **Models**: Define data structures
- **Serializers**: Handle data validation and conversion
- **Views**: Implement API endpoints
- **URLs**: Define routing

### Best Practices
- Create thorough tests for new features
- Use meaningful docstrings and comments
- Follow PEP 8 style guidelines
- Validate all user input with serializers
- Implement proper error handling
- Use descriptive commit messages

### Common Tasks
- **Adding a new endpoint**: Create serializer, view, and add to urls.py
- **Model changes**: Make migrations with `python manage.py makemigrations`
- **Schema updates**: API docs auto-update from DRF views

## 🚢 Deployment

### Production Considerations
- Use PostgreSQL for the database
- Enable Redis for caching
- Set DEBUG=False in production
- Use a proper WSGI server (Gunicorn)
- Set up proper static file serving
- Configure proper email backend
- Set strong SECRET_KEY
- Review and tighten CORS settings

### Security Features
- JWT with short lifetimes
- Token rotation and blacklisting
- Rate limiting to prevent abuse
- Email verification for registration
- Password complexity requirements
- CORS protection

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

This project is maintained by the CuratED team as part of the Techies Collab and Upskill Live Project initiative.
