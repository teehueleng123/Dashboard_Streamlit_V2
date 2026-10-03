# ==============================================================================
# COURSE CODE    : UECS3183
# COURSE TITLE   : Data Visualisation Techniques
# ASSIGNMENT     : Assignment 2 (Interactive Dashboard)
# STUDENT NAME   : Tee Hue Leng
# STUDENT ID     : 2206851
# PROGRAMME      : Bachelor of Software Engineering (SE)
#
# INSTRUCTIONS ON HOW TO GENERATE & RUN THE DASHBOARD:
# 1. Install the required Python packages using:
#    pip install streamlit plotly pandas numpy statsmodels
#
# 2. Ensure 'Rotten Tomatoes Movies.csv' is located in the same directory.
#
# 3. In your terminal/command prompt, execute:
#    streamlit run app.py
#
# 4. The interactive dashboard will automatically open in your default browser at:
#    http://localhost:8501
# ==============================================================================

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION & REFINED UI STYLING
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Cinematic Intelligence | Rotten Tomatoes",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Polished High-Contrast Colorful Theme (Fixed tab padding and clean top-accent line to prevent text crowding)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    :root {
        --bg: #101522;
        --surface: #181d2d;
        --surface-2: #20273a;
        --surface-3: #29324a;
        --border: rgba(255,255,255,0.11);
        --border-strong: rgba(255,255,255,0.19);
        --text: #fffaf5;
        --muted: #b9bfd0;
        --muted-2: #858da3;

        --tomato: #ff5b61;
        --coral: #ff7a59;
        --gold: #ffc857;
        --pink: #ff65a3;
        --purple: #9b7cff;
        --cyan: #48d9e8;
        --green: #67d59a;
        --blue: #5fa8ff;

        --tomato-soft: rgba(255,91,97,0.16);
        --gold-soft: rgba(255,200,87,0.15);
        --radius: 18px;
    }

    * { box-sizing: border-box; }

    header[data-testid="stHeader"],
    .stApp > header,
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"] {
        display: none !important;
    }

    html, body, .stApp {
        background:
            radial-gradient(circle at 4% 5%, rgba(255,91,97,0.24), transparent 28%),
            radial-gradient(circle at 94% 8%, rgba(155,124,255,0.22), transparent 30%),
            radial-gradient(circle at 75% 78%, rgba(72,217,232,0.12), transparent 28%),
            radial-gradient(circle at 25% 92%, rgba(255,101,163,0.10), transparent 25%),
            var(--bg) !important;
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }

    .main, div[data-testid="stAppViewContainer"],
    .stAppViewBlockContainer {
        background: transparent !important;
    }

    .main .block-container,
    div[data-testid="stAppViewContainer"] > section.main > div.block-container {
        max-width: 1480px !important;
        padding: 2.2rem 2.5rem 4rem !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(18,20,24,0.98) !important;
        border-right: 1px solid var(--border) !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 2rem 1.35rem 3rem !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #d8dbe0 !important;
        font-weight: 500 !important;
    }

    /* Editorial hero */
    .hero-banner {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(135deg, rgba(34,38,61,0.98), rgba(21,25,42,0.98));
        border: 1px solid var(--border-strong);
        border-radius: 24px;
        padding: 42px 46px 38px;
        margin-bottom: 26px;
        box-shadow: 0 24px 70px rgba(0,0,0,0.28);
    }

    .hero-banner:after {
        content: "";
        position: absolute;
        right: -90px;
        top: -120px;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(255,91,97,0.22), rgba(155,124,255,0.18));
        filter: blur(4px);
    }

    .hero-eyebrow {
        color: var(--tomato);
        font-size: 0.70rem;
        font-weight: 700;
        letter-spacing: 2.2px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .hero-title {
        font-family: 'Playfair Display', serif !important;
        font-size: clamp(2.2rem, 4vw, 3.5rem);
        line-height: 1.05;
        letter-spacing: -1.4px;
        color: #fffaf2 !important;
        margin: 0 0 14px;
    }

    .hero-subtitle {
        max-width: 900px;
        color: #bfc2c8 !important;
        font-size: 0.98rem;
        line-height: 1.75;
        margin: 0 0 22px;
    }

    .badge-container { display:flex; flex-wrap:wrap; gap:8px; }

    .pill-badge {
        display:inline-flex;
        align-items:center;
        padding:7px 12px;
        border-radius:999px;
        background:rgba(255,255,255,0.045);
        border:1px solid var(--border);
        color:#d7d9dd;
        font-size:0.72rem;
        font-weight:600;
    }

    /* KPI cards */
    .kpi-card {
        position:relative;
        height:100%;
        background:linear-gradient(145deg, rgba(34,39,61,0.98), rgba(24,29,46,0.98));
        border:1px solid var(--border);
        border-radius:16px;
        padding:20px 21px;
        box-shadow:0 12px 32px rgba(0,0,0,0.20);
        transition:transform .2s ease, border-color .2s ease;
        overflow:hidden;
    }

    .kpi-card:hover {
        transform:translateY(-3px);
        border-color:rgba(255,90,79,0.45);
    }

    .kpi-card-glow {
        position:absolute;
        left:0; right:0; top:0;
        height:2px;
        background:linear-gradient(90deg, var(--tomato), var(--pink), var(--purple)) !important;
    }

    .kpi-label {
        color:#858a94 !important;
        font-size:0.67rem;
        letter-spacing:1.2px;
        text-transform:uppercase;
        font-weight:700;
        margin-bottom:9px;
    }

    .kpi-val {
        color:#fffaf2 !important;
        font-size:1.85rem;
        line-height:1.15;
        font-weight:700;
        margin:0;
    }

    .kpi-sub { color:#858a94 !important; font-size:0.75rem; margin-top:7px; }

    /* Narrative blocks */
    .story-callout {
        background:var(--surface);
        border:1px solid var(--border);
        border-left:3px solid var(--gold);
        border-radius:0 14px 14px 0;
        padding:17px 20px;
        margin:4px 0 26px;
        color:#c9ccd1 !important;
        font-size:0.90rem;
        line-height:1.7;
    }

    .story-callout b { color:#fff3df !important; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap:5px;
        background:transparent;
        border-bottom:1px solid var(--border);
        padding:0;
        margin:8px 0 28px;
        overflow-x:auto;
    }

    .stTabs [data-baseweb="tab"] {
        background:transparent;
        border:none !important;
        border-bottom:2px solid transparent !important;
        border-radius:0;
        padding:13px 16px !important;
        color:#858a94 !important;
        font-size:0.84rem;
        font-weight:600;
        white-space:nowrap;
        transition:all .2s ease;
    }

    .stTabs [data-baseweb="tab"]:hover { color:#fff !important; }

    .stTabs [aria-selected="true"] {
        color:#fffaf2 !important;
        border-bottom:2px solid var(--tomato) !important;
        background:transparent !important;
        box-shadow:none !important;
    }

    /* Controls */
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"],
    div[data-baseweb="input"] {
        background:#17191e !important;
        border-color:var(--border-strong) !important;
        border-radius:10px !important;
    }

    div[data-baseweb="select"] div,
    div[data-baseweb="base-input"] input {
        color:#e9e7e1 !important;
        font-weight:500 !important;
    }

    span[data-baseweb="tag"] {
        background:var(--tomato-soft) !important;
        border:1px solid rgba(255,90,79,0.30) !important;
        border-radius:7px !important;
    }

    span[data-baseweb="tag"] span { color:#ffe5df !important; }

    div[data-baseweb="slider"] div[role="slider"] {
        background:linear-gradient(90deg, var(--tomato), var(--pink), var(--purple)) !important;
        border-color:var(--tomato) !important;
    }

    /* Chart surfaces */
    div[data-testid="stPlotlyChart"] {
        background:rgba(21,23,28,0.92);
        border:1px solid var(--border);
        border-radius:16px;
        padding:12px 12px 4px;
        box-shadow:0 12px 32px rgba(0,0,0,0.18);
        margin-bottom:22px;
        overflow:hidden !important;
    }

    /* Movie / gallery cards */
    .movie-card, .gallery-card {
        background:linear-gradient(160deg, #20273a, #171c2c);
        border:1px solid var(--border);
        border-radius:15px;
        overflow:hidden;
        box-shadow:0 10px 28px rgba(0,0,0,0.18);
        transition:transform .2s ease, border-color .2s ease;
    }

    .movie-card:hover, .gallery-card:hover {
        transform:translateY(-4px);
        border-color:rgba(255,90,79,0.45);
    }

    .movie-card-img { width:100%; height:330px; object-fit:cover; display:block; background:#0c0d10; }
    .gallery-img { width:100%; height:290px; object-fit:cover; display:block; background:#0c0d10; }

    .movie-card-body, .gallery-body { padding:15px; }

    .movie-card-title, .gallery-title {
        color:#fffaf2 !important;
        font-size:0.92rem;
        font-weight:700;
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
    }

    .movie-card-meta, .gallery-sub {
        color:#858a94 !important;
        font-size:0.76rem;
        margin-top:4px;
    }

    .score-badge-strip {
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-top:12px;
        padding:9px 11px;
        border-radius:9px;
        background:#0f1115;
        border:1px solid var(--border);
        font-size:0.74rem;
        color:#fff !important;
    }

    /* Typography */
    h1,h2,h3,h4,h5,h6,.stMarkdown h3,.stMarkdown h4,label {
        color:#f7f4ed !important;
        font-family:'DM Sans', sans-serif !important;
        font-weight:700 !important;
    }

    h3 { letter-spacing:-0.35px; }
    p, span, div { color:#c9ccd1; }

    small { color:#858a94 !important; }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border:1px solid var(--border);
        border-radius:14px;
        overflow:hidden;
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        background:linear-gradient(135deg, #ff6b61, #ff65a3) !important;
        color:#ffffff !important;
        border:0 !important;
        border-radius:10px !important;
        font-weight:700 !important;
        padding:0.55rem 1rem !important;
        transition:all .2s ease;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background:linear-gradient(135deg, #ffc857, #ff7a59) !important;
        color:#ffffff !important;
        transform:translateY(-1px);
    }

    .app-footer {
        background:linear-gradient(135deg, #181d2d, #20243a);
        border:1px solid var(--border);
        border-radius:14px;
        padding:22px;
        text-align:center;
        color:#777c86 !important;
        font-size:0.78rem;
        margin-top:45px;
    }

    .app-footer b { color:#e8e4da !important; }

    ::-webkit-scrollbar { width:7px; height:7px; }
    ::-webkit-scrollbar-track { background:#0c0d10; }
    ::-webkit-scrollbar-thumb { background:#30343c; border-radius:8px; }

    @media (max-width: 900px) {
        .main .block-container { padding:1.25rem 1rem 3rem !important; }
        .hero-banner { padding:28px 24px; }
        .hero-title { font-size:2.25rem; }
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 2. DATA LOADING & ROBUST CLEANING PIPELINE
# ------------------------------------------------------------------------------
@st.cache_data(show_spinner="Initializing Rotten Tomatoes Cinematic Engine...")
def load_and_clean_data():
    csv_paths = [
        "Rotten Tomatoes Movies.csv",
        os.path.join(os.path.dirname(__file__), "Rotten Tomatoes Movies.csv")
    ]

    df = None
    for path in csv_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break

    if df is None:
        st.error("Dataset file 'Rotten Tomatoes Movies.csv' was not found. Please ensure the CSV file is in the application directory.")
        st.stop()

    df['movie_title'] = df['movie_title'].astype(str).str.strip()
    df['directors'] = df['directors'].fillna('Unknown').astype(str).str.strip()
    df['studio_name'] = df['studio_name'].fillna('Independent / Other').astype(str).str.strip()
    df['cast'] = df['cast'].fillna('Unknown').astype(str)
    df['critics_consensus'] = df['critics_consensus'].fillna('No consensus recorded.')
    df['movie_info'] = df['movie_info'].fillna('No synopsis available.')

    rating_clean = df['rating'].astype(str).str.strip().str.rstrip(')')
    rating_mapping = {'NR': 'Not Rated', 'NC17': 'NC-17', 'nan': 'Not Rated', '': 'Not Rated'}
    df['rating_clean'] = rating_clean.replace(rating_mapping)
    valid_ratings = ['R', 'PG-13', 'PG', 'Not Rated', 'G', 'NC-17']
    df['rating_clean'] = df['rating_clean'].apply(lambda x: x if x in valid_ratings else 'Other')

    df['in_theaters_dt'] = pd.to_datetime(df['in_theaters_date'], format='%d/%m/%Y', errors='coerce')
    df['on_streaming_dt'] = pd.to_datetime(df['on_streaming_date'], format='%d/%m/%Y', errors='coerce')

    df['release_year'] = df['in_theaters_dt'].dt.year.fillna(df['on_streaming_dt'].dt.year)
    df['release_year'] = df['release_year'].fillna(2000).astype(int)

    df['decade'] = (df['release_year'] // 10 * 10).astype(str) + 's'

    genre_runtime_median = df.groupby('rating_clean')['runtime_in_minutes'].transform('median')
    df['runtime_clean'] = df['runtime_in_minutes'].fillna(genre_runtime_median).fillna(100.0)
    df['runtime_clean'] = df['runtime_clean'].clip(lower=20, upper=300)

    df['tomatometer_rating'] = pd.to_numeric(df['tomatometer_rating'], errors='coerce').fillna(0).astype(int)
    df['tomatometer_count'] = pd.to_numeric(df['tomatometer_count'], errors='coerce').fillna(0).astype(int)

    df['audience_rating'] = pd.to_numeric(df['audience_rating'], errors='coerce')
    df['audience_rating_clean'] = df['audience_rating'].fillna(df['tomatometer_rating']).astype(int)
    df['audience_count'] = pd.to_numeric(df['audience_count'], errors='coerce').fillna(0).astype(int)

    df['tomatometer_status'] = df['tomatometer_status'].fillna('Rotten').str.strip()
    valid_statuses = ['Certified Fresh', 'Fresh', 'Rotten']
    df['tomatometer_status'] = df['tomatometer_status'].apply(lambda x: x if x in valid_statuses else 'Rotten')

    df['genre'] = df['genre'].fillna('Drama')
    df['genre_list'] = df['genre'].apply(lambda x: [g.strip() for g in str(x).split(',') if g.strip()])
    df['primary_genre'] = df['genre_list'].apply(lambda x: x[0] if len(x) > 0 else 'Drama')

    if 'poster_path' not in df.columns and 'Poster Path' in df.columns:
        df['poster_path'] = df['Poster Path']
    elif 'poster_path' not in df.columns:
        df['poster_path'] = None

    df['poster_url'] = df['poster_path'].fillna('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=300&auto=format&fit=crop&q=60')

    df['score_difference'] = df['audience_rating_clean'] - df['tomatometer_rating']
    df['abs_score_difference'] = df['score_difference'].abs()

    def assign_consensus(row):
        c = row['tomatometer_rating']
        a = row['audience_rating_clean']
        if c >= 75 and a >= 75:
            return 'Universal Acclaim'
        elif c >= 70 and a <= 55:
            return 'Critic Darling (Audience Cold)'
        elif a >= 70 and c <= 55:
            return 'Audience Favorite (Cult Classic)'
        elif c < 50 and a < 50:
            return 'Universal Flop'
        else:
            return 'Moderate Consensus'

    df['consensus_category'] = df.apply(assign_consensus, axis=1)

    return df

df_raw = load_and_clean_data()


# ------------------------------------------------------------------------------
# 3. SIDEBAR: PROFESSIONAL CONTROLS & FILTERS
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #FF6B5F; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px; border-bottom: 1px solid rgba(6,182,212,0.3); padding-bottom: 10px;">
        [SYSTEM] Analytics Engine
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:0px; font-weight:700; font-size: 1.15rem; color:#FFFFFF;'>Filter Parameters</h3>", unsafe_allow_html=True)
    st.markdown("<small style='color:#E2E8F0'>Refining 16,638 catalog records.</small>", unsafe_allow_html=True)
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    min_yr = int(df_raw['release_year'].min())
    max_yr = int(df_raw['release_year'].max())
    selected_year_range = st.slider("Release Year Span", min_value=min_yr, max_value=max_yr, value=(1970, max_yr), step=1)

    all_genres = sorted(list(set([g for sublist in df_raw['genre_list'] for g in sublist])))
    selected_genres = st.multiselect("Film Genres", options=all_genres, default=['Drama', 'Comedy', 'Action & Adventure', 'Science Fiction & Fantasy', 'Mystery & Suspense', 'Horror'])
    if not selected_genres: selected_genres = all_genres

    status_options = ['Certified Fresh', 'Fresh', 'Rotten']
    selected_statuses = st.multiselect("Tomatometer Status", options=status_options, default=status_options)
    if not selected_statuses: selected_statuses = status_options

    rating_options = ['R', 'PG-13', 'PG', 'G', 'NC-17', 'Not Rated']
    selected_ratings = st.multiselect("MPAA Content Rating", options=rating_options, default=rating_options)
    if not selected_ratings: selected_ratings = rating_options

    selected_runtime = st.slider("Runtime Duration (Minutes)", min_value=40, max_value=240, value=(60, 200), step=5)

    disconnect_filter = st.selectbox("Consensus Disconnect Focus", [
        "All Films (No Disconnect Filter)",
        "High Disconnect (|Critic - Audience| ≥ 25 pts)",
        "Audience Loved > Critics (Audience +20 pts)",
        "Critics Loved > Audience (Critic +20 pts)",
        "Universal Acclaim (Both ≥ 75%)",
        "Universal Flop (Both < 50%)"
    ])

    search_query = st.text_input("Search Title, Director, Studio", value="", placeholder="e.g., Nolan, Warner Bros...")


# ------------------------------------------------------------------------------
# 4. DATA FILTERING ENGINE
# ------------------------------------------------------------------------------
mask = (
    (df_raw['release_year'] >= selected_year_range[0]) &
    (df_raw['release_year'] <= selected_year_range[1]) &
    (df_raw['tomatometer_status'].isin(selected_statuses)) &
    (df_raw['rating_clean'].isin(selected_ratings)) &
    (df_raw['runtime_clean'] >= selected_runtime[0]) &
    (df_raw['runtime_clean'] <= selected_runtime[1])
)

df_filtered = df_raw[mask].copy()
df_filtered = df_filtered[df_filtered['genre_list'].apply(lambda gl: any(g in selected_genres for g in gl))]

if disconnect_filter == "High Disconnect (|Critic - Audience| ≥ 25 pts)":
    df_filtered = df_filtered[df_filtered['abs_score_difference'] >= 25]
elif disconnect_filter == "Audience Loved > Critics (Audience +20 pts)":
    df_filtered = df_filtered[df_filtered['score_difference'] >= 20]
elif disconnect_filter == "Critics Loved > Audience (Critic +20 pts)":
    df_filtered = df_filtered[df_filtered['score_difference'] <= -20]
elif disconnect_filter == "Universal Acclaim (Both ≥ 75%)":
    df_filtered = df_filtered[(df_filtered['tomatometer_rating'] >= 75) & (df_filtered['audience_rating_clean'] >= 75)]
elif disconnect_filter == "Universal Flop (Both < 50%)":
    df_filtered = df_filtered[(df_filtered['tomatometer_rating'] < 50) & (df_filtered['audience_rating_clean'] < 50)]

if search_query.strip():
    q = search_query.strip().lower()
    df_filtered = df_filtered[
        df_filtered['movie_title'].str.lower().str.contains(q) |
        df_filtered['directors'].str.lower().str.contains(q) |
        df_filtered['studio_name'].str.lower().str.contains(q)
    ]

if len(df_filtered) == 0:
    st.warning("No records match the current filter parameters. Please adjust settings in the sidebar.")
    st.stop()


# ------------------------------------------------------------------------------
# 5. HERO HEADER & KPI STRIP
# ------------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-eyebrow">Data Visualisation Techniques | Assignment 2</div>
    <h1 class="hero-title">Rotten Tomatoes Cinematic Intelligence</h1>
    <p class="hero-subtitle">
        Explore a century of cinema through critic and audience scores, genre patterns, release trends, and industry performance.
    </p>
    <div class="badge-container">
        <span class="pill-badge">[Dataset] 16,638 Titles Analyzed</span>
        <span class="pill-badge">[Metrics] Dual-Rating Matrix</span>
        <span class="pill-badge">[Period] 1914 - 2019</span>
        <span class="pill-badge">[Engine] Streamlit & Plotly</span>
    </div>
</div>
""", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_movies = len(df_filtered)
avg_critic = df_filtered['tomatometer_rating'].mean()
avg_audience = df_filtered['audience_rating_clean'].mean()
certified_fresh_count = (df_filtered['tomatometer_status'] == 'Certified Fresh').sum()
certified_fresh_pct = (certified_fresh_count / total_movies) * 100 if total_movies > 0 else 0
top_genre = df_filtered['primary_genre'].mode()[0] if not df_filtered.empty else "N/A"

with kpi1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-card-glow"></div><div class="kpi-label">Filtered Catalog</div><div class="kpi-val">{total_movies:,}</div><div class="kpi-sub">{(total_movies/len(df_raw)*100):.1f}% of base dataset</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-card-glow"></div><div class="kpi-label">Avg Critic Score</div><div class="kpi-val" style="color: #ff7a59;">{avg_critic:.1f}%</div><div class="kpi-sub">Tomatometer Mean</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-card-glow"></div><div class="kpi-label">Avg Audience Score</div><div class="kpi-val" style="color: #ffc857;">{avg_audience:.1f}%</div><div class="kpi-sub">Popcornmeter Mean</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-card-glow"></div><div class="kpi-label">Certified Fresh</div><div class="kpi-val" style="color: #67d59a;">{certified_fresh_pct:.1f}%</div><div class="kpi-sub">{certified_fresh_count:,} Masterpieces</div></div>', unsafe_allow_html=True)
with kpi5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-card-glow"></div><div class="kpi-label">Dominant Genre</div><div class="kpi-val" style="font-size: 1.15rem; line-height: 2.1rem; color: #9b7cff;">{top_genre}</div><div class="kpi-sub">Highest frequency</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 36px;'></div>", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 6. TABBED VISUAL ANALYTICS
# ------------------------------------------------------------------------------
tab_story, tab_perception, tab_genres, tab_studios, tab_explorer = st.tabs([
    "Trends & Distribution",
    "Critic vs Audience",
    "Genres & Eras",
    "Industry Intelligence",
    "Film Library"
])


# ==============================================================================
# TAB 1: HISTORICAL TRENDS & DISTRIBUTION
# ==============================================================================
with tab_story:
    st.markdown("""
    <div class="story-callout">
        <b>Analytical Summary:</b> Longitudinal tracking reveals an exponential increase in annual film production beginning
        in the late 1990s. Despite substantial volume growth, average critical and audience ratings remain stable within a
        58% to 65% band, while score variance expands across modern release tiers.
    </div>
    """, unsafe_allow_html=True)

    yearly_summary = df_filtered.groupby('release_year').agg(
        avg_critic=('tomatometer_rating', 'mean'),
        avg_audience=('audience_rating_clean', 'mean'),
        movie_count=('movie_title', 'count')
    ).reset_index()

    fig_timeline = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.18,
        subplot_titles=("Critic vs. Audience Annual Mean Trajectory (%)", "Annual Production Volume"),
        row_heights=[0.62, 0.38]
    )

    fig_timeline.add_trace(go.Scatter(x=yearly_summary['release_year'], y=yearly_summary['avg_critic'], name='Critic Score', line=dict(color='#ff5b61', width=3), mode='lines+markers', marker=dict(size=4)), row=1, col=1)
    fig_timeline.add_trace(go.Scatter(x=yearly_summary['release_year'], y=yearly_summary['avg_audience'], name='Audience Score', line=dict(color='#ffc857', width=3, dash='dot'), mode='lines+markers', marker=dict(size=4)), row=1, col=1)
    fig_timeline.add_trace(go.Bar(x=yearly_summary['release_year'], y=yearly_summary['movie_count'], name='Releases', marker=dict(color=yearly_summary['movie_count'], colorscale='Viridis', opacity=0.9)), row=2, col=1)

    fig_timeline.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(24,29,45,0.65)',
        height=540,
        margin=dict(l=30, r=30, t=65, b=45),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, font=dict(color="#FFFFFF", size=12)),
        hovermode="x unified",
        font=dict(family="DM Sans", color="#FFFFFF")
    )
    fig_timeline.update_yaxes(title_text="Score (%)", range=[0, 105], gridcolor="rgba(255,255,255,0.07)", row=1, col=1)
    fig_timeline.update_yaxes(title_text="Count", gridcolor="rgba(255,255,255,0.07)", row=2, col=1)
    fig_timeline.update_xaxes(title_text="Release Year", gridcolor="rgba(255,255,255,0.07)", row=2, col=1)
    st.plotly_chart(fig_timeline, use_container_width=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    col_t1_left, col_t1_right = st.columns(2)

    with col_t1_left:
        status_counts = df_filtered['tomatometer_status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_donut = px.pie(status_counts, names='Status', values='Count', hole=0.6, color='Status', color_discrete_map={'Certified Fresh': '#ff5b61', 'Fresh': '#5fa8ff', 'Rotten': '#858da3'}, title="Tomatometer Status Distribution")
        fig_donut.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#101522', width=2)))
        fig_donut.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=380, margin=dict(l=20, r=20, t=65, b=20), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_t1_right:
        mpaa_counts = df_filtered['rating_clean'].value_counts().reset_index()
        mpaa_counts.columns = ['Rating', 'Count']
        fig_mpaa = px.bar(mpaa_counts, x='Count', y='Rating', orientation='h', color='Rating', title="Distribution by MPAA Rating", color_discrete_sequence=px.colors.sequential.Sunset)
        fig_mpaa.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,45,0.65)', height=380, margin=dict(l=20, r=20, t=65, b=20), showlegend=False, yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_mpaa, use_container_width=True)


# ==============================================================================
# TAB 2: CRITIC VS. AUDIENCE DISCONNECT
# ==============================================================================
with tab_perception:
    st.markdown("""
    <div class="story-callout">
        <b>Core Investigation:</b> The scatter matrix below evaluates the structural disconnect between professional critic reviews
        and audience sentiment. Quadrants segment <i>'Critic Darlings'</i> (high critical acclaim, cold audience reception) from
        <i>'Cult Classics'</i> (audience favorites poorly rated by critics).
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns([8, 4])

    with col_p1:
        scatter_sample = df_filtered.sample(min(len(df_filtered), 3000), random_state=42) if len(df_filtered) > 3000 else df_filtered
        fig_scatter = px.scatter(
            scatter_sample, x='tomatometer_rating', y='audience_rating_clean', color='tomatometer_status',
            color_discrete_map={'Certified Fresh': '#ff5b61', 'Fresh': '#5fa8ff', 'Rotten': '#858da3'},
            hover_name='movie_title', title="4-Quadrant Perception Matrix: Critics vs. Audience", trendline="ols", opacity=0.85
        )
        fig_scatter.add_vline(x=60, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        fig_scatter.add_hline(y=60, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        fig_scatter.add_annotation(x=88, y=96, text="Universal Acclaim", showarrow=False, font=dict(color="#ffc857", size=11), bgcolor="rgba(24,29,46,0.9)", bordercolor="rgba(255,200,87,0.4)", borderpad=6)
        fig_scatter.add_annotation(x=20, y=93, text="Cult Classics", showarrow=False, font=dict(color="#ff65a3", size=11), bgcolor="rgba(24,29,46,0.9)", bordercolor="rgba(255,101,163,0.4)", borderpad=6)
        fig_scatter.add_annotation(x=88, y=18, text="Critic Darlings", showarrow=False, font=dict(color="#9b7cff", size=11), bgcolor="rgba(24,29,46,0.9)", bordercolor="rgba(155,124,255,0.4)", borderpad=6)
        fig_scatter.add_annotation(x=20, y=18, text="Universal Flops", showarrow=False, font=dict(color="#858da3", size=11), bgcolor="rgba(24,29,46,0.9)", bordercolor="rgba(133,141,163,0.4)", borderpad=6)
        
        fig_scatter.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=600, margin=dict(l=20, r=20, t=65, b=20), xaxis=dict(range=[0, 105]), yaxis=dict(range=[0, 105]))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_p2:
        fig_hist = px.histogram(df_filtered, x='score_difference', nbins=35, color_discrete_sequence=['#ff5b61'], title="Score Discrepancy (Audience - Critic)")
        fig_hist.add_vline(x=0, line_dash="solid", line_color="#fff", annotation_text="Parity")
        fig_hist.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=285, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        consensus_df = df_filtered['consensus_category'].value_counts().reset_index()
        consensus_df.columns = ['Consensus Category', 'Count']
        fig_cat = px.bar(consensus_df, x='Count', y='Consensus Category', orientation='h', color='Consensus Category', title="Consensus Breakdown", color_discrete_sequence=px.colors.sequential.Plasma)
        fig_cat.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=285, margin=dict(l=10, r=10, t=55, b=10), showlegend=False, yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3>Extreme Consensus Disconnects Spotlight</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    col_t_left, col_t_right = st.columns(2)
    with col_t_left:
        st.markdown("<h4>Cult Classics (Audience Loved, Critics Panned)</h4>", unsafe_allow_html=True)
        cult_movies = df_filtered[df_filtered['tomatometer_rating'] <= 50].sort_values(by='score_difference', ascending=False).head(3)
        c_cols = st.columns(3)
        for idx, (_, row) in enumerate(cult_movies.iterrows()):
            with c_cols[idx]:
                st.markdown(f'<div class="movie-card"><img src="{row["poster_url"]}" class="movie-card-img"><div class="movie-card-body"><div class="movie-card-title">{row["movie_title"]}</div><div class="movie-card-meta">{row["release_year"]} | {row["primary_genre"]}</div><div class="score-badge-strip"><span style="color:#ff5b61;">Crit: {row["tomatometer_rating"]}%</span><span style="color:#ffc857;">Aud: {row["audience_rating_clean"]}%</span></div></div></div>', unsafe_allow_html=True)

    with col_t_right:
        st.markdown("<h4>Critic Darlings (Critics Loved, Audience Cold)</h4>", unsafe_allow_html=True)
        darling_movies = df_filtered[df_filtered['audience_rating_clean'] <= 50].sort_values(by='score_difference', ascending=True).head(3)
        d_cols = st.columns(3)
        for idx, (_, row) in enumerate(darling_movies.iterrows()):
            with d_cols[idx]:
                st.markdown(f'<div class="movie-card"><img src="{row["poster_url"]}" class="movie-card-img"><div class="movie-card-body"><div class="movie-card-title">{row["movie_title"]}</div><div class="movie-card-meta">{row["release_year"]} | {row["primary_genre"]}</div><div class="score-badge-strip"><span style="color:#9b7cff;">Crit: {row["tomatometer_rating"]}%</span><span style="color:#ff5b61;">Aud: {row["audience_rating_clean"]}%</span></div></div></div>', unsafe_allow_html=True)


# ==============================================================================
# TAB 3: GENRES & ERAS
# ==============================================================================
with tab_genres:
    st.markdown("""
    <div class="story-callout">
        <b>Genre Trajectory Analysis:</b> Examine how genre ratings and output evolved across cinematic eras.
        The matrix heatmap outlines critical standards across decades, highlighting output shifts from traditional drama
        to contemporary animation and documentary formats.
    </div>
    """, unsafe_allow_html=True)

    exploded_df = df_filtered.explode('genre_list')
    exploded_df = exploded_df[exploded_df['genre_list'].isin(selected_genres)]

    col_g1, col_g2 = st.columns([7, 5])

    with col_g1:
        heatmap_metric = st.radio("Heatmap Target Metric:", options=["Critic Score (Tomatometer)", "Audience Score", "Score Discrepancy (Audience - Critic)"], horizontal=True)
        metric_col = 'tomatometer_rating' if "Critic" in heatmap_metric else ('audience_rating_clean' if "Audience Score" in heatmap_metric else 'score_difference')

        heatmap_pivot = exploded_df.pivot_table(index='genre_list', columns='decade', values=metric_col, aggfunc='mean').dropna(how='all')
        sorted_decades = [d for d in ['1920s', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s'] if d in heatmap_pivot.columns]
        heatmap_pivot = heatmap_pivot[sorted_decades]

        fig_heat = px.imshow(heatmap_pivot, x=sorted_decades, y=heatmap_pivot.index, color_continuous_scale="Teal", text_auto=".1f", aspect="auto", title=f"Mean {heatmap_metric} Across Decades")
        fig_heat.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=500, margin=dict(l=20, r=20, t=65, b=20))
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_g2:
        st.markdown("<h3>Market Composition Hierarchy</h3>", unsafe_allow_html=True)
        st.markdown("<small style='color:#858a94'>Hierarchy: MPAA Rating → Primary Genre → Quality Tier</small>", unsafe_allow_html=True)
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        sunburst_sample = df_filtered.dropna(subset=['rating_clean', 'primary_genre', 'tomatometer_status'])
        
        # FIXED: Optimized donut chart size and margins to completely prevent text cut-off
        fig_sunburst = px.sunburst(
            sunburst_sample,
            path=['rating_clean', 'primary_genre', 'tomatometer_status'],
            color='tomatometer_status',
            color_discrete_map={'Certified Fresh': '#ff5b61', 'Fresh': '#5fa8ff', 'Rotten': '#737983'},
            title="Catalog Composition Breakdown"
        )
        fig_sunburst.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            height=460,
            margin=dict(l=35, r=35, t=65, b=35)
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3>Runtime Distribution by Quality Tier</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    top_8_genres = df_filtered['primary_genre'].value_counts().head(8).index.tolist()
    genre_runtime_df = df_filtered[df_filtered['primary_genre'].isin(top_8_genres)]

    fig_box = px.box(genre_runtime_df, x='primary_genre', y='runtime_clean', color='tomatometer_status', color_discrete_map={'Certified Fresh': '#ff5b61', 'Fresh': '#5fa8ff', 'Rotten': '#737983'}, title="Runtime Spread (Minutes) Across Quality Tiers", points="outliers")
    fig_box.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=420, margin=dict(l=20, r=20, t=65, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1))
    st.plotly_chart(fig_box, use_container_width=True)


# ==============================================================================
# TAB 4: INDUSTRY INTELLIGENCE
# ==============================================================================
with tab_studios:
    st.markdown("""
    <div class="story-callout">
        <b>Industry Benchmarking:</b> Evaluate studio production volume against critical ratios. Compare major Hollywood studios
        and visionary directors by their percentage of Certified Fresh releases and overall mean ratings.
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        min_studio_films = st.slider("Minimum Film Output for Studio Ranking:", min_value=15, max_value=100, value=30, step=5)
        studio_agg = df_filtered[df_filtered['studio_name'] != 'Independent / Other'].groupby('studio_name').agg(
            total_films=('movie_title', 'count'), avg_critic=('tomatometer_rating', 'mean'), avg_audience=('audience_rating_clean', 'mean'), certified_count=('tomatometer_status', lambda x: (x == 'Certified Fresh').sum())
        ).reset_index()
        studio_agg = studio_agg[studio_agg['total_films'] >= min_studio_films]
        studio_agg['certified_pct'] = (studio_agg['certified_count'] / studio_agg['total_films']) * 100
        studio_agg = studio_agg.sort_values(by='certified_pct', ascending=True).tail(15)

        fig_studio = px.bar(studio_agg, x='certified_pct', y='studio_name', orientation='h', color='avg_critic', color_continuous_scale='Teal', title=f"Top Studios by Certified Fresh % (Min. {min_studio_films} Films)")
        fig_studio.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=520, margin=dict(l=20, r=20, t=65, b=20), yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_studio, use_container_width=True)

    with col_s2:
        min_dir_films = st.slider("Minimum Film Count for Director Ranking:", min_value=5, max_value=20, value=6, step=1)
        dir_agg = df_filtered[df_filtered['directors'] != 'Unknown'].groupby('directors').agg(
            total_films=('movie_title', 'count'), avg_critic=('tomatometer_rating', 'mean'), avg_audience=('audience_rating_clean', 'mean'), certified_count=('tomatometer_status', lambda x: (x == 'Certified Fresh').sum())
        ).reset_index()
        dir_agg = dir_agg[dir_agg['total_films'] >= min_dir_films]
        dir_agg = dir_agg.sort_values(by='avg_critic', ascending=True).tail(15)

        fig_dir = px.bar(dir_agg, x='avg_critic', y='directors', orientation='h', color='avg_audience', color_continuous_scale='Magma', title=f"Top Directors by Mean Critic Score (Min. {min_dir_films} Films)")
        fig_dir.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=520, margin=dict(l=20, r=20, t=65, b=20), yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_dir, use_container_width=True)


# ==============================================================================
# TAB 5: FILM LIBRARY & DISCOVERY
# ==============================================================================
with tab_explorer:
    st.markdown("<h3>Film Library & Discovery</h3>", unsafe_allow_html=True)
    st.markdown("<small style='color:#858a94'>Inspect high-definition poster cards, perform head-to-head title comparisons, or view the poster gallery.</small>", unsafe_allow_html=True)
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "Film Spotlight",
        "Compare Films",
        "Visual Poster Gallery",
        "Catalog & Export"
    ])

    with sub_tab1:
        spot_col_top1, spot_col_top2 = st.columns([8, 4])
        with spot_col_top1:
            all_spot_movies = df_filtered.sort_values(by=['tomatometer_rating', 'audience_rating_clean'], ascending=False)['movie_title'].tolist()
            selected_movie_name = st.selectbox("Select Movie Title for Spotlight:", options=all_spot_movies, index=0)
        with spot_col_top2:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Load Random Record", use_container_width=True):
                selected_movie_name = df_filtered.sample(1).iloc[0]['movie_title']
                st.toast(f"Loaded: {selected_movie_name}")

        movie_row = df_filtered[df_filtered['movie_title'] == selected_movie_name].iloc[0]
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        spot_c1, spot_c2, spot_c3 = st.columns([3.5, 4.5, 4])

        with spot_c1:
            st.image(movie_row['poster_url'], use_container_width=True, caption=f"{movie_row['movie_title']} ({movie_row['release_year']})")
            yt_query = f"https://www.youtube.com/results?search_query={movie_row['movie_title'].replace(' ', '+')}+{movie_row['release_year']}+trailer"
            st.markdown(f'<a href="{yt_query}" target="_blank" style="text-decoration:none;"><div style="background:linear-gradient(135deg, #ff5b61, #ff7a59); color:#FFFFFF; text-align:center; padding:12px; border-radius:10px; font-weight:700; margin-top:14px;">Search Trailer on YouTube</div></a>', unsafe_allow_html=True)
        with spot_c2:
            st.markdown(f"<h2>{movie_row['movie_title']}</h2>", unsafe_allow_html=True)
            st.markdown(f"**Premiere:** `{movie_row['release_year']}` | **MPAA:** `{movie_row['rating_clean']}` | **Runtime:** `{int(movie_row['runtime_clean'])} mins`")
            st.markdown(f"**Director:** {movie_row['directors']}")
            st.markdown(f"**Studio:** {movie_row['studio_name']}")
            st.markdown(f"**Genre:** {movie_row['genre']}")
            st.markdown(f"**Cast:** {movie_row['cast']}")
            st.markdown("---")
            st.markdown("<h4>Synopsis</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:#b9bfd0; line-height:1.7;'>{movie_row['movie_info']}</p>", unsafe_allow_html=True)
        with spot_c3:
            st.markdown("<h4>Evaluation Metrics</h4>", unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-card" style="padding:18px;"><div class="kpi-label" style="color:#ff5b61;">Critic Tomatometer</div><div class="kpi-val">{movie_row["tomatometer_rating"]}%</div><div style="height:10px;"></div><div class="kpi-label" style="color:#ffc857;">Audience Popcornmeter</div><div class="kpi-val">{movie_row["audience_rating_clean"]}%</div><div style="height:10px;"></div><div class="kpi-label">Consensus Tag</div><div style="font-size:0.9rem; font-weight:700; color:#fff;">{movie_row["consensus_category"]}</div></div>', unsafe_allow_html=True)
            st.markdown("<h4>Critics Consensus</h4>", unsafe_allow_html=True)
            st.info(f"\"{movie_row['critics_consensus']}\"")

    with sub_tab2:
        st.markdown("<h3>Comparative Film Analysis</h3>", unsafe_allow_html=True)
        st.markdown("<small style='color:#858a94'>Evaluate two film records side-by-side.</small>", unsafe_allow_html=True)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        battle_col1, battle_col2 = st.columns(2)
        movie_list_sorted = df_filtered['movie_title'].tolist()
        with battle_col1:
            movie_a_name = st.selectbox("Select Contender A:", options=movie_list_sorted, index=0)
            movie_a = df_filtered[df_filtered['movie_title'] == movie_a_name].iloc[0]
        with battle_col2:
            default_idx_b = min(1, len(movie_list_sorted) - 1)
            movie_b_name = st.selectbox("Select Contender B:", options=movie_list_sorted, index=default_idx_b)
            movie_b = df_filtered[df_filtered['movie_title'] == movie_b_name].iloc[0]

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col_ba, col_mid, col_bb = st.columns([5, 2, 5])
        with col_ba:
            st.markdown(f'<div class="movie-card"><img src="{movie_a["poster_url"]}" class="movie-card-img"><div class="movie-card-body"><div class="movie-card-title">{movie_a["movie_title"]}</div><div class="movie-card-meta">{movie_a["release_year"]} | {int(movie_a["runtime_clean"])}m</div><div class="score-badge-strip"><span style="color:#ff5b61; font-weight:700;">{movie_a["tomatometer_rating"]}%</span><span style="color:#ffc857; font-weight:700;">{movie_a["audience_rating_clean"]}%</span></div></div></div>', unsafe_allow_html=True)
        with col_mid:
            st.markdown('<div style="display:flex; height:100%; justify-content:center; align-items:center;"><h2 style="color:#858a94;">VS</h2></div>', unsafe_allow_html=True)
        with col_bb:
            st.markdown(f'<div class="movie-card"><img src="{movie_b["poster_url"]}" class="movie-card-img"><div class="movie-card-body"><div class="movie-card-title">{movie_b["movie_title"]}</div><div class="movie-card-meta">{movie_b["release_year"]} | {int(movie_b["runtime_clean"])}m</div><div class="score-badge-strip"><span style="color:#ff5b61; font-weight:700;">{movie_b["tomatometer_rating"]}%</span><span style="color:#ffc857; font-weight:700;">{movie_b["audience_rating_clean"]}%</span></div></div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        comp_df = pd.DataFrame({
            'Metric': ['Critic Score (%)', 'Audience Score (%)', 'Runtime (Mins)'],
            movie_a['movie_title']: [movie_a['tomatometer_rating'], movie_a['audience_rating_clean'], movie_a['runtime_clean']],
            movie_b['movie_title']: [movie_b['tomatometer_rating'], movie_b['audience_rating_clean'], movie_b['runtime_clean']]
        })
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name=movie_a['movie_title'], x=comp_df['Metric'], y=comp_df[movie_a['movie_title']], marker_color='#ff5b61'))
        fig_comp.add_trace(go.Bar(name=movie_b['movie_title'], x=comp_df['Metric'], y=comp_df[movie_b['movie_title']], marker_color='#ffc857'))
        fig_comp.update_layout(barmode='group', template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(24,29,46,0.65)', height=340, margin=dict(l=15, r=15, t=40, b=15), legend=dict(orientation="h", yanchor="bottom", y=1.03, xanchor="right", x=1))
        st.plotly_chart(fig_comp, use_container_width=True)

    with sub_tab3:
        st.markdown("<h3>Visual Poster Showcase Gallery</h3>", unsafe_allow_html=True)
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        gal_sort_col, gal_limit_col = st.columns([6, 6])
        with gal_sort_col:
            gallery_sort = st.selectbox("Sort Gallery By:", options=["Highest Critic Score (Tomatometer)", "Highest Audience Score (Popcorn)", "Biggest Score Discrepancy", "Newest Releases First", "Oldest Classics First"])
        with gal_limit_col:
            gallery_count = st.select_slider("Posters to display:", options=[12, 18, 24, 36, 48], value=24)

        gal_df = df_filtered.copy()
        if "Critic Score" in gallery_sort: gal_df = gal_df.sort_values(by='tomatometer_rating', ascending=False)
        elif "Audience Score" in gallery_sort: gal_df = gal_df.sort_values(by='audience_rating_clean', ascending=False)
        elif "Discrepancy" in gallery_sort: gal_df = gal_df.sort_values(by='score_difference', ascending=False)
        elif "Newest" in gallery_sort: gal_df = gal_df.sort_values(by='release_year', ascending=False)
        elif "Oldest" in gallery_sort: gal_df = gal_df.sort_values(by='release_year', ascending=True)

        display_sample = gal_df.head(gallery_count)
        cols_per_row = 4
        gal_rows = [display_sample.iloc[i:i+cols_per_row] for i in range(0, len(display_sample), cols_per_row)]
        for row_df in gal_rows:
            g_cols = st.columns(cols_per_row)
            for idx, (_, m) in enumerate(row_df.iterrows()):
                with g_cols[idx]:
                    st.markdown(f'<div class="gallery-card"><img src="{m["poster_url"]}" class="gallery-img"><div class="gallery-body"><div class="gallery-title">{m["movie_title"]}</div><div class="gallery-sub">{m["release_year"]} | {m["primary_genre"]}</div><div class="score-badge-strip"><span style="color:#ff5b61;">{m["tomatometer_rating"]}%</span><span style="color:#ffc857;">{m["audience_rating_clean"]}%</span></div></div></div>', unsafe_allow_html=True)

    with sub_tab4:
        st.markdown("<h3>Filtered Catalog Data Table</h3>", unsafe_allow_html=True)
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        export_cols = ['movie_title', 'release_year', 'rating_clean', 'genre', 'directors', 'runtime_clean', 'studio_name', 'tomatometer_status', 'tomatometer_rating', 'audience_rating_clean', 'score_difference', 'consensus_category']
        st.dataframe(df_filtered[export_cols], use_container_width=True, height=420)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        csv_data = df_filtered[export_cols].to_csv(index=False).encode('utf-8')
        st.download_button("Download Filtered Data as CSV", data=csv_data, file_name="rotten_tomatoes_filtered.csv", mime="text/csv")


# ------------------------------------------------------------------------------
# 7. FOOTER
# ------------------------------------------------------------------------------
st.markdown("""
<div class="app-footer">
    <b>Data Visualisation Techniques (Assignment 2)</b> | Cinematic Intelligence Interactive Dashboard Powered by Streamlit &amp; Plotly<br>
    Dataset Source: Maven Analytics &amp; Rotten Tomatoes Catalog (16,638 titles)
</div>
""", unsafe_allow_html=True)