"""
Track metadata reader — reads ID3, FLAC, Vorbis, and MP4 tags using mutagen.
Falls back to filename-parsing when mutagen is unavailable.
"""
from __future__ import annotations

import json
import logging
import os
import re

logger = logging.getLogger(__name__)

_CACHE_PATH = os.path.expanduser("~/.violet_dj/metadata_cache.json")
_cache: dict = {}
_cache_loaded = False

try:
    import mutagen
    from mutagen.easyid3 import EasyID3
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.oggvorbis import OggVorbis
    from mutagen.mp4 import MP4
    _MUTAGEN = True
except ImportError:
    _MUTAGEN = False
    logger.info("mutagen unavailable — using filename-based metadata only")


# ── Cache ─────────────────────────────────────────────────────────────────────

def _load_cache() -> None:
    global _cache, _cache_loaded
    if _cache_loaded:
        return
    try:
        if os.path.exists(_CACHE_PATH):
            with open(_CACHE_PATH) as f:
                _cache = json.load(f)
    except Exception:
        _cache = {}
    _cache_loaded = True


def _save_cache() -> None:
    try:
        os.makedirs(os.path.dirname(_CACHE_PATH), exist_ok=True)
        with open(_CACHE_PATH, "w") as f:
            json.dump(_cache, f, indent=2)
    except Exception as e:
        logger.warning(f"Metadata cache save failed: {e}")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_filename(path: str) -> dict:
    """Extract title/artist from 'Artist - Title.mp3' pattern."""
    name = os.path.splitext(os.path.basename(path))[0]
    if " - " in name:
        parts = name.split(" - ", 1)
        return {"title": parts[1].strip(), "artist": parts[0].strip()}
    return {"title": name, "artist": "Unknown Artist"}


def _safe_str(value, default: str = "") -> str:
    if not value:
        return default
    if isinstance(value, (list, tuple)):
        value = value[0] if value else default
    return str(value).strip() or default


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(str(value[0]) if isinstance(value, (list, tuple)) else value)
    except (ValueError, TypeError, IndexError):
        return default


def format_duration(seconds: float) -> str:
    """Format seconds as M:SS or H:MM:SS."""
    if seconds <= 0:
        return "--:--"
    secs = int(seconds)
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


# ── Public API ────────────────────────────────────────────────────────────────

def read_metadata(file_path: str) -> dict:
    """Return a metadata dict for *file_path*.  Uses on-disk cache."""
    _load_cache()
    if file_path in _cache:
        return _cache[file_path]

    info: dict = {
        "title":   "",
        "artist":  "",
        "album":   "",
        "duration": 0.0,
        "bpm":     0.0,
        "key":     "",
        "format":  "",
        "bitrate": 0,
    }
    fn = _parse_filename(file_path)
    info.update(fn)
    ext = os.path.splitext(file_path)[1].lstrip(".").lower()
    info["format"] = ext.upper()

    if _MUTAGEN and os.path.exists(file_path):
        try:
            if ext == "mp3":
                audio = MP3(file_path, ID3=EasyID3)
                info["duration"] = audio.info.length
                info["bitrate"]  = getattr(audio.info, "bitrate", 0) // 1000
                tags = audio.tags or {}
                info["title"]  = _safe_str(tags.get("title"),  fn["title"])
                info["artist"] = _safe_str(tags.get("artist"), fn["artist"])
                info["album"]  = _safe_str(tags.get("album"),  "")
                info["bpm"]    = _safe_float(tags.get("bpm"))
                info["key"]    = _safe_str(tags.get("initialkey"))
            elif ext == "flac":
                audio = FLAC(file_path)
                info["duration"] = audio.info.length
                info["bitrate"]  = (getattr(audio.info, "bits_per_sample", 16)
                                    * getattr(audio.info, "sample_rate", 44100)) // 1000
                t = audio.tags or {}
                info["title"]  = _safe_str(t.get("title"),  fn["title"])
                info["artist"] = _safe_str(t.get("artist"), fn["artist"])
                info["album"]  = _safe_str(t.get("album"),  "")
            elif ext in ("ogg", "oga"):
                audio = OggVorbis(file_path)
                info["duration"] = audio.info.length
                t = audio.tags or {}
                info["title"]  = _safe_str(t.get("title"),  fn["title"])
                info["artist"] = _safe_str(t.get("artist"), fn["artist"])
            elif ext in ("m4a", "aac", "mp4", "alac"):
                audio = MP4(file_path)
                info["duration"] = audio.info.length
                t = audio.tags or {}
                info["title"]  = _safe_str(t.get("\xa9nam"), fn["title"])
                info["artist"] = _safe_str(t.get("\xa9ART"), fn["artist"])
                info["album"]  = _safe_str(t.get("\xa9alb"), "")
            else:
                af = mutagen.File(file_path)
                if af:
                    info["duration"] = getattr(af.info, "length", 0.0)
        except Exception as e:
            logger.warning(f"Mutagen read error [{file_path}]: {e}")

    # Ensure title is never empty
    if not info["title"]:
        info["title"] = fn["title"]
    if not info["artist"]:
        info["artist"] = fn["artist"]

    _cache[file_path] = info
    _save_cache()
    return info
