# Spotify Taste Model - Implementation Plan

## Project Overview
Build a personal music preference model using historical listening data from manually curated Spotify playlists to predict song enjoyment and rank new music recommendations.

**Current Status:**
- ✅ Spotify API access configured
- ✅ Proven ML pipeline on GENERATED SAMPLE DATA with 95% accuracy on sample data (RandomForest + IterativeImputer)
- 📊 **Current Dataset:** ~191 songs across 3 playlists (Like: 82, Dislike: 48, Neutral: 61)
- 🔄 **Data-source pivot:** Spotify audio-features endpoints are **deprecated** and Spotify's terms now **prohibit ML/AI training on Spotify content**. Features will come from **GetSongBPM** instead.

## Data Source Decision (CRITICAL — read first)

### Why the pivot?
- **Deprecation:** `GET /audio-features/{id}`, `GET /audio-features?ids=`, and `GET /audio-analysis/{id}` are officially marked **Deprecated** by Spotify. No replacement exists.
- **ToS restriction:** Spotify's terms state Spotify content may not be used "to train a machine learning or AI model." This project's core purpose is training a model on audio-derived signals.
- **ReccoBeats** (tested `GET https://api.reccobeats.com/v1/audio-features?ids=<spotify_ids>`, returns exact Spotify-style features, no auth) is a working shortcut but re-serves Spotify-derived data, so it carries the same ML-training lineage risk and is a single-maintainer service with no SLA.
- **GetSongBPM** (api.getsong.co) computes features independently (tempo/key are its own; danceability/acousticness via AcousticBrainz/Essentia). This keeps training data outside Spotify's restricted-content terms.

**Chosen Stack:** Spotify → track title, artist, playlist labels. **GetSongBPM** → acoustic features.

### What GetSongBPM provides (and what it can't)
| plan.md feature | GetSongBPM |
|---|---|
| danceability | ✅ (0–100 integer, /100) |
| acousticness | ✅ (0–100 integer) |
| tempo | ✅ |
| key / mode | ✅ `key_of` / `open_key` (mode derivable) |
| time_signature | ✅ `time_sig` |
| energy | ❌ |
| valence | ❌ |
| instrumentalness | ❌ |
| liveness | ❌ |
| speechiness | ❌ |
| loudness | ❌ |

### GetSongBPM API facts (verified)
- Base URL: `https://api.getsong.co/`
- Auth: API key via `api_key` URL param or `X-API-KEY` header
- Free tier: 3000 requests/hour; exceeding blocks the key for 1 hour
- Mandatory **backlink** to getsongbpm.com (already added to README)
- No public rate values beyond that; rate limits enforced server-side

---

## Phase 0: GetSongBPM Coverage & Access Spike 🔧

### Priority: HIGH (blocking)

