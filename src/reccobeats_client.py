import re
import time
from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.reccobeats.com"
CHUNK_SIZE = 40  # ReccoBeats caps ids at 40 per request

# Track IDs in version suffix as returned by ReccoBeats hrefs
_SPOTIFY_ID_RE = re.compile(r"/track/([A-Za-z0-9]+)")


class ReccoBeatsError(Exception):
    pass


def track_id_from_href(href):
    """Extract the Spotify track id from a ReccoBeats href."""
    if not href:
        return None
    m = _SPOTIFY_ID_RE.search(href)
    return m.group(1) if m else None


class ReccoBeatsClient:
    """Client for the ReccoBeats audio-features endpoint.

    GET /v1/audio-features?ids=<comma-separated spotify ids>
    No auth required. Returns the classic audio-feature set.

    fetch_all() is resumable: it keeps a CSV cache of already-fetched
    track ids and only queries the missing ones.
    """

    FEATURES = [
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "key",
        "liveness",
        "loudness",
        "mode",
        "speechiness",
        "tempo",
        "valence",
    ]

    def __init__(self, chunk_size=40, sleep=0.5, timeout=30, max_retries=3, retry_wait=2.0):
        self.chunk_size = chunk_size
        self.sleep = sleep
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_wait = retry_wait
        self.session = requests.Session()

    def _get_features(self, ids):
        url = f"{BASE_URL}/v1/audio-features"
        # ReccoBeats accepts Spotify track ids, commas are fine
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(
                    url, params={"ids": ",".join(ids)}, timeout=self.timeout
                )
            except requests.RequestException as exc:
                if attempt == self.max_retries - 1:
                    raise ReccoBeatsError(f"Request failed: {exc}") from exc
                time.sleep(self.retry_wait * (2 ** attempt))
                continue

            if resp.status_code == 200:
                return resp.json().get("content", []) or []

            if resp.status_code in (429, 500, 502, 503):
                wait = self.retry_wait * (2 ** attempt)
                time.sleep(wait)
                continue

            detail = resp.text[:200]
            raise ReccoBeatsError(
                f"ReccoBeats returned {resp.status_code}: {detail}"
            )

        raise ReccoBeatsError(f"Exhausted retries for {ids[:3]}...")

    def fetch_all(self, track_ids, out_csv):
        """Fetch audio features for all track_ids, caching resumable to a CSV.

        Returns a DataFrame keyed by track_id. Missing tracks are dropped.
        """
        out_csv = Path(out_csv)
        out_csv.parent.mkdir(parents=True, exist_ok=True)

        cached = {}
        if out_csv.exists():
            cache = pd.read_csv(out_csv)
            id_col = "track_id"
            for _, row in cache.iterrows():
                cached[row.get(id_col)] = row.to_dict()

        remaining = [tid for tid in track_ids if tid not in cached]
        print(f"{len(track_ids) - len(remaining)} already cached, {len(remaining)} to fetch")

        for i in range(0, len(remaining), self.chunk_size):
            chunk = remaining[i : i + self.chunk_size]
            try:
                items = self._get_features(chunk)
            except ReccoBeatsError as exc:
                print(f"  batch {i // self.chunk_size} failed: {exc}")
                continue

            batch_rows = []
            for item in items:
                tid = track_id_from_href(item.get("href"))
                if not tid:
                    continue
                row = {"track_id": tid}
                for f in self.FEATURES:
                    row[f] = item.get(f)
                row["isrc"] = item.get("isrc")
                cached[tid] = row
                batch_rows.append(row)

            if batch_rows:
                new_df = pd.DataFrame(batch_rows)
                new_df.to_csv(out_csv, mode="a", header=not out_csv.exists(), index=False)

            if self.sleep:
                time.sleep(self.sleep)
            print(f"  fetched {len(batch_rows)} of {len(chunk)} in chunk {i // self.chunk_size + 1}")

        if not remaining:
            return pd.DataFrame()
        return pd.DataFrame([cached[t] for t in remaining if t in cached])

    @staticmethod
    def load_features(csv_path):
        return pd.read_csv(csv_path)