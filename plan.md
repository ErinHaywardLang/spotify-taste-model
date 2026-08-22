# Spotify Taste Model - Implementation Plan

## Project Overview
Build a personal music preference model using historical listening data from manually curated Spotify playlists to predict song enjoyment and rank new music recommendations.

**Current Status:**
- ✅ Spotify API access configured
- ✅ Proven ML pipeline on GENERATED SAMPLE DATA with 95% accuracy on sample data (RandomForest + IterativeImputer)
- 📊 **Current Dataset:** 304 unique tracks across 3 playlists (Like: 105, Neutral: 100, Dislike: 99)
- ✅ **Feature extraction complete:** 242/304 (79.6%) tracks have ReccoBeats features
- 🔄 **Data source:** Spotify audio-features endpoints are **deprecated** + Spotify's terms now **prohibit ML/AI training on Spotify content**. Features come from **ReccoBeats** (multi-phase comparison decided this).

## Data Source Decision (CRITICAL — read first)

### Why the pivot away from Spotify audio features?
- **Deprecation:** `GET /audio-features/{id}`, `GET /audio-features?ids=`, and `GET /audio-analysis/{id}` are officially marked **Deprecated** by Spotify. No replacement exists.
- **ToS restriction:** Spotify's terms state Spotify content may not be used "to train a machine learning or AI model." This project's core purpose is training a model on audio-derived signals.

### Candidate alternatives (tested)
| Source | Endpoint | Coverage (real spike) | Feature set | Notes |
|---|---|---|---|---|
| **ReccoBeats** ✅ | `GET /v1/audio-features?ids=` | **18/21 (86%)** | Full (dance, energy, valence, acousticness, instrumentalness, liveness, speechiness, tempo, loudness, key, mode) | No auth; max 40 ids/req; resumable CSV cache in `src/reccobeats_client.py` |
| GetSongBPM | `GET /search/` (api key) | 7/21 (@33%) | Reduced (tempo, key, mode, danceability, acousticness) | Skews mainstream; misses indie/electronic/newer |
| Spotify deprecated | `GET /audio-features?ids=` | ~100% | Full | Deprecated + ToS-ban |

**Decision:** **ReccoBeats** is the primary audio-feature source. It matches Spotify's catalog by design (same record labels/ISRC), giving the best coverage for a personal, indie-heavy taste. GetSongBPM retains an optional cross-reference; its free API key registration required a backlink (kept in README).

> Note on ToS: ReccoBeats re-serves Spotify-derived data (its own ToS says base metadata is aggregated from Spotify and the user is responsible for third-party compliance). This is a personal project; accepted as low-risk relative to the benefit. Cache aggressively, keep coverage metrics, and revisit if the service direction changes.

### ReccoBeats API facts (verified)
- Base URL: `https://api.reccobeats.com/v1`
- Auth: none required
- `GET /audio-features?ids=<comma> <comma>` → up to **40** ids/req
- Response: `content[]` with original features + `isrc` + `href` (open.spotify.com/track/<id>)
- No documented rate limit; 429 → retry with backoff
- Single-maintainer, "as-is", may shut down anytime; **cache features to CSV** to be safe

---

## Phase 0: Data-Source Spike ✅ DONE

- Registered GetSongBPM API key (backlink added to README)
- Built `src/getsongbpm_client.py` + spike script `00_getsongbpm_spike.py`
- Ran 21-track spike across Like/Neutral/Dislike:
  - GetSongBPM: **7/21 (33%)**
  - ReccoBeats: **18/21 (86%)**
- Decision: **ReccaBeats** (see table above)
- Output: `data/phase0_spike_results.csv`

---

## Phase 1: API Integration & Core Setup 🔧 ✅ DONE

#### Tasks (done)
- ✅ Authenticate with Spotify (cached token in `src/spotify_client.py`)
- ✅ Locate target playlists: Like `2VGNDXi2HO5rDCtFfdgaA2`, Neutral `2so4nUGUWi305tYS2NVrnm`, Dislike `0KseX0ZufmhqOCdBujgrHO`
- ✅ Extract basic track data (track_id, title, artist, album, added_at)
- ✅ **Key finding:** Spotify's old `/playlists/{id}/tracks` endpoint now **403s**; the new **`/items`** endpoint must be used
- ✅ Duplicate detection & resolution (keep most recently added)

#### Success Criteria (met)
- Notebook can import/authenticate with Spotify API
- Clean, deduplicated, non-conflicting labels
- Ready for bulk feature extraction

---

## Phase 2: Data Collection & Feature Extraction 📊 ✅ DONE

#### Pipeline: Spotify labels → ReccoBeats features
```
Spotify /playlists/{id}/items (paginated)
    → (track_id, title, artist, album, added_at)
    → dedupe across playlists (keep most recently added)
ReccoBeats GET /v1/audio-features?ids=<chunk of 40>
    → full feature set keyed by track id
Merge → data/spotify_taste_dataset.csv
```

