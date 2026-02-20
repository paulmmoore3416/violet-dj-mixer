# Violet DJ Mixer - Development Guide

## For Plugin Developers & Contributors

This guide covers extending Violet DJ Mixer with custom effects, controllers, and features.

---

## Project Architecture

```
violet-dj-mixer/
├── src/
│   ├── ui/                 # PyQt6 UI components
│   │   ├── main_window.py # Main application window
│   │   ├── widgets/       # Custom UI widgets
│   │   └── styles/        # Theme and styling
│   ├── audio/              # Audio processing
│   │   ├── engine.py      # Main audio engine
│   │   ├── decoder.py     # Audio codec support
│   │   └── effects/       # Audio effects
│   ├── devices/            # Device management
│   │   ├── detector.py    # Device detection
│   │   └── manager.py     # Device management
│   └── controllers/        # MIDI controller support
│       ├── manager.py     # Controller management
│       └── mappings/      # Pre-built mappings
├── tests/                  # Unit tests
├── docs/                   # Documentation
└── scripts/                # Build scripts
```

---

## Creating Custom Effects

### Effect Base Class

```python
from src.audio.effects import AudioEffect
import numpy as np

class MyEffect(AudioEffect):
    """Custom audio effect template"""
    
    def __init__(self, name="My Effect"):
        super().__init__(name)
        
        # Define parameters
        self.add_parameter("mix", min=0, max=100, default=50)
        self.add_parameter("intensity", min=0, max=100, default=50)
    
    def process(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Process audio data and return modified audio
        
        Args:
            audio_data: NumPy array of audio samples
            sample_rate: Sample rate in Hz
        
        Returns:
            Modified audio data (same shape)
        """
        # Get parameter values
        mix = self.get_parameter("mix") / 100.0
        intensity = self.get_parameter("intensity") / 100.0
        
        # Process audio
        processed = audio_data.copy()
        
        # Your effect processing here
        # Example: Simple gain
        processed = processed * (0.5 + intensity)
        
        # Mix dry and wet signals
        output = (1 - mix) * audio_data + mix * processed
        
        return output
    
    def reset(self):
        """Reset effect state (called on new track)"""
        pass
```

### Register Effect

```python
# In src/audio/effects/__init__.py
from .my_effect import MyEffect

# Register in effects list
AVAILABLE_EFFECTS = {
    'my_effect': MyEffect,
    'echo': EchoEffect,
    # ... others
}
```

---

## Controller Support

### Adding MIDI Controller

```python
from src.controllers.manager import ControllerManager

class MyControllerMapping:
    """Define controller-specific mappings"""
    
    MANUFACTURER = "My Brand"
    MODEL = "Controller X"
    MIDI_IDS = {
        'vendor': 0x1234,  # USB Vendor ID
        'product': 0x5678   # USB Product ID
    }
    
    # Define controls and their MIDI CC values
    CONTROLS = {
        'deck1_volume': 0x10,      # MIDI CC 16
        'deck2_volume': 0x11,      # MIDI CC 17
        'crossfader': 0x20,        # MIDI CC 32
        'master_volume': 0x21,     # MIDI CC 33
        'eq_low': 0x30,            # MIDI CC 48
        # ... more controls
    }
    
    @staticmethod
    def create_mappings():
        """Create mapping from MIDI controls to functions"""
        return {
            'deck1_volume': {
                'function': 'set_deck_volume',
                'deck': 1,
                'range': (0, 127),  # MIDI value range
                'output_range': (0, 100)  # Mixer value range
            },
            # ... more mappings
        }
```

### Register Controller

```python
# In src/controllers/manager.py
from .my_controller import MyControllerMapping

CONTROLLER_MAPPINGS = {
    'my_brand_controller_x': MyControllerMapping,
    # ... others
}
```

---

## Audio Codec Support

### Adding Codec Decoder

```python
from src.audio.decoder import AudioDecoder
import numpy as np

class MyFormatDecoder(AudioDecoder):
    """Decoder for custom audio format"""
    
    SUPPORTED_EXTENSIONS = ['.xyz']
    FORMAT_NAME = "My Audio Format"
    
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.sample_rate = 48000
        self.channels = 2
        self.duration = 0.0
    
    def read_frames(self, num_frames: int) -> np.ndarray:
        """
        Read audio frames from file
        
        Returns NumPy array of shape (num_frames, channels)
        """
        # Read from file and decode
        frames = self._decode_frames(num_frames)
        return frames
    
    def seek(self, frame_number: int):
        """Seek to specific frame"""
        self._seek_internal(frame_number)
    
    def close(self):
        """Close file and cleanup"""
        self._close_file()
```

