"""
Audio processing, codec support, and playback
"""

import logging
import os

logger = logging.getLogger(__name__)


class AudioEngine:
    """Main audio processing engine"""

    SUPPORTED_CODECS = {
        'mp3':  'MP3 (MPEG Audio)',
        'wav':  'WAV (Waveform Audio)',
        'flac': 'FLAC (Free Lossless Audio)',
        'ogg':  'OGG Vorbis',
        'aac':  'AAC (Advanced Audio)',
        'm4a':  'MP4 Audio',
        'wma':  'Windows Media Audio',
        'aiff': 'Audio Interchange File Format',
        'alac': 'Apple Lossless Audio',
    }

    AUDIO_BACKENDS = {
        'pulseaudio': 'PulseAudio (Recommended)',
        'alsa':       'ALSA (Advanced Linux Sound Architecture)',
        'jack':       'JACK (Jack Audio Connection Kit)',
    }

    # Enhancement 9 – default state constants
    DEFAULT_VOLUME = 100   # 0–100
    DEFAULT_PAN    = 0     # -100 (L) … 0 (C) … +100 (R)
    DEFAULT_PITCH  = 0.0   # semitones, float

    def __init__(self):
        logger.info("Initializing Audio Engine")
        self.backend: str | None = None
        self.is_playing: bool = False
        self.current_track: str | None = None
        self.devices: list = []

        # Enhancement 9 – playback state tracking
        self._volume: int = self.DEFAULT_VOLUME
        self._pan: int = self.DEFAULT_PAN
        self._pitch: float = self.DEFAULT_PITCH
        self._position: float = 0.0   # seconds from start
        self._duration: float = 0.0   # total track duration in seconds

    # ── Backend ──────────────────────────────────────────────────────────────
    def init_backend(self, backend_name: str) -> None:
        """Initialize audio backend."""
        if backend_name not in self.AUDIO_BACKENDS:
            raise ValueError(f"Unknown backend: {backend_name}")
        self.backend = backend_name
        logger.info(f"Audio backend initialized: {backend_name}")

    # ── Playback ─────────────────────────────────────────────────────────────
    def load_track(self, file_path: str) -> None:
        """Load an audio track and reset playback state."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Track not found: {file_path}")
        ext = os.path.splitext(file_path)[1].lstrip('.').lower()
        if ext not in self.SUPPORTED_CODECS:
            raise ValueError(f"Unsupported format: .{ext}")
        logger.info(f"Loading track: {file_path}")
        self.current_track = file_path
        self._position = 0.0
        self._duration = 0.0   # real implementation would probe duration here

    def play(self) -> None:
        """Start playback."""
        if self.current_track:
            self.is_playing = True
            logger.info(f"Playing: {self.current_track}")

    def pause(self) -> None:
        """Pause playback."""
        self.is_playing = False
        logger.info("Playback paused")

    def stop(self) -> None:
        """Stop playback and reset position."""
        self.is_playing = False
        self._position = 0.0
        self.current_track = None
        logger.info("Playback stopped")

    # ── Enhancement 9 – Volume / Pan / Pitch ─────────────────────────────────
    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, value: int) -> None:
        self._volume = max(0, min(100, int(value)))

    @property
    def pan(self) -> int:
        return self._pan

    @pan.setter
    def pan(self, value: int) -> None:
        self._pan = max(-100, min(100, int(value)))

    @property
    def pitch(self) -> float:
        return self._pitch

    @pitch.setter
    def pitch(self, semitones: float) -> None:
        self._pitch = float(semitones)

    @property
    def position(self) -> float:
        """Current playback position in seconds."""
        return self._position

    @position.setter
    def position(self, seconds: float) -> None:
        self._position = max(0.0, float(seconds))

    @property
    def duration(self) -> float:
        """Total track duration in seconds."""
        return self._duration

    # ── Utility ──────────────────────────────────────────────────────────────
    def get_supported_formats(self) -> list[str]:
        """Return list of supported audio format extensions."""
        return list(self.SUPPORTED_CODECS.keys())

    def get_device_list(self) -> list:
        """Get list of available audio devices."""
        return self.devices

    def is_format_supported(self, file_path: str) -> bool:
        """Return True if the file's extension is a supported audio format."""
        ext = os.path.splitext(file_path)[1].lstrip('.').lower()
        return ext in self.SUPPORTED_CODECS