## Feature Set (ReccaBeats, restored to original 10-feature plan)
```
['danceability', 'energy', 'valence', 'acousticness',
 'instrumentalness', 'liveness', 'speechiness',
 'tempo', 'loudness', 'key', 'mode']
```

**Additional Metadata:** `track_id`, `title`, `artist`, `album`, `playlist_name`, `user_label` (liked/disliked/neutral)

#### Tasks (done)
1. ✅ `src/reccobeats_client.py` — chunked, retry, resumable CSV cache
2. ✅ `notebooks/01_data_collection.py` — full pipeline
3. ✅ Export `data/features_cache.csv` (resumable) + `data/spotify_taste_dataset.csv`

#### Data Quality Handling
- **Duplicate tracks (CRITICAL):** keep song from most recent `added_at`; exact `track_id` only
- **Missing features:** ~20% of tracks (obscure/new) lack ReccoBeats data → impute with IterativeImputer or drop (decide in Phase 3/4)
- **ReccoBeats limits:** 40 ids/req; resumable cache; retry/backoff
- **Future growth:** increase playlist sizes to raise dataset/coverage, re-run collector (cache only fetches new ids)

#### Results
- 304 unique tracks (Like: 105, Neutral: 100, Dislike: 99)
- 242/304 (79.6%) with features

---

## Phase 3: Feature Exploration & Visualization 🎨

### Priority: MEDIUM

#### Visualization Pipeline
1. **Feature Correlation Heatmap**
2. **Class Distribution Analysis** — box plots by Like/Dislike/Neutral
3. **Interactive Scatter Plots** ⭐ **User Priority** — color-coded (Like: green, Dislike: red, Neutral: blue)
4. **Feature Importance Analysis** — Random Forest importances

#### Key Questions
- Which features separate liked vs disliked best?
- Do real patterns match earlier synthetic-data expectations (valence/danceability/energy)?
- Which features best separate this user's taste?

---

## Phase 4: ML Pipeline Adaptation 🤖

#### Proven Baseline (synthetic, 95%)
```python
IterativeImputer(random_state=42)
LabelEncoder()        # disliked=0, liked=1, neutral=2
RandomForestClassifier(n_estimators=100, random_state=42)
train_test_split(test_size=0.2, random_state=42)
```

#### Adaptations for real data
- **Smaller, imbalanced classes** — cross-validation + stratified sampling
- **Real-world noise / ~20% missing** — IterativeImputer; expect < synthetic 95%
- **Probability calibration** — better confidence for ranking

#### Evaluation Metrics
Accuracy, Precision, Recall, F1 per class; confusion matrix; CV stability; feature importances.

#### Success Criteria
- Documented honest performance (target ~70-85%, given real-world noise)
- Stable CV
- Saved model

---

## Phase 5: Future Automation 🔄

### Priority: LOW

1. **Discover Weekly / Release Radar extraction** (Spotify `/items` — still non-deprecated)
2. **ReccoBeats feature collection** for new tracks (reuses cache)
3. **Batch prediction & ranking**
4. Feedback loop → incremental retraining

---

## Project Structure (target)
```
spotify-taste-model/
├── src/
│   ├── spotify_client.py         # Spotify auth/playlists
│   ├── reccobeats_client.py      # ReccoBeats features (primary) ✅
│   ├── getsongbpm_client.py      # GetSongBPM (optional cross-reference)
│   └── data_collector.py         # (planned consolidation)
├── notebooks/
│   ├── connect.ipynb
│   ├── 00_getsongbpm_spike.py    # Phase 0 coverage spike
│   ├── 01_data_collection.py     # ✅ Phase 1+2
│   ├── 02_feature_exploration.py # Phase 3 (planned)
│   └── 03_model_training.py      # Phase 4 (planned)
├── data/
│   ├── features_cache.csv          # ✅ ReccoBeats resumable cache
│   ├── spotify_taste_dataset.csv   # ✅ merged labeled dataset
│   └── phase0_spike_results.csv    # ✅ spike comparison
├── models/
└── plan.md
```

## Dependencies
- **Existing:** `pandas`, `numpy`, `scikit-learn`, `spotipy`, `python-dotenv`, `requests`
- **New:** `plotly` (interactive scatter, Phase 3)

## Risks & Open Items
- **ReccaBeats reliability:** 18/21 spike → 79.6% real coverage; cache mitigates re-fetch costs; if service drops, revisit Spotify/local-audio path
- **Feature coverage gap (~20%):** decide impute-vs-drop by label balance in Phase 3/4
- **ML-training lineage:** ReccoBeats serves Spotify-derived data; accepted for personal use
- **GetSongBPM backlink** kept in README (required for the registered API key)