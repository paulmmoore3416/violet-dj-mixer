"""
Unit tests for src/audio/engine.py — AudioEngine
"""
import os
import tempfile
import unittest

from src.audio.engine import AudioEngine


class TestAudioEngineInit(unittest.TestCase):
    def setUp(self):
        self.engine = AudioEngine()

    def test_initial_state(self):
        self.assertIsNone(self.engine.backend)
        self.assertFalse(self.engine.is_playing)
        self.assertIsNone(self.engine.current_track)
        self.assertEqual(self.engine.volume,   AudioEngine.DEFAULT_VOLUME)
        self.assertEqual(self.engine.pan,      AudioEngine.DEFAULT_PAN)
        self.assertAlmostEqual(self.engine.pitch, AudioEngine.DEFAULT_PITCH)
        self.assertAlmostEqual(self.engine.position, 0.0)
        self.assertAlmostEqual(self.engine.duration, 0.0)

    def test_supported_codecs_count(self):
        formats = self.engine.get_supported_formats()
        self.assertEqual(len(formats), 9)
        for ext in ('mp3', 'wav', 'flac', 'ogg', 'aac', 'm4a', 'wma', 'aiff', 'alac'):
            self.assertIn(ext, formats)


class TestAudioEngineBackend(unittest.TestCase):
    def setUp(self):
        self.engine = AudioEngine()

    def test_valid_backend(self):
        self.engine.init_backend('pulseaudio')
        self.assertEqual(self.engine.backend, 'pulseaudio')

    def test_alsa_backend(self):
        self.engine.init_backend('alsa')
        self.assertEqual(self.engine.backend, 'alsa')

    def test_jack_backend(self):
        self.engine.init_backend('jack')
        self.assertEqual(self.engine.backend, 'jack')

    def test_invalid_backend_raises(self):
        with self.assertRaises(ValueError):
            self.engine.init_backend('nonexistent')


class TestAudioEnginePlayback(unittest.TestCase):
    def setUp(self):
        self.engine = AudioEngine()
        # Create a real temp file so load_track passes the existence check
        self._tmpfile = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        self._tmpfile.close()
        self.track = self._tmpfile.name

    def tearDown(self):
        os.unlink(self.track)

    def test_load_track(self):
        self.engine.load_track(self.track)
        self.assertEqual(self.engine.current_track, self.track)
        self.assertAlmostEqual(self.engine.position, 0.0)

    def test_load_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            self.engine.load_track('/does/not/exist.mp3')

    def test_load_unsupported_format_raises(self):
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            tmp = f.name
        try:
            with self.assertRaises(ValueError):
                self.engine.load_track(tmp)
        finally:
            os.unlink(tmp)

    def test_play_sets_is_playing(self):
        self.engine.load_track(self.track)
        self.engine.play()
        self.assertTrue(self.engine.is_playing)

    def test_play_without_track_does_nothing(self):
        self.engine.play()
        self.assertFalse(self.engine.is_playing)

    def test_pause(self):
        self.engine.load_track(self.track)
        self.engine.play()
        self.engine.pause()
        self.assertFalse(self.engine.is_playing)

    def test_stop_clears_track_and_position(self):
        self.engine.load_track(self.track)
        self.engine.play()
        self.engine.position = 42.5
        self.engine.stop()
        self.assertFalse(self.engine.is_playing)
        self.assertIsNone(self.engine.current_track)
        self.assertAlmostEqual(self.engine.position, 0.0)


class TestAudioEngineState(unittest.TestCase):
    def setUp(self):
        self.engine = AudioEngine()

    def test_volume_clamped_high(self):
        self.engine.volume = 999
        self.assertEqual(self.engine.volume, 100)

    def test_volume_clamped_low(self):
        self.engine.volume = -5
        self.assertEqual(self.engine.volume, 0)

    def test_volume_normal(self):
        self.engine.volume = 75
        self.assertEqual(self.engine.volume, 75)

    def test_pan_clamped(self):
        self.engine.pan = 200
        self.assertEqual(self.engine.pan, 100)
        self.engine.pan = -200
        self.assertEqual(self.engine.pan, -100)

    def test_pan_center(self):
        self.engine.pan = 0
        self.assertEqual(self.engine.pan, 0)

    def test_pitch_float(self):
        self.engine.pitch = 2.5
        self.assertAlmostEqual(self.engine.pitch, 2.5)

    def test_position_non_negative(self):
        self.engine.position = -10.0
        self.assertAlmostEqual(self.engine.position, 0.0)

    def test_position_valid(self):
        self.engine.position = 123.45
        self.assertAlmostEqual(self.engine.position, 123.45)


class TestAudioEngineFormatCheck(unittest.TestCase):
    def setUp(self):
        self.engine = AudioEngine()

    def test_supported_mp3(self):
        self.assertTrue(self.engine.is_format_supported('/music/track.mp3'))

    def test_supported_flac(self):
        self.assertTrue(self.engine.is_format_supported('/music/track.FLAC'))

    def test_unsupported_txt(self):
        self.assertFalse(self.engine.is_format_supported('/music/notes.txt'))

    def test_unsupported_no_ext(self):
        self.assertFalse(self.engine.is_format_supported('/music/track'))


if __name__ == '__main__':
    unittest.main()
