"""
Audio processing, codec support, and playback
"""

import logging

logger = logging.getLogger(__name__)

class AudioEngine:
    """Main audio processing engine"""
    
    SUPPORTED_CODECS = {
        'mp3': 'MP3 (MPEG Audio)',
        'wav': 'WAV (Waveform Audio)',
        'flac': 'FLAC (Free Lossless Audio)',
        'ogg': 'OGG Vorbis',
        'aac': 'AAC (Advanced Audio)',
        'm4a': 'MP4 Audio',
        'wma': 'Windows Media Audio',
        'aiff': 'Audio Interchange File Format',
        'alac': 'Apple Lossless Audio',
    }
    
    AUDIO_BACKENDS = {
        'pulseaudio': 'PulseAudio (Recommended)',
        'alsa': 'ALSA (Advanced Linux Sound Architecture)',
        'jack': 'JACK (Jack Audio Connection Kit)',
    }
    
    def __init__(self):
        logger.info("Initializing Audio Engine")
        self.backend = None
        self.is_playing = False
        self.current_track = None
        self.devices = []
    
    def init_backend(self, backend_name):
        """Initialize audio backend"""
        if backend_name not in self.AUDIO_BACKENDS:
            raise ValueError(f"Unknown backend: {backend_name}")
        
        self.backend = backend_name
        logger.info(f"Audio backend initialized: {backend_name}")
    
    def load_track(self, file_path):
        """Load an audio track"""
        logger.info(f"Loading track: {file_path}")
        self.current_track = file_path
    
    def play(self):
        """Start playback"""
        if self.current_track:
            self.is_playing = True
            logger.info(f"Playing: {self.current_track}")
    
    def pause(self):
        """Pause playback"""
        self.is_playing = False
        logger.info("Playback paused")
    
    def stop(self):
        """Stop playback"""
        self.is_playing = False
        self.current_track = None
        logger.info("Playback stopped")
    
    def get_supported_formats(self):
        """Return list of supported audio formats"""
        return list(self.SUPPORTED_CODECS.keys())
    
    def get_device_list(self):
        """Get list of available audio devices"""
        return self.devices
