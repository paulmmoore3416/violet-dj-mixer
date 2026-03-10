"""
WAV recorder — writes real WAV files via Python's wave module.
A real implementation would stream audio from the selected backend;
this stub writes silent frames so the file is structurally valid.
"""
from __future__ import annotations

import logging
import os
import time
import wave

logger = logging.getLogger(__name__)

RECORDINGS_DIR = os.path.expanduser("~/.violet_dj/recordings")


class Recorder:
    """Start/stop WAV recorder with elapsed-time tracking."""

    SAMPLE_RATE  = 44100
    CHANNELS     = 2
    SAMPLE_WIDTH = 2   # 16-bit PCM

    def __init__(self) -> None:
        os.makedirs(RECORDINGS_DIR, exist_ok=True)
        self._recording: bool = False
        self._start_time: float = 0.0
        self._path: str | None = None
        self._wav: wave.Wave_write | None = None

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def is_recording(self) -> bool:
        return self._recording

    @property
    def elapsed(self) -> float:
        """Seconds since recording started (0.0 if not recording)."""
        return time.time() - self._start_time if self._recording else 0.0

    @property
    def current_path(self) -> str | None:
        return self._path

    # ── Control ───────────────────────────────────────────────────────────────

    def start(self, output_path: str | None = None) -> str:
        """Open a WAV file and start recording.  Returns the file path."""
        if self._recording:
            return self._path or ""

        if output_path is None:
            ts = time.strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(RECORDINGS_DIR, f"rec_{ts}.wav")

        self._path = output_path
        try:
            self._wav = wave.open(output_path, "wb")
            self._wav.setnchannels(self.CHANNELS)
            self._wav.setsampwidth(self.SAMPLE_WIDTH)
            self._wav.setframerate(self.SAMPLE_RATE)
            self._recording  = True
            self._start_time = time.time()
            logger.info(f"Recording started: {output_path}")
        except Exception as e:
            logger.error(f"Recorder.start failed: {e}")
            self._wav = None

        return output_path

    def stop(self) -> str | None:
        """Finalise the WAV file and stop recording.  Returns saved path."""
        if not self._recording:
            return None

        self._recording = False
        path = self._path

        if self._wav:
            try:
                # Write one second of silence so the WAV is playable
                silence = b"\x00" * (self.SAMPLE_RATE * self.CHANNELS * self.SAMPLE_WIDTH)
                self._wav.writeframes(silence)
                self._wav.close()
            except Exception as e:
                logger.warning(f"Recorder.stop WAV error: {e}")
            finally:
                self._wav = None

        logger.info(f"Recording saved: {path}")
        return path

    def discard(self) -> None:
        """Stop without saving (delete the partial file)."""
        self._recording = False
        if self._wav:
            try:
                self._wav.close()
            except Exception:
                pass
            self._wav = None
        if self._path and os.path.exists(self._path):
            try:
                os.remove(self._path)
            except Exception:
                pass
        self._path = None

    # ── Listings ──────────────────────────────────────────────────────────────

    def list_recordings(self) -> list[str]:
        """Return saved WAV filenames sorted newest-first."""
        try:
            names = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith(".wav")]
            return sorted(names, reverse=True)
        except Exception:
            return []
