# Spotify Taste Model - Implementation Plan

## Project Overview
Build a personal music preference model using historical listening data from manually curated Spotify playlists to predict song enjoyment and rank new music recommendations.

**Current Status:** 
- ✅ Spotify API access configured
- ✅ Proven ML pipeline on GENERATED SAMPLE DATA with 95% accuracy on sample data (RandomForest + IterativeImputer)
- 📊 **Current Dataset:** Songs across 3 playlists (Like, Neutral, Dislike)

## Core Goals
1. **Feature Exploration:** Understand which Spotify audio features correlate with personal music preferences
2. **Visualization:** Create color-coded scatter plots to visualize feature relationships across like/dislike/neutral preferences  
3. **Model Training:** Adapt proven ML pipeline to work with real playlist data
4. **Future Automation:** Weekly playlist ranking for Discover Weekly/Release Radar

---

## Phase 1: API Integration & Core Setup 🔧

#### Tasks:
3. ⏸️ **Locate target playlists** - Find 'Like', 'Dislike', 'Neutral' playlists in 'ML' folder
4. ⏸️ **Extract basic track data** - Get track_id and playlist_name for all songs
5. ⏸️ **Duplicate detection & resolution** - Check for identical track_ids across playlists, keep most recent
6. ⏸️ **Validate clean playlist access** - Confirm API can read tracks from deduplicated playlists

#### Success Criteria:
- Notebook can successfully import and authenticate with Spotify API
- Can list and access tracks from the three target playlists
- **Data integrity confirmed** - No duplicate track_ids across playlists
- Ready for bulk feature extraction with clean, non-conflicting labels

---

## Phase 2: Data Collection & Feature Extraction 📊

#### Data Collection Strategy
**Target Playlists:**
- Folder: 'ML' 
- Playlists: 'Like', 'Dislike', 'Neutral'

#### Feature Extraction Pipeline
**Core Audio Features (Proven Successful):**
```
['danceability', 'energy', 'valence', 'acousticness', 
 'instrumentalness', 'liveness', 'speechiness', 
 'tempo', 'loudness', 'mode']
```

**Additional Metadata:**
- `track_name`, `artist_name`, `album_name`
- `duration_ms`, `popularity`, `key`
- `playlist_name` (Like/Dislike/Neutral)
- `user_label` (liked/disliked/neutral)

#### Tasks:
1. ⏸️ **Validate data integrity** - Confirm no duplicate track_ids remain after Phase 1 resolution
2. ⏸️ **Build track extractor** - Pull all tracks from the three cleaned playlists
3. ⏸️ **Implement feature fetcher** - Get audio features for each unique track
4. ⏸️ **Data validation** - Handle missing features, API rate limits
5. ⏸️ **Export to CSV** - Save combined dataset for analysis

#### Data Quality Handling:
- **Duplicate tracks (CRITICAL):** Check for identical track_ids across playlists
  - Resolution strategy: Keep song from most recently modified playlist
  - Rationale: Most recent placement represents current preference 
  - Scope: Only exact track_id matches (ignore different versions/remixes)
- Missing audio features: Use IterativeImputer (proven approach)
- Duplicate tracks within playlists: Remove or flag appropriately  
- API failures: Retry logic and error logging

#### Success Criteria:
- Combined dataset with unique tracks only (no cross-playlist duplicates)
- All 10 core audio features present
- Three classes with clean, non-conflicting labels (like/dislike/neutral)
- Clean CSV ready for analysis

---

## Phase 3: Feature Exploration & Visualization 🎨

### Priority: MEDIUM (User's Primary Interest)

#### Correlation Analysis Goals
**Primary Objectives:**
- Identify which audio features best separate liked vs disliked songs
- Visualize feature relationships and clustering patterns
- Compare real preference patterns vs sample data insights

#### Visualization Pipeline
1. **Feature Correlation Heatmap**
   - Audio feature intercorrelations
   - Identify multicollinear features
   
2. **Class Distribution Analysis**
   - Feature distributions by preference class
   - Box plots showing feature ranges per class
   
3. **Interactive Scatter Plots** ⭐ **User Priority**
   - Color-coded by preference (Like: green, Dislike: red, Neutral: blue)
   - Any feature X vs feature Y combination
   - Pattern identification and cluster analysis

4. **Feature Importance Analysis**
   - Random Forest feature importance scores
   - Comparison with sample data patterns
   - Ranking of most predictive features

#### Key Questions to Answer:
- Which features show clearest separation between liked/disliked?
- Do real preferences match sample data patterns (valence, danceability, energy)?
- Are there unexpected feature correlations?
- What audio characteristics define personal taste?

#### Tasks:
1. ⏸️ **Exploratory Data Analysis** - Basic statistics and distributions
2. ⏸️ **Correlation matrix** - Feature relationships and multicollinearity
3. ⏸️ **Class separation analysis** - Statistical differences between preference groups
4. ⏸️ **Interactive visualization framework** - Flexible scatter plotting
5. ⏸️ **Feature importance extraction** - From trained models
6. ⏸️ **Insight documentation** - Key findings and patterns

