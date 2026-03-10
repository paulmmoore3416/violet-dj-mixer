"""
Unit tests for src/devices/detector.py — DeviceDetector
"""
import unittest
from unittest.mock import patch, MagicMock


class TestDeviceDetectorImport(unittest.TestCase):
    """Smoke test: module imports without PyQt6 raising errors in headless CI."""

    def test_import(self):
        try:
            from src.devices.detector import DeviceDetector
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"PyQt6 not available in this environment: {e}")


class TestDeviceDetectorLogic(unittest.TestCase):
    """Test device detection logic with mocked subprocesses."""

    def setUp(self):
        try:
            from src.devices.detector import DeviceDetector
            self.DeviceDetector = DeviceDetector
        except ImportError as e:
            self.skipTest(f"PyQt6 not available: {e}")

    def _make_detector(self):
        detector = self.DeviceDetector.__new__(self.DeviceDetector)
        detector.devices = []
        return detector

    @patch('subprocess.run')
    def test_detect_audio_devices_pulseaudio(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='sink info')
        detector = self._make_detector()
        detector.detect_audio_devices()
        types = [d['type'] for d in detector.devices]
        self.assertIn('audio', types)

    @patch('subprocess.run')
    def test_detect_audio_devices_alsa(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='card 0')
        detector = self._make_detector()
        detector.detect_audio_devices()
        backends = [d.get('backend') for d in detector.devices]
        self.assertTrue(any(b in ('pulseaudio', 'alsa') for b in backends))

    @patch('subprocess.run')
    def test_detect_audio_devices_failure(self, mock_run):
        mock_run.side_effect = Exception("pactl not found")
        detector = self._make_detector()
        # Should not raise; just logs a warning
        try:
            detector.detect_audio_devices()
        except Exception:
            self.fail("detect_audio_devices raised unexpectedly on subprocess error")

    @patch('subprocess.run')
    def test_detect_bluetooth_devices(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='Device AA:BB:CC')
        detector = self._make_detector()
        detector.detect_bluetooth_devices()
        types = [d['type'] for d in detector.devices]
        self.assertIn('bluetooth', types)

    def test_detect_midi_devices_proc_asound(self):
        detector = self._make_detector()
        import os
        with patch('os.path.exists', return_value=True):
            detector.detect_midi_devices()
        types = [d['type'] for d in detector.devices]
        self.assertIn('midi', types)

    def test_detect_wifi_devices_always_adds_entry(self):
        detector = self._make_detector()
        detector.detect_wifi_devices()
        types = [d['type'] for d in detector.devices]
        self.assertIn('wifi', types)

    def test_devices_list_initially_empty(self):
        detector = self._make_detector()
        self.assertEqual(detector.devices, [])

    def test_connect_device_does_not_raise(self):
        detector = self._make_detector()
        try:
            detector.connect_device({'type': 'audio', 'name': 'Test'})
        except Exception:
            self.fail("connect_device raised unexpectedly")

    def test_disconnect_device_does_not_raise(self):
        detector = self._make_detector()
        try:
            detector.disconnect_device({'type': 'audio', 'name': 'Test'})
        except Exception:
            self.fail("disconnect_device raised unexpectedly")


if __name__ == '__main__':
    unittest.main()
