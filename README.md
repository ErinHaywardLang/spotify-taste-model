# spotify-taste-model

A personal machine learning project to predict how much I'll like a song and rank Spotify's Discover Weekly and Release Radar playlists.

This is an exploratory learning project where I combine the Spotify Web API with Python and ML techniques to help prioritise which songs to listen to each week. The goal is to eventually connect to Spotify's developer API to automate weekly playlist pulls and rankings.

**Current Status** (2026-03-01): Spotify API access established! Training dataset curated with ~300 manually labeled songs across 3 preference categories. Ready to implement real data pipeline and feature exploration. 

## Goals
- Build a personal music preference model using historical listening data
- Pull weekly Spotify playlists (Discover Weekly, Release Radar)
- Score and rank songs based on predicted enjoyment
- Make listening to new music more efficient 

## Training Dataset
- **Manual Curation:** 3 playlists in 'ML' folder (Like/Dislike/Neutral)
- **Dataset Size:** ~300 songs (balanced: ~100 per preference category)
- **Quality Control:** Duplicate detection strategy implemented
- **Labels:** Clean preference classifications for supervised learning

## Proven Approach
- **Baseline Model:** RandomForest classifier with 95% accuracy on synthetic data
- **Feature Engineering:** 10 core Spotify audio features (danceability, energy, valence, etc.)
- **Data Pipeline:** IterativeImputer + LabelEncoder preprocessing approach 

## Tech Stack
- Python
- Jupyter Notebooks
- Spotipy (Spotify Web API client)
- Pandas & NumPy (data manipulation)
- scikit-learn (machine learning)
- Matplotlib / Seaborn (optional visualization)
- python-dotenv (environment configuration)

## Project Structure
```
spotify-taste-model/
├── README.md                          # Project documentation
├── plan.md                           # Comprehensive implementation plan
├── requirements.txt                   # Python dependencies
├── src/
│   ├── __init__.py                   # Package initialization
│   ├── spotify_client.py             # Spotify API client (needs import fix)
│   └── data_collector.py             # Playlist data extraction (planned)
├── notebooks/
│   ├── connect.ipynb                 # API connection testing (has import error)
│   ├── 01_data_collection.ipynb      # Extract real playlist data (planned)
│   ├── 02_feature_exploration.ipynb  # Correlation & visualization (planned)
│   ├── 03_model_training.ipynb       # ML pipeline adaptation (planned)
│   └── sample data [old]/            # Archive of synthetic data experiments
│       ├── 00_sample_data.ipynb      # (Various sample data notebooks)
│       ├── 01_explore_spotify_data.ipynb
│       ├── 02_messy_sample_spotify_data.ipynb
│       ├── 03_explore_spotify_data_messy.ipynb
│       ├── sample_spotify_likes_dataset_large.csv
│       └── sample_spotify_likes_dataset_noisy.csv
├── data/                             # Real playlist datasets (to be created)
└── models/                           # Trained models storage (to be created)
```

## Setup
1. Clone the repo
2. Create and activate a virtual environment 
3. Install dependencies: `pip install -r requirements.txt`
4. Spotify API credentials already configured in `.env`
5. **Current Focus:** Follow implementation plan in `plan.md`
6. Start with Phase 1: Fix API integration and extract playlist data

## Current Progress
- ✅ Environment & dependencies configured
- ✅ Spotify API credentials established
- ✅ Proven ML pipeline developed (95% accuracy on synthetic data)
- ✅ Training dataset curated (~300 songs, 3 balanced preference categories)
- ✅ Comprehensive implementation plan created (see plan.md)
- 🔄 **NEXT:** Fix API integration and extract real playlist data
- 🔄 Phase 1: API connection and duplicate detection
- 🔄 Phase 2: Feature extraction and data collection
- ⏸️ Phase 3: Feature exploration and correlation analysis
- ⏸️ Phase 4: Model training and evaluation

## Known Issues
- **Import Error:** `notebooks/connect.ipynb` expects `get_spotify_client()` function that doesn't exist
- **API Integration:** Connection established but code mismatch preventing data extraction
- **Duplicate Detection:** Need to verify no songs exist in multiple preference playlists

See `plan.md` for detailed resolution strategy.