#### Success Criteria:
- Clear visual understanding of feature-preference relationships
- Identification of most discriminative features
- Interactive exploration capability for any feature pair
- Documented insights about personal music taste patterns

---

## Phase 4: ML Pipeline Adaptation 🤖

### Priority: MEDIUM

#### Proven Baseline Approach
**From Sample Data Success (95% accuracy):**
```python
# Preprocessing
IterativeImputer(random_state=42)  # Handle missing values
LabelEncoder()  # Target encoding (disliked=0, liked=1, neutral=2)

# Model
RandomForestClassifier(n_estimators=100, random_state=42)

# Evaluation
train_test_split(test_size=0.2, random_state=42)
classification_report, accuracy_score
```

#### Adaptations for Real Data
**Dataset Size Considerations:**
- Smaller dataset (~178-232 vs 300 sample songs)
- Potentially unbalanced classes
- Real-world noise and feature variations

**Enhanced Pipeline:**
1. **Cross-validation** - For robust evaluation with limited data
2. **Stratified sampling** - Maintain class balance in splits
3. **Feature scaling** - For algorithm exploration beyond Random Forest
4. **Probability calibration** - Better confidence scores for ranking

#### Tasks:
1. ⏸️ **Adapt preprocessing pipeline** - Real data → model-ready format
2. ⏸️ **Implement baseline model** - RandomForest with proven parameters
3. ⏸️ **Add cross-validation** - K-fold evaluation for robustness
4. ⏸️ **Performance benchmarking** - Compare to 95% sample data accuracy
5. ⏸️ **Feature importance analysis** - Real vs sample data comparison
6. ⏸️ **Model persistence** - Save trained models for reuse

#### Evaluation Metrics:
- Accuracy, Precision, Recall, F1-score per class
- Confusion matrix for error analysis
- Feature importance rankings
- Cross-validation stability

#### Success Criteria:
- Model performance ≥80% accuracy (accounting for real-world complexity)
- Stable cross-validation results
- Clear feature importance insights
- Saved models ready for prediction

---

## Phase 5: Future Automation 🔄

### Priority: LOW (Future Enhancement)

#### Weekly Playlist Ranking System
1. **Discover Weekly/Release Radar extraction**
2. **Automated feature collection**
3. **Batch prediction and ranking**
4. **Results export/integration**

#### Model Improvement Pipeline
1. **Feedback collection system**
2. **Incremental model updates**
3. **Performance monitoring**
4. **Automated retraining**

---

## Technical Stack Confirmation

### Dependencies (Already Installed)
- **Data:** `pandas`, `numpy`
- **ML:** `scikit-learn` (RandomForest, IterativeImputer, LabelEncoder)
- **API:** `spotipy`, `python-dotenv`
- **Viz:** `matplotlib`, `seaborn` (consider `plotly` for interactivity)
- **Environment:** Jupyter notebooks, Python 3.11

### Project Structure
```
spotify-taste-model/
├── src/
│   ├── spotify_client.py     # API integration (needs fix)
│   └── data_collector.py     # New: Playlist data extraction
├── notebooks/
│   ├── connect.ipynb         # Current: broken API test
│   ├── 01_data_collection.ipynb    # New: Extract playlist data
│   ├── 02_feature_exploration.ipynb # New: Correlation & visualization
│   └── 03_model_training.ipynb     # New: ML pipeline adaptation
├── data/                     # New: Real playlist datasets
├── models/                   # New: Trained model storage
└── plan.md                   # This document
```

---

## Key Decisions & Questions

### Dataset Size Strategy
**Current:** 191 songs total (Like: 82, Dislike: 48, Neutral: 61)
**Critical Check:** Ensure no duplicate track_ids exist across preference categories
**Options:**
1. Proceed with deduplicated dataset for initial exploration
2. Expand playlists after understanding baseline performance
3. Focus on data quality and label consistency over quantity

### Visualization Priority 
**User Request:** Interactive scatter plots with color-coded preferences
**Implementation Options:**
1. Static matplotlib/seaborn plots (faster development)
2. Interactive plotly plots (better exploration)
3. Both approaches

### Feature Focus
**Sample Data Leaders:** Valence, danceability, energy
**Question:** Start with these proven features or explore full feature set?

---

## Success Metrics

### Phase Completion Criteria:
- **Phase 1:** ✅ Working API connection and playlist access
- **Phase 2:** ✅ Clean dataset with all target features  
- **Phase 3:** ✅ Clear feature-preference insights with visualizations
- **Phase 4:** ✅ Trained model with ≥80% accuracy
- **Phase 5:** 🔄 Automated weekly ranking system

### Overall Project Success:
1. **Understanding gained:** Clear insights into personal music taste patterns
2. **Model performance:** Reliable preference prediction (≥80% accuracy)
3. **Practical utility:** Ability to rank new songs by predicted enjoyment
4. **Foundation built:** Scalable system for ongoing music discovery
