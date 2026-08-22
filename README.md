# spotify-taste-model

A personal machine learning project to predict how much I'll like a song and rank Spotify's Discover Weekly and Release Radar playlists.

This is an exploratory learning project where I combine Spotify playlist data with acoustic features and Python/ML techniques to help prioritise which songs to listen to each week.

**Current Status** (2026-08-22): Spotify API access established. Training dataset curated with manually labeled songs across 3 preference categories (Like / Neutral / Dislike). Data-source pivot complete: Spotify's audio-features endpoints were deprecated and Spotify's terms now prohibit training ML/AI models on Spotify content, so acoustic features come from **ReccoBeats** (a free, no-auth API returning the classic feature set). Phase 0 spike validated coverage: **242/304 tracks (79.6%)** resolved.

> Data powered by [ReccoBeats](https://reccobeats.com) (audio features). 

## Goals
- Build a personal music preference model using historical listening data
- Pull weekly Spotify playlists (Discover Weekly, Release Radar)
- Score and rank songs based on predicted enjoyment
- Make listening to new music more efficient 

## Training Dataset
- **Manual Curation:** 3 playlists in 'ML' folder (Like/Dislike/Neutral)
- **Dataset Size:** 304 unique tracks (Like: 105, Neutral: 100, Dislike: 99)
- **Feature Coverage:** 242/304 (79.6%) resolved via ReccoBeats
- **Quality Control:** Cross-playlist dedupe keeps most recently added track
- **Labels:** Clean preference classifications for supervised learning

## Data Sources & Why
Spotify is used **only** for playlist structure, labels, and track titles/artists. Acoustic features no longer come from Spotify: the audio-features endpoints are officially **deprecated**, and Spotify's terms now ban training machine-learning models on Spotify content.

Features are fetched from the **ReccoBeats** API (`GET /v1/audio-features?ids=`), which returns the classic feature set by Spotify track id:
- `danceability`, `energy`, `valence`, `acousticness`, `instrumentalness`
- `liveness`, `speechiness`, `tempo`, `loudness`, `key`, `mode`

**Why not GetSongBPM?** A Phase 0 spike measured coverage on real tracks: GetSongBPM could only resolve **7/21 (33%)** — it skews mainstream and misses indie/electronic/newer releases. ReccoBeats resolved **18/21 (86%)** on the same sample, matching Spotify's catalog by design. (A GetSongBPM API key was registered during the spike; the mandatory backlink is kept at the bottom.)

**Coverage note:** expected ~80% real coverage; ~20% of tracks (typically obscure/new) will lack features and be imputed or dropped per Phase 2 policy.

---
*Backlink: data also cross-referenced with [GetSongBPM](https://getsongbpm.com) (API key registration credit).*

## Proven Approach
- **Baseline Model:** RandomForest classifier (95% accuracy on synthetic data)
- **Feature Set (ReccoBeats):** full 10-feature Spotify-style set (see above)
- **Data Pipeline:** IterativeImputer + LabelEncoder preprocessing approach 

## Tech Stack
- Python
- Jupyter Notebooks
- Spotipy (Spotify Web API client — playlist/label extraction only)
- requests (ReccoBeats + GetSongBPM API clients)
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
│   ├── spotify_client.py             # Spotify API client (playlist/labels)
│   ├── reccobeats_client.py          # ReccoBeats feature fetch (primary)
│   ├── getsongbpm_client.py          # GetSongBPM client (spike/alt, optional)
│   └── data_collector.py             # End-to-end collection (planned)
├── notebooks/
│   ├── connect.ipynb                 # API connection testing (has import error)
│   ├── 00_getsongbpm_spike.py        # Phase 0 coverage spike (GetSongBPM vs ReccoBeats)
│   ├── 01_data_collection.py         # Extract playlists + ReccoBeats features ✅
│   ├── 02_feature_exploration.py     # Correlation & visualization (planned)
│   ├── 03_model_training.py          # ML pipeline adaptation (planned)
│   └── sample data [old]/            # Archive of synthetic data experiments
│       ├── 00_sample_data.ipynb      # (Various sample data notebooks)
│       ├── 01_explore_spotify_data.ipynb
│       ├── 02_messy_sample_spotify_data.ipynb
│       ├── 03_explore_spotify_data_messy.ipynb
│       ├── sample_spotify_likes_dataset_large.csv
│       └── sample_spotify_likes_dataset_noisy.csv
├── data/
│   ├── features_cache.csv            # Resumable ReccoBeats feature cache ✅
│   ├── spotify_taste_dataset.csv     # Merged labeled dataset ✅
│   └── phase0_spike_results.csv      # Spike coverage comparison
└── models/                           # Trained models storage (to be created)
```

## Setup
1. Clone the repo
2. Create and activate a virtual environment 
3. Install dependencies: `pip install -r requirements.txt`
4. Spotify API credentials already configured in `.env`
5. (Optional) `GETSONGBPM_API_KEY` in `.env` for GetSongBPM cross-reference
6. **Current Focus:** Follow implementation plan in `plan.md`
7. Start with Phase 1/2 (already done): run `01_data_collection.py`

## Current Progress
- ✅ Environment & dependencies configured
- ✅ Spotify API credentials established
- ✅ Training dataset curated (304 unique songs, 3 preference categories)
- ✅ Phase 0 spike: ReccoBeats 86% vs GetSongBPM 33% coverage (decision)
- ✅ Phase 1+2: playlist extraction, dedupe, ReccoBeats features → dataset (242/304)
- 🔄 **NEXT:** Phase 3 — feature exploration & visualization
- ⏸️ Phase 4: Model training and evaluation

## Known Issues
- **Coverage:** ~20% of tracks lack ReccoBeats features (obscure/new) — impute or drop per Phase 2 policy
- **ReccoBeats reliability:** no-auth, free, single-maintainer API with no SLA; `features_cache.csv` keeps re-runs safe
- **Spotify to-do's:** old `/tracks` endpoint 403s — `01_data_collection.py` uses new `/items` endpoint
- **connect.ipynb** still has a stale import of `spotify_client_quiet` (retire in a later pass)

See `plan.md` for detailed resolution strategy.
