import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API = "https://movie-recommender-9ykt.onrender.com";

function MovieCard({ movie, onClick }) {
  return (
    <div className="movie-card" onClick={onClick}>
      <img
        src={movie.poster_url}
        alt={movie.title}
        onError={(e) =>
          (e.target.src =
            "https://via.placeholder.com/200x300?text=No+Image")
        }
      />
      <div className="movie-card-title">{movie.title}</div>
      <div className="movie-card-overlay">
        <h3>{movie.title}</h3>
        <p>{movie.genres}</p>
        <span>⭐ {movie.vote_average?.toFixed(1)} · {movie.year}</span>
      </div>
    </div>
  );
}

function App() {
  const [popular, setPopular] = useState([]);
  const [upcoming, setUpcoming] = useState([]);
  const [recommendations, setRecs] = useState([]);
  const [searchQuery, setSearch] = useState("");
  const [searchResults, setResults] = useState([]);
  const [selectedMovie, setSelected] = useState("");
  const [loading, setLoading] = useState(false);
  const [bgPosters, setBgPosters] = useState([]);
  const [activeNav, setActiveNav] = useState("home");
  const [bgIndex, setBgIndex] = useState(0);

  useEffect(() => {
    axios.get(`${API}/movies/popular`).then((r) => {
      setPopular(r.data);
      setBgPosters(r.data.slice(0, 8).map((m) => m.poster_url));
    });
    axios.get(`${API}/movies/upcoming`).then((r) => setUpcoming(r.data));
  }, []);

  // Rotate background poster
  useEffect(() => {
    if (bgPosters.length === 0) return;
    const interval = setInterval(() => {
      setBgIndex((prev) => (prev + 1) % bgPosters.length);
    }, 4000);
    return () => clearInterval(interval);
  }, [bgPosters]);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    const r = await axios.get(`${API}/search?q=${searchQuery}`);
    setResults(r.data);
    setRecs([]);
    setActiveNav("home");
  };

  const handleRecommend = async (title) => {
    setLoading(true);
    setSelected(title);
    setResults([]);
    setActiveNav("home");
    window.scrollTo({ top: 0, behavior: "smooth" });
    const r = await axios.get(
      `${API}/recommend?title=${encodeURIComponent(title)}`
    );
    setRecs(r.data);
    setLoading(false);
  };

  const showPopular = () => {
    setActiveNav("popular");
    setRecs([]);
    setResults([]);
    setSelected("");
  };

  const showUpcoming = () => {
    setActiveNav("upcoming");
    setRecs([]);
    setResults([]);
    setSelected("");
  };

  return (
    <div className="app">
      {/* Animated background */}
      <div className="bg-container">
        {bgPosters.map((url, i) => (
          <div
            key={i}
            className={`bg-slide ${i === bgIndex ? "active" : ""}`}
            style={{ backgroundImage: `url(${url})` }}
          />
        ))}
        <div className="bg-overlay" />
      </div>

      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-logo">🎬 MovieAI</div>
        <div className="navbar-links">
          <button
            className={activeNav === "home" ? "nav-link active" : "nav-link"}
            onClick={() => { setActiveNav("home"); setRecs([]); setResults([]); setSelected(""); }}
          >
            Home
          </button>
          <button
            className={activeNav === "popular" ? "nav-link active" : "nav-link"}
            onClick={showPopular}
          >
            Popular
          </button>
          <button
            className={activeNav === "upcoming" ? "nav-link active" : "nav-link"}
            onClick={showUpcoming}
          >
            Upcoming
          </button>
        </div>
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search movies..."
            value={searchQuery}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
          />
          <button onClick={handleSearch}>🔍</button>
        </div>
      </nav>

      {/* Hero Section */}
      {activeNav === "home" && !searchResults.length && !recommendations.length && (
        <div className="hero">
          <div className="hero-content">
            <p className="hero-eyebrow">AI-Powered Discovery</p>
            <h1 className="hero-title">Movie Recommendations</h1>
            <p className="hero-subtitle">
              Search any movie and our ML model finds what you'll love next
            </p>
            <div className="hero-search">
              <input
                type="text"
                placeholder="Try  &quot;Inception&quot; or &quot;The Godfather&quot;..."
                value={searchQuery}
                onChange={(e) => setSearch(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              />
              <button onClick={handleSearch}>Find Movies</button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="content">

        {/* Loading */}
        {loading && (
          <div className="loading-wrap">
            <div className="spinner" />
            <p>Finding movies similar to <strong>{selectedMovie}</strong>...</p>
          </div>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <section className="movie-section">
            <h2>
              Because you liked{" "}
              <span className="highlight">{selectedMovie}</span>
            </h2>
            <div className="movie-row">
              {recommendations.map((m) => (
                <MovieCard
                  key={m.title}
                  movie={m}
                  onClick={() => handleRecommend(m.title)}
                />
              ))}
            </div>
          </section>
        )}

        {/* Search Results */}
        {searchResults.length > 0 && (
          <section className="movie-section">
            <h2>Search Results</h2>
            <p className="section-sub">Click a movie to get AI recommendations</p>
            <div className="movie-row">
              {searchResults.map((m) => (
                <MovieCard
                  key={m.title}
                  movie={m}
                  onClick={() => handleRecommend(m.title)}
                />
              ))}
            </div>
          </section>
        )}

        {/* Popular Movies Page */}
        {activeNav === "popular" && (
          <section className="movie-section">
            <h2>🔥 Now Playing</h2>
            <div className="movie-grid">
              {popular.map((m) => (
                <MovieCard
                  key={m.title}
                  movie={m}
                  onClick={() => handleRecommend(m.title)}
                />
              ))}
            </div>
          </section>
        )}

        {/* Upcoming Movies Page */}
        {activeNav === "upcoming" && (
          <section className="movie-section">
            <h2>🚀 Upcoming Movies</h2>
            <div className="movie-grid">
              {upcoming.map((m) => (
                <MovieCard key={m.title} movie={m} />
              ))}
            </div>
          </section>
        )}

        {/* Home — rows */}
        {activeNav === "home" && !searchResults.length && !recommendations.length && (
          <>
            <section className="movie-section">
              <h2> Now Playing</h2>
              <div className="movie-row">
                {popular.map((m) => (
                  <MovieCard
                    key={m.title}
                    movie={m}
                    onClick={() => handleRecommend(m.title)}
                  />
                ))}
              </div>
            </section>
            <section className="movie-section">
              <h2> Upcoming Movies</h2>
              <div className="movie-row">
                {upcoming.map((m) => (
                  <MovieCard key={m.title} movie={m} />
                ))}
              </div>
            </section>
          </>
        )}
      </div>
    </div>
  );
}

export default App;