### Register Decoder

```python
# In src/audio/engine.py
from .decoders.my_format import MyFormatDecoder

AUDIO_DECODERS = {
    '.xyz': MyFormatDecoder,
    # ... others
}
```

---

## UI Customization

### Custom Widget

```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider
from PyQt6.QtCore import Qt, pyqtSignal

class AdvancedSlider(QWidget):
    """Custom slider widget with value display"""
    
    value_changed = pyqtSignal(int)
    
    def __init__(self, name: str, min_val: int = 0, max_val: int = 100):
        super().__init__()
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.valueChanged.connect(self._on_value_changed)
        
        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        self.setLayout(layout)
    
    def _on_value_changed(self, value):
        self.value_changed.emit(value)
    
    def setValue(self, value):
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)
    
    def value(self):
        return self.slider.value()
```

### Custom Theme

```python
# Create custom stylesheet
THEME = """
QWidget {
    background-color: #1a1a2e;
    color: #e0e0e0;
}

QSlider::groove:horizontal {
    border: 1px solid #7c3aed;
    height: 8px;
    background: #2a2a3e;
}

QSlider::handle:horizontal {
    background: #7c3aed;
    border: 1px solid #7c3aed;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}
"""

# Apply in main window
app.setStyleSheet(THEME)
```

---

## Testing

### Unit Tests

```python
# tests/test_effects.py
import unittest
import numpy as np
from src.audio.effects import MyEffect

class TestMyEffect(unittest.TestCase):
    
    def setUp(self):
        self.effect = MyEffect()
        self.sample_rate = 48000
    
    def test_effect_output_shape(self):
        """Test output has same shape as input"""
        input_data = np.random.randn(48000, 2)
        output = self.effect.process(input_data, self.sample_rate)
        self.assertEqual(output.shape, input_data.shape)
    
    def test_parameter_setting(self):
        """Test parameter setting"""
        self.effect.set_parameter("mix", 75)
        self.assertEqual(self.effect.get_parameter("mix"), 75)
    
    def test_no_clipping(self):
        """Test output doesn't clip"""
        input_data = np.ones((48000, 2))
        output = self.effect.process(input_data, self.sample_rate)
        self.assertTrue(np.max(np.abs(output)) <= 1.0)

if __name__ == '__main__':
    unittest.main()
```

### Run Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test
python3 -m pytest tests/test_effects.py::TestMyEffect::test_effect_output_shape

# With coverage
python3 -m pytest --cov=src tests/
```

---

## Building & Distribution

### Create .deb Package

```bash
bash scripts/build-deb.sh
# Creates: dist/violet-dj-mixer_1.0.0_amd64.deb
```

### Create Release

```bash
# Tag version
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0

# GitHub Actions automatically:
# - Builds .deb
# - Creates release page
# - Uploads package
```

---

## Debugging

### Enable Debug Logging

```bash
violet-dj --loglevel DEBUG
```

### Debug Specific Module

```python
import logging

# In your code
logger = logging.getLogger(__name__)
logger.debug("Debug message: %s", variable)
logger.info("Info message")
logger.error("Error message", exc_info=True)
```

### Debug MIDI

```bash
# Monitor MIDI events
aseqdump -l
```

### Debug Audio

```bash
# Check audio devices
aplay -l
pactl list sources
```

---

## Contributing

1. **Fork** repository
2. **Create** feature branch
3. **Make** changes with tests
4. **Document** your code
5. **Create** pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

## API Documentation

### AudioEngine

```python
engine = AudioEngine()
engine.init_backend('pulseaudio')
engine.load_track('song.mp3')
engine.play()
```

### DeviceDetector

```python
detector = DeviceDetector()
devices = detector.detect_all()
detector.connect_device(device_id)
```

### ControllerManager

```python
manager = ControllerManager()
controllers = manager.detect_controllers()
manager.map_control(ctrl_id, midi_cc, action)
```

---

## Resources

- [PyQt6 Documentation](https://doc.qt.io/qt-6/)
- [NumPy Audio Processing](https://numpy.org/)
- [MIDI Specification](https://www.midi.org/)
- [Ubuntu Development](https://ubuntu.com/blog)

---

Happy Developing! 🎧
