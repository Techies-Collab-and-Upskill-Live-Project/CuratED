# 🎓 CuratED Backend API

Educational content curation and learning management system powered by Django REST Framework.

## 🛠️ Technology Stack

- **Framework:** Django 5.2 + Django REST Framework
- **Authentication:** JWT (Simple JWT)
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **API Documentation:** Swagger/OpenAPI (drf-yasg)
- **External APIs:** YouTube Data API v3
- **Email:** SMTP (Production) / Console (Development)

## 🚀 Quick Start

1. **Clone & Setup Virtual Environment**
```bash
git clone https://github.com/Techies-Collab-and-Upskill-Live-Project/CuratED.git
cd curated-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

2. **Environment Setup**
```bash
cp .env.example .env
# Update .env with your credentials:
# - SECRET_KEY
# - YOUTUBE_API_KEY
# - DEBUG
# - ALLOWED_HOSTS
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

## 📚 API Documentation

### Authentication Endpoints

```http
POST /api/v1/users/register/
POST /api/v1/users/login/
POST /api/v1/users/verify-otp/
POST /api/v1/users/password-reset/
POST /api/v1/token/refresh/
```

### Content Endpoints

```http
GET    /api/v1/search/                    # Search educational videos
POST   /api/v1/progress/mark/             # Mark video as watched
GET    /api/v1/progress/list/             # Get watch history
POST   /api/v1/feedback/                  # Create video feedback
GET    /api/v1/feedback/{video_id}/       # Get video feedback
```

### Playlist Management

```http
GET    /api/v1/playlists/                # List user playlists
POST   /api/v1/playlists/                # Create playlist
GET    /api/v1/playlists/{id}/           # Get playlist details
POST   /api/v1/playlists/{id}/items/     # Add video to playlist
PATCH  /api/v1/playlists/{id}/reorder/   # Reorder playlist items
```

## 🔒 Security Features

- JWT Authentication with refresh tokens
- Email verification (OTP)
- Password reset flow
- Rate limiting
- Custom password validation
- Token blacklisting

## 📁 Project Structure

```
curated-backend/
├── accounts/           # User authentication & management
├── api/               # Core API functionality & YouTube integration
├── playlists/         # Playlist management
├── templates/         # Email templates
├── manage.py
└── requirements.txt
```

## ⚙️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Django secret key | Yes |
| YOUTUBE_API_KEY | YouTube Data API key | Yes |
| DEBUG | Debug mode | No (default: False) |
| ALLOWED_HOSTS | Allowed hosts | No (default: *) |
| EMAIL_HOST | SMTP host | Production only |
| EMAIL_PORT | SMTP port | Production only |

## 🧪 Testing

Run all tests:
```bash
python manage.py test
```

Run specific tests:
```bash
python manage.py test accounts.tests.AuthenticationTests
python manage.py test api.tests.YouTubeSearchTests
python manage.py test playlists.tests.PlaylistManagementTests
```

## 📈 API Rate Limits

- Anonymous: 100 requests/day
- Authenticated: 1000 requests/day
- Login attempts: 5/minute

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.
