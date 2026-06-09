import requests, pandas as pd, pickle, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = os.environ.get("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies(category, pages=5):
    movies = []
    for page in range(1, pages + 1):
        r = requests.get(f"{BASE_URL}/movie/{category}?api_key={API_KEY}&page={page}")
        movies.extend(r.json().get("results", []))
    return movies

all_movies = (
    fetch_movies("top_rated", 20) +
    fetch_movies("now_playing", 5) +
    fetch_movies("upcoming", 5)
)

seen, unique = set(), []
for m in all_movies:
    if m["id"] not in seen:
        seen.add(m["id"])
        unique.append(m)

def get_details(movie_id):
    r = requests.get(f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,keywords")
    d = r.json()
    genres = " ".join([g["name"] for g in d.get("genres", [])])
    cast = " ".join([c["name"] for c in d.get("credits", {}).get("cast", [])[:5]])
    director = next((c["name"] for c in d.get("credits", {}).get("crew", []) if c["job"] == "Director"), "")
    keywords = " ".join([k["name"] for k in d.get("keywords", {}).get("keywords", [])])
    return genres, cast, director, keywords

rows = []
for m in unique:
    try:
        genres, cast, director, keywords = get_details(m["id"])
        rows.append({
            "id": m["id"], "title": m["title"],
            "poster_path": m.get("poster_path", ""),
            "overview": m.get("overview", ""),
            "vote_average": m.get("vote_average", 0),
            "soup": f"{genres} {cast} {director} {keywords}"
        })
    except:
        continue

df = pd.DataFrame(rows).drop_duplicates("title").reset_index(drop=True)
df.to_csv("movies.csv", index=False)

tfidf = TfidfVectorizer(stop_words="english")
matrix = tfidf.fit_transform(df["soup"])
sim = cosine_similarity(matrix)
indices = pd.Series(df.index, index=df["title"]).drop_duplicates()
pickle.dump({
    "df": df,
    "cosine_sim": sim,
    "indices": indices
}, open("recommender_model.pkl", "wb"))
print(f"✅ Built model with {len(df)} movies")