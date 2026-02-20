# 🎛️ Violet DJ Mixer
## Professional Digital Mixing Board for Ubuntu

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-blue.svg)](LICENSE)
[![Platform: Ubuntu](https://img.shields.io/badge/Platform-Ubuntu%2020.04%2B-orange.svg)](https://ubuntu.com)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Version: 1.0.0](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)](https://github.com/violet-dj/violet-dj-mixer)

<div align="center">

![Violet DJ Mixer](assets/logo.png)

**Free, Professional-Grade DJ Mixing Software**  
*Built for the Music Industry by Musicians & Developers*

[🌐 Visit Website](https://violet-dj.github.io) • [📖 Documentation](docs/README.md) • [🐛 Report Issues](https://github.com/violet-dj/violet-dj-mixer/issues) • [💬 Discussions](https://github.com/violet-dj/violet-dj-mixer/discussions)

</div>

---

## ✨ Features

### 🎚️ Professional Mixing Board
- **Multi-Channel Mixing**: Dual turntable decks with independent controls
- **Advanced Faders**: Smooth 100-level faders with visual feedback
- **EQ Controls**: 3-band parametric equalizer (Low, Mid, High) per channel
- **Crossfader**: Professional-grade crossfader for seamless transitions
- **Master Output**: Master volume control with metering
- **Level Meters**: Real-time VU metering for all channels

### 🎵 Audio Format Support
Supports all industry-standard audio formats:
- **Lossless**: WAV, FLAC, ALAC, AIFF
- **Lossy**: MP3, OGG Vorbis, AAC, M4A, WMA
- **Real-time Processing**: Zero-latency mixing and effects

### 🎧 Hardware Compatibility
Seamlessly integrates with professional DJ equipment:

**DJ Controllers Supported:**
- Pioneer DDJ Series (DDJ-400, DDJ-1000, etc.)
- Pioneer CDJ/DJM Mixers
- Numark Controllers
- Reloop Controllers
- Traktor Hardware
- Denon DJ Controllers
- Rane Seventy Series
- Allen & Heath Xone Series
- Akai Professional
- And 100+ more via standard MIDI

**Audio Devices:**
- USB Audio Interfaces
- Professional Sound Cards
- Turntables & Cartridges
- Microphones & Line Inputs

**Wireless Connectivity:**
- **Bluetooth Audio**: Connect multiple wireless speakers/headphones
- **Bluetooth Instruments**: Control synthesizers, drum machines, etc.
- **Wi-Fi Devices**: Network audio streaming and control
- **Multi-Device**: Simultaneous Bluetooth connections support

### 🎛️ Effects & Processors
Professional audio effects:
- Echo & Delay
- Reverb
- Chorus
- Flanger
- Phaser
- Distortion
- Filtering
- Real-time Parameters

### 🎨 Advanced Features
- **Waveform Visualization**: Real-time track waveforms
- **Spectrum Analyzer**: Professional audio spectrum display
- **Beat Synchronization**: Automatic BPM detection & sync
- **Hot Cues**: Up to 8 cue points per track
- **Looping**: Create dynamic loops with variable length
- **Sampler**: Integrated sampler with effects
- **Auto-Detection**: Intelligent device discovery & configuration

### 🔧 Developer-Friendly
- **Open Source**: Full source code available (GPL-3.0)
- **Extensible Architecture**: Plugin system for custom effects
- **MIDI Mapping**: Complete customizable MIDI mapping
- **RESTful API**: Control mixer via HTTP/WebSocket
- **Scripting Support**: Python scripting engine

---

## 🚀 Quick Start

### Installation

**Ubuntu 20.04 LTS & Later:**

```bash
# Download and install the .deb package
wget https://github.com/violet-dj/violet-dj-mixer/releases/download/v1.0.0/violet-dj-mixer_1.0.0_amd64.deb
sudo apt install ./violet-dj-mixer_1.0.0_amd64.deb
```

**Or install from source:**

```bash
git clone https://github.com/violet-dj/violet-dj-mixer.git
cd violet-dj-mixer
sudo ./scripts/install.sh
```

### First Launch

```bash
# Start the application
violet-dj

# Or from source
python3 main.py
```

---

## 📚 Documentation

Comprehensive guides for all features:

- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Installation & first steps
- **[User Manual](docs/USER_MANUAL.md)** - Complete feature documentation
- **[Hardware Setup](docs/HARDWARE_SETUP.md)** - Controller & device configuration
- **[Audio Configuration](docs/AUDIO_CONFIGURATION.md)** - Audio backend & codecs
- **[Bluetooth Guide](docs/BLUETOOTH_SETUP.md)** - Wireless device connectivity
- **[MIDI Mapping Guide](docs/MIDI_MAPPING.md)** - Controller customization
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues & solutions
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Plugin development

---

## 🎓 System Requirements

### Minimum Specifications
- **OS**: Ubuntu 20.04 LTS or later
- **Processor**: Intel i5 / AMD Ryzen 5 (2.5 GHz+)
- **RAM**: 4 GB
- **Storage**: 500 MB for application

### Recommended Specifications
- **OS**: Ubuntu 22.04 LTS or later
- **Processor**: Intel i7 / AMD Ryzen 7 (3.5 GHz+)
- **RAM**: 8 GB or more
- **Storage**: SSD with 1+ GB free space
- **Audio**: Professional sound card (USB or PCI)

### Required Packages
```bash
sudo apt install python3 python3-pip pulseaudio alsa-utils bluetooth bluez
```

---

## 🔗 Hardware Setup

### USB Controllers

**Connect your DJ controller via USB:**

```bash
# List connected USB devices
lsusb | grep -i audio

# Load device drivers (automatically)
violet-dj --detect-devices
```

### Bluetooth Devices

**Connect Bluetooth devices:**

1. **Pair Bluetooth device** (Ubuntu Settings > Bluetooth)
2. **Open Violet DJ Mixer** → Settings tab
3. **Check "Enable Bluetooth Audio"**
4. **Select device** from dropdown
5. **Multiple devices**: Enable "Multiple Bluetooth Connections"

### Network Audio (Wi-Fi)

**Connect to network audio devices:**

1. **Ensure device on same network**
2. **Enable "Wi-Fi Device Discovery"** in Settings
3. **Mixer auto-detects** compatible devices
4. **Click to connect**

---

## 🎛️ Mixer Basics

### Loading Tracks

```
1. Click "Load" on Deck 1 or Deck 2
2. Browse to audio file
3. Waveform displays automatically
4. Click "Play" to begin
```

### Mixing Two Tracks

```
1. Load Track A on Deck 1, Track B on Deck 2
2. Start Track B playing (cue in headphones first via Cue button)
3. Monitor mix levels on Master fader
4. Use Crossfader to blend between tracks
5. Adjust Pitch/Speed for beat-matching
```

### Using Effects

```
1. Select effect (Echo, Reverb, etc.) in Effects tab
2. Enable checkbox to activate
3. Adjust Mix and Time parameters
4. Effect applies to master output
```

---

## 🛠️ Configuration

### Audio Backend Selection

**Via GUI:**
Settings Tab → Audio Backend → Select PulseAudio/ALSA/JACK

**Via Command Line:**
```bash
violet-dj --audio-backend pulseaudio
violet-dj --audio-backend alsa
violet-dj --audio-backend jack
```

### MIDI Controller Mapping

**Automatic Detection:**
```
1. Connect MIDI controller via USB
2. Open Controllers tab
3. Click "Detect"
4. Select detected controller
5. Mappings auto-load for supported devices
```

**Custom Mapping:**
```
1. Controllers tab → MIDI Mapping
2. Right-click control to map
3. Move controller knob/slider
4. Assign mixer function
5. Save profile
```

---

## 🐛 Troubleshooting

### No Audio Output

```bash
# Check audio devices
pactl list sources
aplay -l

# Restart PulseAudio
pulseaudio --kill && sleep 1 && pulseaudio --start
```

### MIDI Controller Not Detected

```bash
# List MIDI devices
aseqdump -l

# Check USB connection
lsusb | grep -i midi
```

### Bluetooth Connection Issues

```bash
# Restart Bluetooth
sudo systemctl restart bluetooth

# Check paired devices
bluetoothctl paired-devices
```

[More troubleshooting →](docs/TROUBLESHOOTING.md)

---

## 💻 Development

### Building from Source

```bash
# Clone repository
git clone https://github.com/violet-dj/violet-dj-mixer.git
cd violet-dj-mixer

# Install dependencies
pip3 install -r requirements.txt

# Run application
python3 main.py

# Run tests
python3 -m pytest tests/
```

### Creating Custom Effects

```python
from src.audio.effects import AudioEffect

class MyEffect(AudioEffect):
    def __init__(self, name="My Effect"):
        super().__init__(name)
    
    def process(self, audio_data):
        # Your effect processing here
        return audio_data
```

[Full Developer Guide →](docs/DEVELOPER_GUIDE.md)

---

## 📦 Distribution

### Creating .deb Package

```bash
./scripts/build-deb.sh
```

### Distribution Files

- `violet-dj-mixer_1.0.0_amd64.deb` - Ubuntu 64-bit package
- Includes all dependencies and drivers
- Desktop integration & menu shortcuts

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- 🎵 Additional audio effects
- 🎛️ Hardware controller support
- 🌐 Localization & translations
- 📖 Documentation
- 🐛 Bug fixes
- ✨ New features

---

## 📝 License

Violet DJ Mixer is released under the **GNU General Public License v3.0 or later**.

This ensures the software remains free and open for the music community.

[Read Full License →](LICENSE)

---

## 🌟 Credits

**Created For:**
- Musicians who can't afford expensive mixing software
- DJs building their home studios
- Music producers on a budget
- Open-source music software community

**Built With:**
- Python 3.8+
- PyQt6 for UI
- JACK/PulseAudio/ALSA for audio
- python-rtmidi for MIDI support

---

## 📞 Support & Community

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/violet-dj/violet-dj-mixer/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/violet-dj/violet-dj-mixer/discussions)
- **📧 Email**: support@violet-dj.github.io
- **🎵 Discord Community**: [Join Server](https://discord.gg/violet-dj)

---

## 🎯 Roadmap

### v1.1.0 (Q2 2024)
- [ ] Video visualization enhancements
- [ ] Advanced sampler
- [ ] Cue/Remix utilities
- [ ] Performance improvements

### v1.2.0 (Q3 2024)
- [ ] Integration with Spotify/SoundCloud
- [ ] Network jamming over LAN
- [ ] Mobile controller app
- [ ] VST plugin support

### v2.0.0 (2025)
- [ ] Professional console version
- [ ] Multi-deck support (4+ decks)
- [ ] Advanced AI mixing assistant
- [ ] Full DAW integration

---

<div align="center">

**Made with 🎵 for the music community**

[⭐ Star us on GitHub](https://github.com/violet-dj/violet-dj-mixer) | [Follow us on Twitter](https://twitter.com/violet_dj) | [Support Development](https://github.com/sponsors/violet-dj)

</div>
