"""Phase 1+2: collect full Like/Neutral/Dislike tracks and audio features.

Pipeline:
  Spotify /items (pagination) -> (track_id, title, artist, album, added_at)
  Dedupe across playlists: keep most recently added track_id
  ReccoBeats /audio-features by track_id (chunked, resumable) -> features
  Merge -> data/spotify_taste_dataset.csv + data/features_cache.csv
"""
import json
import sys
import urllib.request
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
DATA_DIR = PROJECT_ROOT / "data"

from src.reccobeats_client import ReccoBeatsClient
from src.spotify_client import get_spotify_client

PLAYLISTS = {
    "Like": "2VGNDXi2HO5rDCtFfdgaA2",
    "Neutral": "2so4nUGUWi305tYS2NVrnm",
    "Dislike": "0KseX0ZufmhqOCdBujgrHO",
}


def _spotify_get(sp, url):
    token = sp._auth_headers()["Authorization"].split()[1]
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def load_playlist_tracks(sp, playlist_id, label):
    """All non-local track entries from a playlist via the /items endpoint."""
    records = []
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items?limit=100"
    while url:
        page = _spotify_get(sp, url)
        for entry in page["items"]:
            item = entry.get("item") or {}
            if item.get("type") != "track":
                continue
            artists = [a.get("name") for a in (item.get("artists") or [])]
            records.append(
                {
                    "track_id": item["id"],
                    "title": item["name"],
                    "artist": artists[0] if artists else None,
                    "artist_all": " / ".join(artists),
                    "album": (item.get("album") or {}).get("name"),
                    "added_at": entry.get("added_at"),
                    "playlist_name": label,
                    "user_label": label.lower(),
                }
            )
        url = page.get("next")
    return records


def dedupe_tracks(records):
    """Keep the most recently added track across playlists (exact track_id)."""
    df = pd.DataFrame(records)
    df["added_at"] = pd.to_datetime(df["added_at"], utc=True, errors="coerce")
    df = df.sort_values("added_at")
    deduped = df.drop_duplicates(subset="track_id", keep="last")
    # Report cross-playlist duplicates
    dupes = df.duplicated(subset="track_id", keep=False)
    n_dupes = int(dupes.sum())
    print(f"raw rows: {len(df)} | cross-playlist duplicate rows: {n_dupes}")
    return deduped.reset_index(drop=True)


def main():
    sp = get_spotify_client()
    features_csv = DATA_DIR / "features_cache.csv"
    dataset_csv = DATA_DIR / "spotify_taste_dataset.csv"

    all_records = []
    for label, pid in PLAYLISTS.items():
        recs = load_playlist_tracks(sp, pid, label)
        print(f"{label}: {len(recs)} tracks")
        all_records.extend(recs)

    tracks = dedupe_tracks(all_records)
    print(f"unique tracks: {len(tracks)}")
    print(tracks.groupby("playlist_name").size())

    client = ReccoBeatsClient(chunk_size=40, sleep=0.5)
    features = client.fetch_all(tracks["track_id"].tolist(), features_csv)

    if features.empty:
        print("no features fetched!")
        return

    features = features.set_index("track_id")
    dataset = tracks.set_index("track_id").join(features, how="left").reset_index()

    dataset.to_csv(dataset_csv, index=False)
    print(f"\ndataset saved: {dataset_csv}")
    covered = dataset[dataset["tempo"].notna()]
    print(f"total tracks: {len(dataset)} | with features: {len(covered)} "
          f"({100 * len(covered) / len(dataset):.1f}%)")
    print(dataset[["title", "artist", "playlist_name", "danceability", "energy", "valence"]].head(10).to_string())


if __name__ == "__main__":
    main()