#### Tasks:
1. ⏸️ **Register for API key** at getsongbpm.com/api (backlink to this repo's README)
2. ⏸️ **Add `GETSONGBPM_API_KEY` to `.env`**
3. ⏸️ **Build `getsongbpm_client.py`** — thin wrapper for `/search/` (song: + artist:) and `/song/{id}`
4. ⏸️ **Coverage spike** — run against a ~20-track slice of real playlists
   - Measure **match rate** (how many tracks resolve to a sensible song)
   - Check disambiguation: live versions, covers, remixes, multiple artists
   - Check missing-data patterns (obscure tracks, instrumentals)

#### Success Criteria
- [ ] API key works, no 401s
- [ ] Match rate ≥ 80% on a 20-track slice
- [ ] Confident matching rule documented (e.g. exact title + artist match preferred)

#### Go / No-Go
If match rate < 80%, fall back to discussion: accept lower coverage + imputation, or reconsider ReccoBeats (full 10 features, deprecated-spotify lineage risk).

---

## Phase 1: API Integration & Core Setup 🔧

#### Tasks:
1. ✅ **Fix `src/spotify_client.py`** — cached-token auth flow exists; verify no remaining import errors
2. ⏸️ **Locate target playlists** — find 'Like', 'Dislike', 'Neutral' playlists in 'ML' folder
3. ⏸️ **Extract basic track data** — track_id, title, artist, playlist_name for all songs
4. ⏸️ **Duplicate detection & resolution** — check for identical track_ids across playlists, keep most recent
5. ⏸️ **Validate clean playlist access** — confirm API can read tracks from deduplicated playlists

#### Success Criteria
- Notebook can import and authenticate with Spotify API
- Clean, deduplicated (no cross-playlist dup track_ids), non-conflicting labels
- Ready for bulk feature extraction

---

## Phase 2: Data Collection & Feature Extraction 📊

#### Pipeline: Spotify labels → GetSongBPM features

```
Spotify (Get Playlist Items, non-deprecated)
    → track_id, title, artist[0].name, playlist_name
    ── dedupe (keep most recently placed) ──
GetSongBPM /search/ "song:<title> artist:<artist>"
    → best-match song (score + validate)
GetSongBPM /song/{id}
    → tempo, time_sig, key_of, open_key, danceability, acousticness
Normalize: danceability/100, acousticness/100, key→int, mode→major/minor
Export CSV
```

#### Feature Pipeline
**Final feature set:**
```
['danceability', 'acousticness', 'tempo', 'key', 'mode', 'time_signature']
```

**Additional Metadata:**
- `track_title`, `artist_name`, `track_id`
- `playlist_name` (Like/Dislike/Neutral)
- `user_label` (liked/disliked/neutral)

#### Data Quality Handling:
- **Match scoring:** score candidate matches (title exact, artist match) and keep best; bucket unmatched as `missing`
- **Missing features:** IterativeImputer (proven approach)
- **Duplicate tracks (CRITICAL):** keep song from most recently modified playlist; exact track_id only
- **Rate limits:** 3000 req/hr — ~191 tracks = fine with small sleep; retry with backoff on 429
- **API failures:** retry logic, error logging

#### Tasks:
1. ⏸️ **Build track extractor** — all tracks from three cleaned playlists
2. ⏸️ **GetSongBPM feature fetcher** — search + song for each unique track
3. ⏸️ **Data validation** — missing features, rate-limit handling
4. ⏸️ **Export to CSV** — `data/` datasets

#### Success Criteria
- Combined CSV with unique tracks only
- All 6 features + labels where GetSongBPM has data
- Coverage rate documented per playlist

---

## Phase 3: Feature Exploration & Visualization 🎨

### Priority: MEDIUM

Note: reduced feature set (6 vs the original 10) means fewer dimensions to explore and weaker original "valence/danceability/energy" hypothesis tests. Visualizations now center on danceability/acousticness/tempo/key/mode.

#### Visualization Pipeline
1. **Feature Correlation Heatmap**
2. **Class Distribution Analysis** — box plots of feature range by Like/Dislike/Neutral
3. **Interactive Scatter Plots** ⭐ **User Priority** — color-coded (Like: green, Dislike: red, Neutral: blue)
4. **Feature Importance Analysis** — Random Forest importances

#### Key Questions
- Which features separate liked vs disliked best?
- Do real patterns match the synthetic-data expectations (danceability/acousticness)?
- What audio characteristics define personal taste in this 6-feature space?

---

## Phase 4: ML Pipeline Adaptation 🤖

#### Proven Baseline (synthetic, 95%)
```python
IterativeImputer(random_state=42)
LabelEncoder()  # disliked=0, liked=1, neutral=2
RandomForestClassifier(n_estimators=100, random_state=42)
train_test_split(test_size=0.2, random_state=42)
```

### Adaptations for real, reduced-feature data
- **Smaller dataset (~191, imbalanced)** — cross-validation + stratified sampling
- **Real-world noise** — lower expectations than 95% (fewer features, imperfect label separation)
- **Probability calibration** — better confidence for ranking
- **Feature scaling** — for algorithm exploration beyond RF

#### Evaluation Metrics
Accuracy, Precision, Recall, F1 per class; confusion matrix; CV stability; feature imports.

#### Success Criteria
- ≥ baseline-equivalent or documented lower, with honest expectations set (given 6 features, target ~real-world 70–80% may be more realistic than the synthetic 95%)
- Stable CV
- Saved model

---

## Phase 5: Future Automation 🔄

### Priority: LOW

1. **Discover Weekly / Release Radar extraction** (Spotify — still non-deprecated)
2. **GetSongBPM feature collection** for new tracks
3. **Batch prediction & ranking**
4. Feedback → incremental retraining

---

## Project Structure (target)
```
spotify-taste-model/
├── src/
│   ├── spotify_client.py         # Spotify auth/playlist (labels)
│   ├── getsongbpm_client.py      # GetSongBPM feature fetcher
│   └── data_collector.py         # end-to-end collection
├── notebooks/
│   ├── connect.ipynb
│   ├── 01_data_collection.ipynb
│   ├── 02_feature_exploration.ipynb
│   └── 03_model_training.ipynb
├── data/                         # real datasets + coverage report
├── models/
└── plan.md
```

## Dependencies
- **Existing:** `pandas`, `numpy`, `scikit-learn`, `spotipy`, `python-dotenv`, `requests` (already pinned in requirements.txt)
- **New:** `plotly` (interactive scatter for Phase 3)
- getSongBPM backlink in README (compliant)

## Risks & Open Items
- **GetSongBPM coverage for niche/obscure tracks** — Phase 0 spike answers
- **Feature count reduced** — model likely weaker; acceptance criteria set at Phase 4 to track
- **API stability** — sole-maintainer, free tier, no guarantee; cache features to CSV to reduce re-fetch
- **ML-training compliance** — features come from GetSongBPM's independent analysis, not Spotify audio values; Spotify used only for playlist structure/labels