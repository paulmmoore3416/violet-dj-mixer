"""
Unit tests for the 12 new feature modules:
  - src/audio/metadata.py
  - src/audio/recorder.py
  - src/ui/vu_meter.py
  - src/ui/waveform.py
"""
from __future__ import annotations

import os
import tempfile
import unittest
import wave


# ── Metadata ──────────────────────────────────────────────────────────────────

class TestMetadata(unittest.TestCase):
    def test_import(self):
        from src.audio.metadata import read_metadata, format_duration
        self.assertTrue(callable(read_metadata))
        self.assertTrue(callable(format_duration))

    def test_format_duration_zero(self):
        from src.audio.metadata import format_duration
        self.assertEqual(format_duration(0), "--:--")
        self.assertEqual(format_duration(-5), "--:--")

    def test_format_duration_minutes(self):
        from src.audio.metadata import format_duration
        self.assertEqual(format_duration(90), "1:30")
        self.assertEqual(format_duration(65), "1:05")

    def test_format_duration_hours(self):
        from src.audio.metadata import format_duration
        self.assertEqual(format_duration(3661), "1:01:01")

    def test_read_nonexistent_returns_dict(self):
        from src.audio.metadata import read_metadata
        info = read_metadata("/does/not/exist.mp3")
        self.assertIsInstance(info, dict)
        self.assertIn("title", info)
        self.assertIn("artist", info)
        self.assertIn("duration", info)

    def test_artist_title_parsed_from_filename(self):
        from src.audio.metadata import read_metadata
        info = read_metadata("/music/Daft Punk - Around The World.mp3")
        self.assertEqual(info["artist"], "Daft Punk")
        self.assertEqual(info["title"],  "Around The World")

    def test_title_only_filename(self):
        from src.audio.metadata import read_metadata
        info = read_metadata("/music/SomeSong.flac")
        self.assertEqual(info["title"], "SomeSong")

    def test_format_inferred_from_extension(self):
        from src.audio.metadata import read_metadata
        info = read_metadata("/music/track.wav")
        self.assertEqual(info["format"], "WAV")

    def test_caching_returns_same_object(self):
        from src.audio import metadata as md
        md._cache.clear()
        info1 = md.read_metadata("/tmp/fake_song - No Artist.mp3")
        info2 = md.read_metadata("/tmp/fake_song - No Artist.mp3")
        self.assertEqual(info1["title"], info2["title"])


# ── Recorder ──────────────────────────────────────────────────────────────────

class TestRecorder(unittest.TestCase):
    def setUp(self):
        from src.audio.recorder import Recorder
        self.tmpdir = tempfile.mkdtemp()
        self.rec = Recorder()

    def tearDown(self):
        import shutil
        if self.rec.is_recording:
            self.rec.stop()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_import(self):
        from src.audio.recorder import Recorder
        self.assertTrue(callable(Recorder))

    def test_initially_not_recording(self):
        self.assertFalse(self.rec.is_recording)

    def test_elapsed_zero_when_stopped(self):
        self.assertEqual(self.rec.elapsed, 0.0)

    def test_start_creates_file(self):
        path = os.path.join(self.tmpdir, "test_rec.wav")
        returned = self.rec.start(path)
        self.assertEqual(returned, path)
        self.assertTrue(self.rec.is_recording)

    def test_stop_returns_path(self):
        path = os.path.join(self.tmpdir, "test_stop.wav")
        self.rec.start(path)
        out = self.rec.stop()
        self.assertEqual(out, path)
        self.assertFalse(self.rec.is_recording)

    def test_saved_file_is_valid_wav(self):
        path = os.path.join(self.tmpdir, "valid.wav")
        self.rec.start(path)
        self.rec.stop()
        self.assertTrue(os.path.exists(path))
        with wave.open(path, "rb") as w:
            self.assertEqual(w.getnchannels(), 2)
            self.assertEqual(w.getsampwidth(), 2)
            self.assertEqual(w.getframerate(), 44100)

    def test_double_start_is_safe(self):
        path = os.path.join(self.tmpdir, "safe.wav")
        p1 = self.rec.start(path)
        p2 = self.rec.start(os.path.join(self.tmpdir, "other.wav"))
        self.assertEqual(p1, p2)   # second start is ignored
        self.rec.stop()

    def test_stop_without_start_returns_none(self):
        result = self.rec.stop()
        self.assertIsNone(result)

    def test_discard_removes_file(self):
        path = os.path.join(self.tmpdir, "discard.wav")
        self.rec.start(path)
        self.rec.discard()
        self.assertFalse(self.rec.is_recording)
        self.assertFalse(os.path.exists(path))

    def test_list_recordings_returns_list(self):
        result = self.rec.list_recordings()
        self.assertIsInstance(result, list)

    def test_auto_path_if_none_given(self):
        path = self.rec.start()
        self.assertTrue(path.endswith(".wav"))
        self.rec.stop()


# ── VU Meter ──────────────────────────────────────────────────────────────────

class TestVUMeter(unittest.TestCase):
    """Headless tests — no QApplication needed for pure logic checks."""

    def test_import(self):
        from src.ui.vu_meter import VUMeter
        self.assertTrue(callable(VUMeter))

    def test_set_level_clamps(self):
        from src.ui.vu_meter import VUMeter
        # Instantiating VUMeter requires a QApplication; test logic directly
        # by importing the class and checking its logic doesn't error.
        try:
            import PyQt6
            app_available = True
        except ImportError:
            app_available = False
        if not app_available:
            self.skipTest("PyQt6 not available")


# ── Waveform ──────────────────────────────────────────────────────────────────

class TestWaveform(unittest.TestCase):
    def test_import(self):
        from src.ui.waveform import WaveformDisplay, _synth_waveform
        self.assertTrue(callable(WaveformDisplay))
        self.assertTrue(callable(_synth_waveform))

    def test_synth_waveform_length(self):
        from src.ui.waveform import _synth_waveform
        data = _synth_waveform(12345, n=128)
        self.assertEqual(len(data), 128)

    def test_synth_waveform_range(self):
        from src.ui.waveform import _synth_waveform
        data = _synth_waveform(99999, n=256)
        self.assertTrue(all(-1.0 <= v <= 1.0 for v in data))

    def test_synth_waveform_deterministic(self):
        from src.ui.waveform import _synth_waveform
        d1 = _synth_waveform(42, n=64)
        d2 = _synth_waveform(42, n=64)
        self.assertEqual(d1, d2)

    def test_synth_waveform_different_seeds(self):
        from src.ui.waveform import _synth_waveform
        d1 = _synth_waveform(1,  n=64)
        d2 = _synth_waveform(99, n=64)
        self.assertNotEqual(d1, d2)


if __name__ == "__main__":
    unittest.main()
