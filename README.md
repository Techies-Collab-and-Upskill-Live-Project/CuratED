# 📚 CuratEd

Turn YouTube into your personal study partner.  
Discover curated educational video paths, organize learning playlists, and grow smarter — not harder.

---

## 🚀 Project Overview

**CuratEd** helps users search educational topics, discover curated YouTube video playlists, and engage in meaningful community discussions around learning.

We are building a fast, intuitive web app where users can:
- Search educational topics
- Find high-quality, structured YouTube video paths
- Save and build personal learning playlists
- Discuss videos, learning paths, and growth tips with the community

---

## 🧠 Project Goals

- Eliminate distraction and decision fatigue from endless YouTube recommendations
- Make structured self-learning accessible to everyone
- Encourage intentional learning through curated playlists and community-driven discussions
- Build a fun, inspiring place for self-education

---

## 🛠️ Tech Stack

- **Frontend:** React.js + TailwindCSS
- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL (Railway or Supabase)
- **Authentication:** Supabase Auth or Django AllAuth
- **Deployment:** Railway or Render
- **APIs:** YouTube Data API v3

---

## ✨ MVP Key Features

- Smart keyword-based YouTube search
- Organized, curated video result lists
- Custom Playlist Builder (save and manage videos)
- Contextual filtering (topic relevance, freshness)
- Community threads/comment sections around videos/playlists
- Basic authentication system (sign up, login, manage profile)

---

## 📈 Functional Requirements (MVP)

| Feature | Functional Requirement |
|--------|-------------------------|
| Keyword Search | Users search for learning topics |
| Video Fetch | System fetches and structures YouTube videos |
| Playlist Saving | Users create personal playlists |
| Commenting | Users discuss videos/playlists |
| Authentication | Basic email login system |
| Progress Tracker | Mark videos as watched |

---

## 📍 User Journeys

1. **Finding Educational Content:**  
User searches → Views structured videos → Watches and marks progress → Joins discussion.

2. **Building Playlists:**  
User saves videos → Organizes into custom playlists → Shares or discusses playlists.

---

## 🔥 Technical Considerations

- **Web-only platform** for MVP (desktop + responsive mobile)
- **YouTube embed only** (no hosting videos)
- **Caching or optimizing API usage** due to YouTube quota
- **Simple, fast UI** optimized for speed and clarity
- **Database scalable** for playlists, users, and discussions

---

## 🛠️ Local Development Setup

```bash
# Clone the repo
git clone https://github.com/your-username/curated.git
cd curated
```

### Backend Setup
```bash
cd backend
python -m venv env
source env/bin/activate  # or .\\env\\Scripts\\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🤝 Contribution Guidelines

- Fork this repo
- Create a new branch
- Submit a clear pull request describing changes

---

## ⚖️ License

Licensed under the MIT License.

---

## 🙏 Acknowledgments

Thanks to the entire TCU Team 1 for the brainstorming, leadership, design, development, and shared vision behind **CuratEd** ❤️

---

# 🎯 Let’s curate learning. Let’s build CuratEd.


