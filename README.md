# 🎬 MovieAI — AI-Powered Movie Recommendation System

> A full-stack machine learning web app that recommends movies based on content similarity using TF-IDF and Cosine Similarity.

🌐 **Live Demo:** [movie-recommender-amber-mu.vercel.app](https://movie-recommender-amber-mu.vercel.app/)

---

## ✨ Features

- 🔍 **Search any movie** and get instant AI-powered recommendations
- 🎥 **Now Playing** — latest movies currently in theatres
- 🚀 **Upcoming Movies** — what's releasing soon
- 🖼️ **Netflix-style UI** with animated rotating poster backgrounds
- ⚡ **Click any movie** to get similar recommendations instantly

---

## 🧠 How It Works

1. Fetched **557 movies** from TMDB API (top rated, now playing, upcoming)
2. Built a **"soup"** of each movie's genres, cast, director, and keywords
3. Applied **TF-IDF Vectorization** to convert text into numerical vectors
4. Computed a **557×557 Cosine Similarity matrix** to find similar movies
5. FastAPI backend serves recommendations via REST API
6. React frontend displays results in a modern Netflix-style interface

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data | TMDB API |
| ML | TF-IDF + Cosine Similarity (scikit-learn) |
| Backend | FastAPI + Uvicorn (Python) |
| Frontend | React + Axios |
| Deployment | Render (backend) + Vercel (frontend) |

---

## 📁 Project Structure

```
Movie_Recommendation/
├── main.py                  ← FastAPI backend (4 endpoints)
├── build.py                 ← Fetches data & builds ML model on deploy
├── requirements.txt         ← Python dependencies
├── movies.csv               ← Dataset (auto-generated on deploy)
├── recommender_model.pkl    ← ML model (auto-generated on deploy)
├── movie_recomm.ipynb       ← Jupyter notebook (data exploration)
└── movie-frontend/
    ├── src/
    │   ├── App.js           ← React frontend
    │   └── App.css          ← Netflix-style CSS
    └── package.json
```

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommend?title=Inception` | Get ML recommendations |
| GET | `/movies/popular` | Now playing movies |
| GET | `/movies/upcoming` | Upcoming movies |
| GET | `/search?q=dark` | Search by title |

**Base URL:** `https://movie-recommender-9ykt.onrender.com`

---

## 🏃 Run Locally

### Backend
```bash
pip install -r requirements.txt
python build.py               # builds model (needs TMDB_API_KEY)
uvicorn main:app --reload     # runs on http://localhost:8000
```

### Frontend
```bash
cd movie-frontend
npm install
npm start                     # runs on http://localhost:3000
```

---

## 👩‍💻 About the Developer

**Palak Jethi**  
B.Tech CSE (AI & ML) — 3rd Year  

[![GitHub](https://img.shields.io/badge/GitHub-Palakjethi-black?style=flat&logo=github)](https://github.com/Palakjethi)

---

## 📸 Screenshots
### Home Page
<img width="1920" height="1080" alt="Screenshot (155)" src="https://github.com/user-attachments/assets/c78acbd4-a279-4dbd-a20c-47839fd81a58" />
### Search Results
<img width="1920" height="1080" alt="Screenshot (156)" src="https://github.com/user-attachments/assets/0381e726-a0ea-49cc-a9a9-568a46295c79" />
### Recommendations
<img width="1920" height="1080" alt="Screenshot (157)" src="https://github.com/user-attachments/assets/83d59ef4-8632-449f-af5c-d78ce4273cec" />



*Built with ❤️ using Python, React, and Machine Learning*
