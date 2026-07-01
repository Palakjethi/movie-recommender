import requests, pandas as pd, pickle, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = os.environ.get("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def fetch_movies(category, pages=5):
    movies = []
    for page in range(1, pages + 1):
        r = requests.get(f"{BASE_URL}/movie/{category}?api_key={API_KEY}&page={page}")
        results = r.json().get("results", [])
        for m in results:
            m["category"] = category
        movies.extend(results)
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
        poster_path = m.get("poster_path", "")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
        release_date = m.get("release_date", "")
        year = release_date[:4] if release_date else ""
        rows.append({
            "id": m["id"],
            "title": m["title"],
            "poster_url": poster_url,
            "overview": m.get("overview", ""),
            "vote_average": m.get("vote_average", 0),
            "vote_count": m.get("vote_count", 0),
            "release_date": release_date,
            "year": year,
            "genres": genres,
            "cast": cast,
            "director": director,
            "soup": f"{genres} {cast} {director} {keywords}",
            "category": m.get("category", "")
        })
    except Exception as e:
        print(f"❌ Failed for movie {m['id']}: {e}")
        continue

print(f"Total rows fetched: {len(rows)}")  # ✅ rows exists here

df = pd.DataFrame(rows).drop_duplicates("title").reset_index(drop=True)  # ✅ create df FIRST

# ✅ NOW use df
print(f"DataFrame shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
if len(df) == 0:
    raise Exception("No movies fetched! Check TMDB API key and responses.")

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