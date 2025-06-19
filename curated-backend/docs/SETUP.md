# CuratED Setup Guide

## Prerequisites
- Python 3.11+
- Redis (optional, for production caching)
- Gmail account (for email notifications)

## Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd curated-backend
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Copy `.env.example` to `.env` and configure:
```ini
SECRET_KEY=your_django_secret_key
DEBUG=True
YOUTUBE_API_KEY=your_youtube_api_key
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_APP_PASSWORD=your_gmail_app_password
```

5. **Database Setup**
```bash
python manage.py migrate
```

6. **Create Superuser**
```bash
python manage.py createsuperuser
```

## Development

### Running Tests
```bash
python manage.py test
```

### API Documentation
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

### Email Configuration
1. Enable 2FA in Gmail
2. Generate App Password
3. Use in EMAIL_HOST_APP_PASSWORD
