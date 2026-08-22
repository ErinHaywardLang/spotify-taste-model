import os
import re
import time
from difflib import SequenceMatcher

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.getsong.co"

# Tokens that indicate a version/remaster and should be stripped when comparing titles
_TITLE_NOISE = re.compile(
    r"(\(.*?\)|\bremaster(ed)?\b|\bremaster\b|\blive\b|\bbonus\b|\bmix\b|\bedit\b|\bversion\b|\bsingle\b|\b202\d\b|\b19\d\d\b)",
    re.IGNORECASE,
)


class GetSongBPMError(Exception):
    pass


class GetSongBPMClient:
    """Client for the GetSongBPM API (api.getsong.co).

    Search returns full song features in one call:
    tempo, time_sig, key_of, open_key, danceability (0-100), acousticness (0-100).
    """

    def __init__(self, api_key=None, timeout=15, max_retries=3, retry_wait=2.0):
        self.api_key = api_key or os.getenv("GETSONGBPM_API_KEY")
        if not self.api_key:
            raise GetSongBPMError(
                "GETSONGBPM_API_KEY not set. Add it to your .env file."
            )
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_wait = retry_wait
        self.session = requests.Session()

    def _get(self, endpoint, params):
        url = f"{BASE_URL}/{endpoint}"
        params = {**params, "api_key": self.api_key}

        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as exc:
                if attempt == self.max_retries - 1:
                    raise GetSongBPMError(f"Request failed for {url}: {exc}") from exc
                time.sleep(self.retry_wait * (2 ** attempt))
                continue

            if resp.status_code == 200:
                return resp.json()

            if resp.status_code == 429:
                time.sleep(self.retry_wait * (2 ** attempt))
                continue

            detail = resp.text[:200]
            raise GetSongBPMError(
                f"GetSongBPM returned {resp.status_code} for {url}: {detail}"
            )

        raise GetSongBPMError(f"Exhausted retries for {url}")

    def search_by_title(self, title, limit=5):
        """Search songs by title only (type=song). Returns list of raw song dicts."""
        data = self._get("search/", {"type": "song", "lookup": title, "limit": limit})
        results = data.get("search", []) or []
        return results if isinstance(results, list) else []

    def search_song_artist(self, title, artist, limit=5):
        """Search by song: title + artist: artist (type=both)."""
        lookup = f"song:{title} artist:{artist}"
        data = self._get("search/", {"type": "both", "lookup": lookup, "limit": limit})
        results = data.get("search", []) or []
        return results if isinstance(results, list) else []

    def best_match(self, title, artist=None, threshold=0.55):
        """Find the best GetSongBPM song for a Spotify track.

        Strategy:
          1. type=both with song:+artist: (most precise)
          2. fallback type=song title-only, ranked by min(title, artist)
             similarity when an artist is known (artist gate), else title
             similarity.

        Returns a raw song dict, or None.
        """
        norm_title = normalize_title(title)
        norm_artist = _normalize_name(artist)

        if artist:
            results = self.search_song_artist(title, artist)
            if results:
                return results[0]

        results = self.search_by_title(title)
        if not results and norm_title and norm_title != title:
            results = self.search_by_title(norm_title)

        best = None
        best_score = 0.0
        for raw in results:
            cand_artist = (raw.get("artist") or {}).get("name") or ""
            title_score = _title_score(norm_title, normalize_title(raw.get("title") or ""))
            if norm_artist:
                artist_score = _name_score(norm_artist, cand_artist)
                # artist is a hard gate: both must be reasonably high
                score = min(title_score, artist_score)
            else:
                score = title_score
            if score > best_score:
                best_score = score
                best = raw

        return best if best_score >= threshold else None


def normalize_title(value):
    """Normalize a title for matching: lowercase, strip parentheticals
    and version/noise tokens (remaster, live, bonus, mix, year...)."""
    cleaned = _TITLE_NOISE.sub("", value or "")
    return re.sub(r"[^a-z0-9 ]", " ", cleaned.lower()).strip()


def _normalize_name(value):
    if not value:
        return ""
    return re.sub(r"[^a-z0-9 ]", " ", value.lower()).strip()


def _name_score(a, b):
    a, b = _normalize_name(a), _normalize_name(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _title_score(norm_title, norm_cand):
    if not norm_title or not norm_cand:
        return 0.0
    if norm_title == norm_cand:
        return 1.0
    return SequenceMatcher(None, norm_title, norm_cand).ratio()


def normalize_song(raw):
    """Convert a raw GetSongBPM song dict into a flat feature dict.

    danceability/acousticness are 0-100 integers -> 0.0-1.0 floats.
    tempo is a string (may carry 'bpm' suffix).
    """
    def _key_mode(key_of):
        key_of = (key_of or "").strip()
        mode = "minor" if key_of.endswith("m") else "major"
        return key_of, mode

    if not raw:
        return None

    key_of, mode = _key_mode(raw.get("key_of"))

    tempo = raw.get("tempo")
    if tempo is not None:
        tempo = str(tempo).lower().replace("bpm", "").strip()

    return {
        "title": raw.get("title"),
        "artist": (raw.get("artist") or {}).get("name"),
        "song_uri": raw.get("uri"),
        "tempo": float(tempo) if _is_float(tempo) else None,
        "time_sig": raw.get("time_sig"),
        "key_of": key_of,
        "mode": mode,
        "danceability": _to_unit(raw.get("danceability")),
        "acousticness": _to_unit(raw.get("acousticness")),
        "genres": (raw.get("artist") or {}).get("genres") or [],
        "album_year": (raw.get("album") or {}).get("year"),
        "album_title": (raw.get("album") or {}).get("title"),
    }


def _is_float(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _to_unit(value):
    """Map 0-100 integer (e.g. 58) to 0.0-1.0 float."""
    if value is None or not _is_float(value):
        return None
    return float(value) / 100.0