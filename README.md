# spotify-taste-model

A personal machine learning project to predict how much I'll like a song and rank Spotify's Discover Weekly and Release Radar playlists.

This is an exploratory learning project where I combine Spotify playlist data with [GetSongBPM](https://getsongbpm.com) acoustic features and Python/ML techniques to help prioritise which songs to listen to each week.

**Current Status** (2026-08-22): Spotify API access established. Training dataset curated with manually labeled songs across 3 preference categories (Like / Neutral / Dislike). Data-source pivot in progress: Spotify's audio-features endpoints were deprecated and Spotify's terms now prohibit training ML/AI models on Spotify content, so acoustic features for this project come from [GetSongBPM](https://getsongbpm.com).

> Data powered by [GetSongBPM](https://getsongbpm.com) (BPM, key, and acoustic analysis). 

## Goals
- Build a personal music preference model using historical listening data
- Pull weekly Spotify playlists (Discover Weekly, Release Radar)
- Score and rank songs based on predicted enjoyment
- Make listening to new music more efficient 

## Training Dataset
- **Manual Curation:** 3 playlists in 'ML' folder (Like/Dislike/Neutral)
- **Dataset Size:** ~191 songs (Like: 82, Dislike: 48, Neutral: 61)
- **Quality Control:** Duplicate detection strategy implemented
- **Labels:** Clean preference classifications for supervised learning

## Data Sources & Why
Spotify is used **only** for playlist structure, labels, and track titles/artists. Acoustic features no longer come from Spotify: the audio-features endpoints are officially **deprecated**, and Spotify's terms now ban training machine-learning models on Spotify content.

Features are fetched from the [GetSongBPM](https://getsongbpm.com) API instead:
- `tempo` (BPM), `time_sig`, `key_of` / `open_key` (mode derivable)
- `danceability`, `acousticness` (0–100, via AcousticBrainz/Essentia)
- Independent of Spotify, so training a personal taste model stays out of Spotify's restricted-data terms.

## Proven Approach
- **Baseline Model:** RandomForest classifier (95% accuracy on synthetic data)
- **Feature Set (GetSongBPM):** danceability, acousticness, tempo, key/mode, time_signature
- **Data Pipeline:** IterativeImputer + LabelEncoder preprocessing approach 

## Tech Stack
- Python
- Jupyter Notebooks
- Spotipy (Spotify Web API client — playlist/label extraction only)
- requests (GetSongBPM API client)
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
│   ├── getsongbpm_client.py          # GetSongBPM feature fetch (planned)
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
5. Add `GETSONGBPM_API_KEY` to `.env` (register at [GetSongBPM](https://getsongbpm.com/api))
6. **Current Focus:** Follow implementation plan in `plan.md`
7. Start with Phase 0: GetSongBPM coverage spike, then Phase 1

## Current Progress
- ✅ Environment & dependencies configured
- ✅ Spotify API credentials established
- ✅ Training dataset curated (~191 songs, 3 preference categories)
- ✅ Data-source pivot documented (Spotify features deprecated → GetSongBPM)
- 🔄 **NEXT:** Phase 0 — GetSongBPM API coverage spike
- ⏸️ Phase 1: API connection and duplicate detection
- ⏸️ Phase 2: Feature collection via GetSongBPM
- ⏸️ Phase 3: Feature exploration and correlation analysis
- ⏸️ Phase 4: Model training and evaluation

## Known Issues
- **Cooldown:** GetSongBPM enforces rate limits (3,000 req/hr); unauthorized requests blocked for 1 hour
- **Coverage risk:** GetSongBPM is a BPM database — matches may be missing for obscure/niche tracks (Phase 0 measures this)
- **Feature set reduced:** GetSongBPM lacks valence/energy/instrumentalness/liveness/speechiness/loudness that the original Spotify plan had

See `plan.md` for detailed resolution strategy.
