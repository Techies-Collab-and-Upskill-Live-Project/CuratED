# 🔧 CuratEd Backend - README

Welcome to the backend service for **CuratEd** — the structured YouTube learning platform!
This README will guide you through everything we'll be doing step-by-step, from setup to development workflow.

---

## 🚀 Overview

The backend handles all the business logic, database interactions, and external API integrations for CuratEd. It is built using **Django** and **Django REST Framework**.

Key responsibilities include:
- Managing user authentication
- Handling YouTube API requests for search results
- Managing user playlists and video progress
- Enabling community comments and discussions

---

## 🛠️ Tech Stack

- **Backend Framework:** Django + Django REST Framework
- **Database:** PostgreSQL (using Railway or Supabase for deployment)
- **Authentication:** Supabase Auth (or Django AllAuth if needed)
- **Deployment:** Railway or Render
- **External API:** YouTube Data API v3

---

## 📈 Project Setup (Step-by-Step)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/curated-backend.git
cd curated-backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv env
source env/bin/activate  # For Windows: .\\env\\Scripts\\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Dependencies include:
- Django
- djangorestframework
- python-decouple
- psycopg2-binary
- requests (for YouTube API calls)
- corsheaders

### 4. Configure Environment Variables
Create a `.env` file in the root of `backend/`:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=your_postgresql_db_url
YOUTUBE_API_KEY=your_youtube_api_key
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```

---

## 📚 Backend Folder Structure

```bash
curated-backend/
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── youtube.py  # YouTube API Service
│   ├── comments.py  # Community Comments Logic
│   └── playlist.py  # Playlist Management Logic
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚒 Core APIs We Will Build

### User Authentication (if handled on backend)
- Register User
- Login User
- Logout User

### YouTube Search and Curation
- Search Videos by Keyword (calls YouTube Data API)
- Process and clean search results
- Return structured video data to frontend

### Playlist Management
- Create a playlist
- Add/remove videos from playlist
- Fetch user playlists
- Mark video as watched

### Community Engagement
- Add comments on videos or playlists
- View comments
- Like or reply to comments (future phase)

---

## 🔄 Development Workflow

1. Pull latest changes:
```bash
git pull origin main
```
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```
3. Make your changes.
4. Test your changes locally.
5. Commit and push:
```bash
git add .
git commit -m "Your detailed commit message"
git push origin feature/your-feature-name
```
6. Open a Pull Request and request a code review.

---

## 🛡️ Deployment

Once backend is working locally:
- Connect the GitHub repo to Railway or Render.
- Add environment variables on the deployment dashboard.
- Set automatic deployment from the `main` branch.

---

## 🛡️ Testing APIs

We will use **Postman** or **Insomnia** for API testing before integrating with frontend.

Test Cases:
- Search API: Returns correct videos
- Playlist API: CRUD works
- Comments API: Post and fetch comments
- Authentication: Register/login/logout flows

---

## 🙏 Acknowledgments

Thanks to everyone contributing to building **CuratEd** backend. Let's create a backend that makes structured learning easy, fast, and fun!

---

# 🎯 Let's build the heart of CuratEd — clean, scalable, and powerful!

