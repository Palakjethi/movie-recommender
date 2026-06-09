import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML model
print("Loading ML model...")
with open("recommender_model.pkl", "rb") as f:
    model = pickle.load(f)

cosine_sim = model["cosine_sim"]
indices    = model["indices"]
df         = model["df"]
print("Model loaded! Server ready.")

# Endpoint 1 — Recommend similar movies
@app.get("/recommend")
def recommend(title: str, n: int = 10):
    if title not in indices:
        return {"error": f"Movie '{title}' not found"}
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
    movie_indices = [i[0] for i in sim_scores]
    
    results = df.iloc[movie_indices][["title", "genres", 
                "vote_average", "year", "poster_url"]].copy()
    results["similarity"] = [round(i[1], 3) for i in sim_scores]
    
    return results.to_dict(orient="records")

# Endpoint 2 — Get popular movies
@app.get("/movies/popular")
def get_popular():
    popular = df[df["category"] == "now_playing"]\
              .sort_values("vote_average", ascending=False)\
              .head(20)
    return popular[["title", "genres", "vote_average", 
                    "year", "poster_url"]].to_dict(orient="records")

# Endpoint 3 — Get upcoming movies
@app.get("/movies/upcoming")
def get_upcoming():
    upcoming = df[df["category"] == "upcoming"]\
               .sort_values("release_date", ascending=True)\
               .head(20)
    return upcoming[["title", "genres", "vote_average",
                     "year", "poster_url"]].to_dict(orient="records")

# Endpoint 4 — Search movies by title
@app.get("/search")
def search(q: str):
    results = df[df["title"].str.contains(q, case=False, na=False)]
    return results[["title", "genres", "vote_average",
                    "year", "poster_url"]].head(10).to_dict(orient="records")