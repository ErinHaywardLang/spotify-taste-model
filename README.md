# spotify-taste-model

A personal machine learning project to predict how much I'll like a song and rank Spotify's Discover Weekly and Release Radar playlists.

This is an exploratory learning project where I combine the Spotify Web API with Python and ML techniques to help prioritise which songs to listen to each week. The goal is to eventually connect to Spotify's developer API to automate weekly playlist pulls and rankings.

**Current Status** (2026-01-25): Initial exploratory work underway. **Blocker**: Spotify's developer web API is currently [not accepting new app registrations](https://developer.spotify.com/dashboard), which completely halts direct API integrations. Exploring alternative data sources and audio feature providers to proceed with the project. 

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

## Setup
1. Clone the repo
2. Create and activate a virtual environment 
3. Install dependencies from the pinned list: `pip install -r requirements.txt`
4. Add a `.env` file with your Spotify API credentials (see `.env.example` when credentials become available)
5. Run notebooks or scripts to explore, label, and train models

## Current Progress
- ✅ Environment & dependencies pinned
- 🔄 Exploratory notebook started (initial feature engineering and model prototyping)
- 🚫 **Blocker**: Direct Spotify API integration unavailable—investigating alternative audio data sources
