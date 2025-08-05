import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import base64
import plotly.graph_objs as go

# =============================
# 🎬 Cinematic Background
# =============================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                background-repeat: no-repeat;
                font-family: 'Poppins', sans-serif;
                color: #fff;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# =============================
# Data Loading & Preprocessing
# =============================
ratings = pd.read_csv("u.data", sep="\t", names=["userId", "movieId", "rating", "timestamp"])
movies = pd.read_csv("u.item", sep="|", encoding="latin-1", usecols=[0, 1], names=["movieId", "title"], header=None)
ratings = pd.merge(ratings, movies, on="movieId")
movies["genres"] = movies["title"].apply(lambda x: "movie")  # dummy genres, replace if you have better info

# =============================
# Hybrid Content Similarity (memory-optimized)
# =============================
@st.cache_resource(show_spinner=False)
def compute_similarity():
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies["genres"])
    return cosine_similarity(tfidf_matrix)

similarity = compute_similarity()

# =============================
# 🎨 Glassmorphism & Gradient CSS
# =============================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');
    .glass {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 18px;
        box-shadow: 0 8px 32px 0 rgba(31,38,135,0.37);
        border: 1.5px solid rgba(255,255,255,0.18);
        padding: 1.1rem;
        margin-bottom: 1.2rem;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(90deg, #dd2476, #ff512f, #923cb5, #0000ff);
        color: white;
        border: none;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.6rem 2rem;
        transition: box-shadow 0.2s, transform 0.2s;
        box-shadow: 0 0 14px #9210c6;
        letter-spacing: 0.02em;
    }
    .stButton>button:hover {
        box-shadow: 0 0 24px #ff005e, 0 0 18px #2929fa;
        transform: scale(1.04);
    }
    div[data-baseweb="slider"] {
        background: linear-gradient(87deg, #ff512f, #923cb5, #0000ff);
        border-radius: 15px;
        padding: 0.3rem;
        margin-bottom: 1.5rem;
    }
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        text-align: center;
        color: #fff;
        text-shadow: 0 0 16px #ff005e, 0 0 18px #2929fa;
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from {text-shadow:0 0 6px #dd2476,0 0 10px #dd2476;}
        to {text-shadow:0 0 16px #2000ff, 0 0 24px #ff005e;}
    }
    .rec-card {
        background: rgba(0,0,0,0.58);
        border-radius: 16px;
        padding: 1.1rem;
        margin-bottom: 1rem;
        transition: transform 0.3s, box-shadow 0.3s;
        color: white;
        box-shadow: 0 6px 14px rgba(80,20,130,0.44);
        cursor: pointer;
        animation: fadein 1.15s cubic-bezier(.22,1,.36,1) backwards;
        display: flex;
        align-items: center;
    }
    .rec-card:hover {
        transform: scale(1.055);
        box-shadow: 0 0 24px #922ff7, 0 0 20px #dd2476;
        background: rgba(60,60,84,0.22);
    }
    @keyframes fadein {
        from {opacity:0; transform:translateY(44px);}
        to {opacity:1; transform:translateY(0);}
    }
    .gradient-text {
        background: linear-gradient(90deg, #ff512f 0%, #dd2476 50%, #923cb5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .history-panel {
        max-height: 350px;
        overflow-y: auto;
        background: rgba(0,0,0,0.38);
        border-radius: 15px;
        padding: 1rem;
        color: white;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================
# 🎬 Main Layout & Inputs
# =============================
add_bg_from_local("mov_rec.jpg")

st.title("🎬 Movie Recommendation System")

if 'search_history' not in st.session_state:
    st.session_state['search_history'] = []

user_id = st.number_input("👤 Enter User ID", min_value=1, max_value=ratings["userId"].max(), step=1)
movie_title = st.selectbox("🎥 Select a Movie", movies["title"].values)
hybrid_weight = st.slider("⚖ Hybrid Weight (Content vs Collaborative)", 0.0, 1.0, 0.5)
submit = st.button("🚀 Get Recommendations")

# =============================
# 🔥 Recommendation Logic & Display
# =============================
if submit:
    # Content-based
    movie_index = movies[movies["title"] == movie_title].index[0]
    content_scores = list(enumerate(similarity[movie_index]))
    content_recommendations = sorted(content_scores, key=lambda x: x[1], reverse=True)[1:11]
    content_recs = [(movies.iloc[i]["title"], score * 1000) for i, score in content_recommendations]

    # Collaborative
    user_ratings = ratings[ratings["userId"] == user_id][["title", "rating"]]
    collab_scores = ratings.groupby("title")["rating"].mean().sort_values(ascending=False)
    collab_recs = [(title, score * 100) for title, score in collab_scores.items() if title not in user_ratings["title"].values]

    # Hybrid
    hybrid_recs = {}
    for movie, score in content_recs:
        hybrid_recs[movie] = hybrid_recs.get(movie, 0) + score * hybrid_weight
    for movie, score in collab_recs:
        hybrid_recs[movie] = hybrid_recs.get(movie, 0) + score * (1 - hybrid_weight)

    final_recs = sorted(hybrid_recs.items(), key=lambda x: x[1], reverse=True)[:5]
    st.session_state['search_history'].append({
        'user_id': user_id,
        'movie': movie_title,
        'hybrid_weight': hybrid_weight,
        'recommendations': final_recs
    })

    st.markdown(f"<h2 class='fade-in'>🔥 Top 5 Recommendations for User {user_id}</h2>", unsafe_allow_html=True)

    # Simply show recommendation cards (no images)
    for idx, (movie, score) in enumerate(final_recs):
        st.markdown(f"""
        <div class='rec-card'>
            <span class='gradient-text' style="font-size:1.09rem;">
            🎬 {movie}<br/>
            <span style='font-size:0.97rem;opacity:0.82;'>Score: {round(score,2)}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Animated Plotly bar chart for recommendation scores
    rec_names = [x[0] for x in final_recs]
    rec_scores = [x[1] for x in final_recs]
    fig = go.Figure(go.Bar(
        x=rec_names, y=rec_scores,
        marker=dict(
            color=['#ff512f', '#dd2476', '#923cb5', '#0000ff', '#220077'],
            line=dict(color='rgba(128,0,128,1.0)', width=2)
        ),
        text=[f'Score: {round(s,2)}' for s in rec_scores],
        textposition='auto'
    ))
    fig.update_traces(hovertemplate='%{x}<br>Score: %{y:.1f}')
    fig.update_layout(
        title='📊 Top 5 Recommendation Scores',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(title='Score'), xaxis=dict(tickangle=45),
        transition = {'duration': 650}
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # User's top 10 rated movies
    st.markdown(f"<h2 class='fade-in'>⭐ Top 10 Movies Rated by User {user_id}</h2>", unsafe_allow_html=True)
    user_history = ratings[ratings["userId"] == user_id].nlargest(10, "rating")
    hist_fig = go.Figure(go.Bar(
        y=user_history["title"].values, x=user_history["rating"].values, orientation='h',
        marker=dict(color='#923cb5', line=dict(color='#dd2476', width=2)),
        text=[f'Rating: {r}' for r in user_history["rating"]],
        textposition='auto'
    ))
    hist_fig.update_layout(
        title=f"User {user_id} Top 10 Rated Movies",
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'), xaxis=dict(title='Rating', range=[0, 5]),
        yaxis=dict(autorange='reversed'),
        transition = {'duration': 600}
    )
    st.plotly_chart(hist_fig, use_container_width=True, config={'displayModeBar': False})

# =============================
# 📜 Sidebar: Search History & Clear
# =============================
st.sidebar.markdown("<h2 class='gradient-text'>🔍 Search History</h2>", unsafe_allow_html=True)
if st.sidebar.button("❌ Clear History"):
    st.session_state['search_history'] = []

if st.session_state['search_history']:
    with st.sidebar.container():
        for entry in reversed(st.session_state['search_history']):
            user = entry['user_id']
            movie = entry['movie']
            weight = entry['hybrid_weight']
            recs = entry['recommendations']
            st.sidebar.markdown(f"<div class='glass fade-in'><b>User {user}</b><br>Movie: {movie}<br>Weight: {weight}<br>Recs:", unsafe_allow_html=True)
            for rec_movie, rec_score in recs:
                st.sidebar.markdown(f"- {rec_movie} ({round(rec_score,2)})", unsafe_allow_html=True)
            st.sidebar.markdown("</div>", unsafe_allow_html=True)

# =============================
# End of App
# =============================
