# CuratED Backend API

CuratED is an educational video platform that helps users discover, organize, and track their learning journey through curated YouTube content.

## 🚀 Tech Stack

- Django REST Framework
- JWT Authentication
- YouTube Data API v3
- SQLite (Development)
- Swagger/OpenAPI Documentation

## 📋 Prerequisites

- Python 3.11+
- pip
- YouTube API Key

## 🛠 Setup

1. **Clone the repository**
```bash
git clone https://github.com/Techies-Collab-and-Upskill-Live-Project/CuratED.git
cd curated-backend
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Setup**
```bash
cp .env.example .env
```
Update `.env` with your settings:
```
SECRET_KEY='your_django_secret_key'
DEBUG=True
YOUTUBE_API_KEY='your_youtube_api_key'
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. **Database Setup**
```bash
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Run Development Server**
```bash
python manage.py runserver
```

## 🔑 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Register
```http
POST /api/v1/users/register/
{
    "email": "user@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Login
```http
POST /api/v1/users/login/
{
    "email": "user@example.com",
    "password": "securepass123"
}
```

## 🎥 API Endpoints

### Search Videos
```http
GET /api/v1/search/?q=python+tutorial
```

### Watch History
```http
POST /api/v1/progress/mark/
{
    "video_id": "abc123",
    "title": "Learn Python",
    "description": "Tutorial...",
    "thumbnail": "https://...",
    "channel_title": "CodingChannel"
}
```

### Playlists
```http
POST /api/v1/playlists/
{
    "name": "Python Basics",
    "description": "Beginner Python tutorials"
}
```

### Add to Playlist
```http
POST /api/v1/playlists/{playlist_id}/items/
{
    "video_id": "abc123",
    "title": "Learn Python",
    "thumbnail_url": "https://...",
    "channel_title": "CodingChannel"
}
```

## 📝 API Documentation

Full API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run specific tests:
```bash
python manage.py test accounts.tests.AuthenticationTests
python manage.py test api.tests.YouTubeSearchTests
```

## 🔒 Security Features

- JWT Authentication
- Email Verification
- Password Reset Flow
- Rate Limiting
- Token Refresh/Blacklisting

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | Required |
| DEBUG | Debug mode | False |
| YOUTUBE_API_KEY | YouTube Data API key | Required |
| ALLOWED_HOSTS | Allowed hosts | * |

## 📁 Project Structure

```
curated-backend/
├── accounts/           # User authentication
├── api/               # Core API functionality
├── playlists/         # Playlist management
├── templates/         # Email templates
├── manage.py
└── requirements.txt
```

## 🤝 Contributing

1. Create a new branch (`git checkout -b feature/enhancement`)
2. Make changes
3. Run tests
4. Create pull request

## 📄 License

This project is licensed under the MIT License.
