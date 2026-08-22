"""Phase 0 coverage spike: GetSongBPM match-rate sanity check on real playlists.

Pulls a small stratified sample of tracks from the Like/Neutral/Dislike
playlists via Spotify, looks each one up in GetSongBPM, and prints a
match report. Used to decide whether to commit to GetSongBPM as the
feature source.
"""
import json
import random
import sys
import urllib.request
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.getsongbpm_client import GetSongBPMClient, GetSongBPMError, normalize_song
from src.spotify_client import get_spotify_client

PLAYLISTS = {
    "Like": "2VGNDXi2HO5rDCtFfdgaA2",
    "Neutral": "2so4nUGUWi305tYS2NVrnm",
    "Dislike": "0KseX0ZufmhqOCdBujgrHO",
}

SAMPLE_PER_PLAYLIST = 7
RANDOM_SEED = 42


def _spotify_get(sp, url):
    """Raw GET against the Spotify API using the authed client's token."""
    token = sp._auth_headers()["Authorization"].split()[1]
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def get_spotify_tracks(sp, playlist_id, n):
    """Return a random sample of up to n track dicts from a playlist."""
    # New Spotify /items endpoint (the old /tracks is deprecated/403s).
    all_items = []
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items?limit=100"
    while url:
        page = _spotify_get(sp, url)
        all_items.extend(page["items"])
        url = page.get("next")

    random.seed(RANDOM_SEED)
    sample = random.sample(all_items, min(n, len(all_items)))
    records = []
    for entry in sample:
        item = entry.get("item") or {}
        if item.get("type") != "track":
            continue
        records.append(
            {
                "track_id": item["id"],
                "title": item["name"],
                "artist": item["artists"][0]["name"] if item["artists"] else None,
                "album": (item.get("album") or {}).get("name"),
            }
        )
    return records


def main():
    sp = get_spotify_client()
    client = GetSongBPMClient()

    all_rows = []
    all_tracks = []

    for label, pid in PLAYLISTS.items():
        tracks = get_spotify_tracks(sp, pid, SAMPLE_PER_PLAYLIST)
        all_tracks.extend((label, t) for t in tracks)

    print(f"Spike: {len(all_tracks)} tracks across playlists\n")

    matched = 0
    for label, t in all_tracks:
        try:
            best_raw = client.best_match(t["title"], t["artist"], threshold=0.55)
            best = normalize_song(best_raw) if best_raw else None
        except GetSongBPMError as exc:
            print(f"[ERR ] {label:7s} {t['title']!r} by {t['artist']!r} -> {exc}")
            best = None

        if best:
            matched += 1
            status = "MATCH"
        else:
            status = "MISS"

        title_marker = ""
        if best and best["title"].strip().lower() != t["title"].strip().lower():
            title_marker = f"  [GSB={best['title']!r}]"
        best_artist = (best or {}).get("artist") or "N/A"
        best_tempo = (best or {}).get("tempo")
        best_dance = (best or {}).get("danceability")
        print(
            f"[{status:4s}] {label:7s} {t['title'][:34]:34s} "
            f"| {best_artist:<16s}"
            f" | tempo={best_tempo if best_tempo is not None else '-':<6}"
            f" | dance={best_dance if best_dance is not None else '-'}"
            f"{title_marker}"
        )
        row = {
            "label": label,
            "track_id": t["track_id"],
            "spotify_title": t["title"],
            "spotify_artist": t["artist"],
            "status": status,
            "gsb_title": best["title"] if best else None,
            "gsb_artist": best["artist"] if best else None,
            "gsb_tempo": best["tempo"] if best else None,
            "gsb_danceability": best["danceability"] if best else None,
            "gsb_acousticness": best["acousticness"] if best else None,
        }
        all_rows.append(row)

    out = PROJECT_ROOT / "data" / "phase0_spike_results.csv"
    out.parent.mkdir(exist_ok=True)
    pd.DataFrame(all_rows).to_csv(out, index=False)

    miss_count = len(all_tracks) - matched
    print(f"\nmatched: {matched}/{len(all_tracks)}  ({(matched/len(all_tracks))*100:.1f}%)")
    print(f"miss:    {miss_count}/{len(all_tracks)}")
    print(f"\nreport saved to {out}")


if __name__ == "__main__":
    main()