# 🛠 CuratEd Backend - README

Welcome to the backend service for **CuratEd** — the structured YouTube learning platform!
This README has been updated to reflect a leaner MVP scope focused on delivering fast, distraction-free video discovery using YouTube.

---

## 🚀 MVP Scope (Simplified)

For the MVP, our core mission is to:

> Help users quickly find relevant YouTube educational content through keyword search and track their learning progress.

We’re prioritizing **speed, clarity, and simplicity**. Additional features (playlists, community, blogs, mentorship) will be explored post-MVP.

---

## 🛠 Tech Stack

- **Backend Framework:** Django + Django REST Framework
- **Database:** PostgreSQL (via Railway or Supabase)
- **Authentication:** Optional for MVP (can use session/local storage for now)
- **Deployment:** Railway or Render
- **External API:** YouTube Data API v3

---

## 📦 Project Setup (Step-by-Step)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/curated-backend.git
cd curated-backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv env
source env/bin/activate  # Windows: .\\env\\Scripts\\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

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

## 📂 Backend Folder Structure

```bash
curated-backend/
├── backend/
│   ├── settings.py
│   ├── urls.py
├── api/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── youtube.py
├── manage.py
└── .env
```

---

## 🔑 MVP Backend Features

### 1. YouTube Search
- **Endpoint:** `GET /api/search/?q=keyword`
- **Function:** Uses YouTube Data API v3 to return structured, relevant video content.

### 2. Mark Video as Watched
- **Endpoint:** `POST /api/progress/mark/`
- **Function:** Stores video ID and watched status (locally or per session for now).

### 3. Get Watched Videos
- **Endpoint:** `GET /api/progress/list/`
- **Function:** Returns a list of watched videos to track progress.

### (Optional)
- Save Video (basic bookmarking): `POST /api/save/`

---

## 🔁 Development Workflow

1. Pull latest changes:
```bash
git pull origin main
```
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```
3. Make changes locally and test
4. Commit and push:
```bash
git add .
git commit -m "Your message"
git push origin feature/your-feature-name
```
5. Open a PR on GitHub and request review

---

## 📊 Testing

Use Postman or browser:
- `GET /api/search/?q=learn+python` — get curated YouTube videos
- `POST /api/progress/mark/` — mark as watched
- `GET /api/progress/list/` — retrieve watched history

---

## 🙏 Acknowledgments

Thanks to everyone contributing to building **CuratEd** backend. We're building simple, purposeful tech to make learning easier.

---

# 🎯 Let’s stay lean, build smart, and deliver value — fast.

