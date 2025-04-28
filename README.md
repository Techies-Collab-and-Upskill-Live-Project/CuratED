# 📘 YouTube Study Coach

## 🧠 Overview
YouTube Study Coach is a platform designed to turn chaotic YouTube learning into a structured, effective, and goal-driven experience. Instead of endlessly scrolling through videos and playlists, users can now learn smarter by using our system to organize, track, and personalize their learning journey—powered by YouTube's existing content library.

This platform is particularly useful for students, self-learners, and professionals looking to gain mastery in specific topics, all while avoiding the stress of filtering through unrelated or low-quality videos.

---

## 🏗️ Scope of the MVP (Minimum Viable Product)

The MVP focuses on the core feature of transforming YouTube playlists into interactive study plans. This phase will include:

### 🎯 Features:
- Input field for users to paste a YouTube playlist URL.
- Extraction of all video titles and metadata from the playlist using YouTube Data API v3.
- Display of videos in an organized, step-by-step format.
- Progress tracking (check off completed videos).
- Clean, intuitive UI.

### 🚧 Current State:
- ❌ **Frontend UI** has been designed and implemented using React.
- ❌ **Styling** is not finalized yet.
- ❌ **API integration** (YouTube API & backend logic) is yet to be done.
- ❌ **Backend and database setup** using Django + DRF is pending.

The MVP provides a strong proof-of-concept and foundation for future features.

---

## 🏁 Final Product Scope

The final product aims to be a full-fledged learning assistant that combines curated YouTube content with structured course outlines, extra materials, and community support.

### 💡 Additional Features Planned:
- 🔍 **Search-based learning**: Users can search for a course (e.g. "Learn Python") and get a curated playlist + learning roadmap.
- 📚 **Course Outline Generation**: Auto-generate outlines from playlist content and metadata.
- 📝 **Additional Reading Materials**: Attach PDF guides, articles, and references to each lesson.
- 📊 **Progress Dashboards**: Visual progress tracking with analytics.
- 💬 **Learner Group Chats**: Real-time chat for each course or subject.
- 🧑‍🏫 **Mentorship System**: Request a mentor or volunteer to become one.
- 🧪 **Assignments/Quizzes**: Custom assignments and peer-reviewed projects.
- 💼 **Certificates of Completion**.
- 💻 **Admin Dashboard** for curating content, managing users, and reviewing submitted playlists.

---

## 🎯 Goal
To simplify and elevate the self-learning experience by:
- Reducing time spent finding high-quality resources.
- Creating structure from scattered YouTube content.
- Supporting community-driven learning.
- Making quality education accessible, without needing to create original video content.

---

## 🧱 Tech Stack

### Frontend:
- React.js (TypeScript)
- [Styling not finalized, likely Tailwind CSS]

### Backend:
- Django
- Django REST Framework (DRF)
- PostgreSQL (planned)

### APIs:
- YouTube Data API v3 (to fetch video data)
- Custom DRF endpoints for:
  - Playlist parsing
  - Progress storage

### Tools:
- GitHub for version control
- Railway / Render for deployment
- Figma for design prototyping

---

## 🚀 Procedures & Workflow

### ✅ MVP Workflow (Phase 1)

#### 👨‍🎓 Basic User Flow:
1. User pastes a YouTube playlist link.
2. Backend fetches video data using YouTube API.
3. Frontend displays videos in an ordered, clickable format.
4. User checks off videos as “Done.”
5. Progress saved locally or in a simple DB (if login exists).

### ⚙️ Phase 2 (Post-MVP Enhancements):
- Add user authentication.
- Store progress in database per user.
- Start building a minimal admin panel for content curation.

### 🧑‍🏫 Future Feature Workflow (Phase 3):
- Allow users to register for structured courses.
- Add mentorship matching and live chat.
- Introduce quizzes and certification.

---

## 📌 Contribution Guidelines

We welcome contributions! To collaborate:
1. Fork the repository.
2. Clone it locally.
3. Create a feature branch.
4. Commit your changes.
5. Open a pull request with clear documentation of what you changed.

---

## 📅 Roadmap

- [x] Build homepage UI
- [ ] Integrate YouTube API
- [ ] Parse playlist metadata and organize content
- [ ] Implement progress tracking (local/DB)
- [ ] Add backend and database
- [ ] Enable login/account system
- [ ] Curated course search & registration
- [ ] Chat and mentorship features
- [ ] Assignments and certification

---

## 🧑‍💻 Authors & Credits
- **[Your Name]** – Project Lead & Frontend Developer
- Special thanks to the team for brainstorming, UI ideas, and future planning.

---

## ⚖️ License
This project is licensed under the MIT License.

---

## 🙏 Acknowledgments
- YouTube for providing public APIs.
- React and TailwindCSS communities.
- All learners and educators who inspire structured self-education.

---

Let’s build a smarter, more structured way to learn from the content that’s already out there.

