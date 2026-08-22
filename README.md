# personal-music-recommender

A personal project that learns my music taste from my own playlists and ranks new songs by predicted enjoyment.

This is an exploratory learning project combining playlist data with acoustic features and ML techniques to help prioritise which songs to listen to each week.

**Current Status** (2026-08-22): Training dataset curated from manually labeled songs across 3 preference categories (Like / Neutral / Dislike). Acoustic features come from **ReccoBeats** (a free, no-auth API returning the classic feature set). Coverage validated: **242/304 tracks (79.6%)** resolved.

> Data powered by [ReccoBeats](https://reccobeats.com) (audio features).

## Goals
- Build a personal music preference model from historically labeled songs
- Pull weekly playlist candidates and score them by predicted enjoyment
- Make listening to new music more efficient

## Training Dataset
- **Manual Curation:** 3 playlists labelled Like / Neutral / Dislike
- **Dataset Size:** 304 unique tracks (Like: 105, Neutral: 100, Dislike: 99)
- **Feature Coverage:** 242/304 (79.6%) resolved via ReccoBeats
- **Quality Control:** Cross-playlist dedupe keeps most recently added track
- **Labels:** Clean preference classifications for supervised learning

## Data Sources & Why
- **Spotify** is used **only** to read my own playlists — a list of track titles/artists/labels. No Spotify audio or audio-feature content is used in this project.
- **ReccoBeats** (`GET /v1/audio-features?ids=`) supplies the acoustic features that power the model:
  `danceability`, `energy`, `valence`, `acousticness`, `instrumentalness`, `liveness`, `speechiness`, `tempo`, `loudness`, `key`, `mode`

**Why not Spotify's own audio features?** Spotify has deprecated its audio-features endpoints, so they're no longer a reliable source.

**Why not GetSongBPM?** A coverage spike on real tracks: GetSongBPM resolved only **7/21 (33%)** — it skews mainstream and misses indie/electronic/newer releases. ReccoBeats resolved **18/21 (86%)**, matching the catalog by design.

**Coverage note:** expected ~80% coverage; ~20% of tracks (typically obscure/new) lack features and are imputed or dropped per Phase 2 policy.

---
*Backlink: data also cross-referenced with [GetSongBPM](https://getsongbpm.com) (API key registration credit).*

## Proven Approach
- **Baseline Model:** RandomForest classifier (95% accuracy on synthetic data)
- **Feature Set (ReccoBeats):** full 11-feature set (see above)
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
personal-music-recommender/
├── README.md                          # Project documentation
├── plan.md                           # Implementation plan
├── requirements.txt                   # Python dependencies
├── src/
│   ├── __init__.py                   # Package initialization
│   ├── spotify_client.py             # Spotify playlist client (labels)
│   ├── reccobeats_client.py          # ReccoBeats feature fetch (primary)
│   ├── getsongbpm_client.py          # GetSongBPM client (spike/alt, optional)
│   └── data_collector.py             # End-to-end collection (planned)
├── notebooks/
│   ├── connect.ipynb                 # API connection testing
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
│   ├── music_dataset.csv             # Merged labeled dataset ✅
│   └── phase0_spike_results.csv      # Spike coverage comparison
└── models/                           # Trained models storage (to be created)
```

## Setup
1. Clone the repo
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Playlist API credentials already configured in `.env`
5. (Optional) `GETSONGBPM_API_KEY` in `.env` for GetSongBPM cross-reference
6. **Current Focus:** follow implementation plan in `plan.md`
7. Start with Phase 1/2 (already done): run `01_data_collection.py`

## Current Progress
- ✅ Environment & dependencies configured
- ✅ Playlist API credentials established
- ✅ Training dataset curated (304 unique songs, 3 preference categories)
- ✅ Phase 0 spike: ReccoBeats 86% vs GetSongBPM 33% coverage (decision)
- ✅ Phase 1+2: playlist extraction, dedupe, ReccoBeats features → dataset (242/304)
- 🔄 **NEXT:** Phase 3 — feature exploration & visualization
- ⏸️ Phase 4: Model training and evaluation

## Known Issues
- **Coverage:** ~20% of tracks lack ReccoBeats features (obscure/new) — impute or drop per Phase 2 policy
- **ReccoBeats reliability:** no-auth, free, single-maintainer API with no SLA; `features_cache.csv` keeps re-runs safe
- **Spotify API to-dos:** old `/tracks` endpoint 403s — `01_data_collection.py` uses new `/items` endpoint

See `plan.md` for detailed resolution strategy.