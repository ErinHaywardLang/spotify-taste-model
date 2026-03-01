# spotify-taste-model

A personal machine learning project to predict how much I'll like a song and rank Spotify's Discover Weekly and Release Radar playlists.

This is an exploratory learning project where I combine the Spotify Web API with Python and ML techniques to help prioritise which songs to listen to each week. The goal is to eventually connect to Spotify's developer API to automate weekly playlist pulls and rankings.

**Current Status** (2026-03-01): Spotify API access established! Initial exploratory work and API integration development underway. 

## Goals
- Build a personal music preference model using historical listening data
- Pull weekly Spotify playlists (Discover Weekly, Release Radar)
- Score and rank songs based on predicted enjoyment
- Make listening to new music more efficient 

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
├── requirements.txt                   # Python dependencies
├── src/
│   ├── __init__.py                   # Package initialization
│   └── spotify_client.py             # Spotify API client configuration
├── notebooks/
│   ├── connect.ipynb                 # Main exploratory notebook
│   └── sample data [old]/            # Archive of older analysis
│       ├── 00_sample_data.ipynb
│       ├── 01_explore_spotify_data.ipynb
│       ├── 02_messy_sample_spotify_data.ipynb
│       ├── 03_explore_spotify_data_messy.ipynb
│       ├── sample_spotify_likes_dataset_large.csv
│       └── sample_spotify_likes_dataset_noisy.csv
└── models/                            # Trained models (TBD)
```

## Setup
1. Clone the repo
2. Create and activate a virtual environment 
3. Install dependencies from the pinned list: `pip install -r requirements.txt`
4. Add a `.env` file with your Spotify API credentials (see `.env.example` when credentials become available)
5. Run notebooks or scripts to explore, label, and train models

## Current Progress
- ✅ Environment & dependencies pinned
- ✅ Spotify API access configured
- 🔄 Exploratory notebook started (initial feature engineering and model prototyping)
- 🔄 API integration and data pulling from Spotify playlists
