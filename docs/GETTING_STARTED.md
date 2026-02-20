# Getting Started with Violet DJ Mixer

## 📋 Prerequisites

### System Requirements
- **Ubuntu 20.04 LTS** or later
- **Python 3.8** or later
- **4 GB RAM** (8 GB recommended)
- **500 MB** disk space

### Required Dependencies
```bash
sudo apt update
sudo apt install -y \
    python3 python3-pip python3-dev \
    pulseaudio alsa-utils libasound2-dev \
    libpulse-dev \
    bluetooth bluez libbluetooth-dev \
    qt6-base-dev libqt6core6 \
    libssl-dev libffi-dev
```

---

## 🔧 Installation

### Method 1: Ubuntu Package (.deb)

**Recommended for most users**

```bash
# Download latest release
wget https://github.com/violet-dj/violet-dj-mixer/releases/download/v1.0.0/violet-dj-mixer_1.0.0_amd64.deb

# Install package
sudo apt install ./violet-dj-mixer_1.0.0_amd64.deb

# Verify installation
violet-dj --version
```

### Method 2: From Source

**For developers and contributors**

```bash
# Clone repository
git clone https://github.com/violet-dj/violet-dj-mixer.git
cd violet-dj-mixer

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Run application
python3 main.py
```

### Method 3: From Git (Development)

```bash
# Clone with latest development code
git clone -b develop https://github.com/violet-dj/violet-dj-mixer.git
cd violet-dj-mixer

# Follow Method 2 steps above
```

---

## 🎯 First Launch

### Launching the Application

**Via Application Menu:**
1. Click Activities
2. Search "Violet DJ"
3. Click to launch

**Via Command Line:**
```bash
# If installed via .deb
violet-dj

# If running from source
cd ~/violetdj
python3 main.py
```

### Initial Setup Wizard

On first launch, you'll see:

1. **Audio Configuration** - Select audio backend (PulseAudio/ALSA)
2. **Device Detection** - Scanner checks for connected devices
3. **Preference** - Choose mixer layout and units
4. **Finish** - Ready to mix!

---

## 🎧 Connecting Your First Device

### USB Controller

1. **Connect** USB cable to Ubuntu machine
2. **Open** Violet DJ Mixer
3. **Settings tab** → Scroll to "MIDI Devices"
4. **Detect** button to auto-find controllers
5. **Select** your controller from dropdown
6. **Done!** - Mappings auto-load for supported devices

### Audio Interface

1. **Connect** USB or 3.5mm audio interface
2. **Settings tab** → Audio Devices
3. **Select** device in "Output Device"
4. **Test** audio with track playback

### Bluetooth Speaker

1. **Pair** in Ubuntu Settings (Bluetooth panel)
2. **Violet DJ** → Settings → Bluetooth
3. **Check** "Enable Bluetooth Audio"
4. **Select** device from dropdown
5. **Play** a track to test

---

## 🎵 Loading Your First Track

### From File

1. **Click "Load"** on Deck 1 or Deck 2
2. **Browse** to your music folder
3. **Select** an MP3, WAV, or FLAC file
4. **Waveform displays** automatically
5. **Click "Play"** to start mixing

### Supported Formats
- MP3, WAV, FLAC, OGG, AAC, M4A, ALAC, AIFF, WMA

---

## 🎛️ Basic Mixing

### Simple DJ Mix (2 Tracks)

**Step 1: Load Tracks**
```
Deck 1: Load "Track_A.mp3"
Deck 2: Load "Track_B.mp3"
```

**Step 2: Monitor Levels**
```
- Ensure Level Meters show green (not red)
- Adjust Deck 1 fader to -3dB if too loud
```

**Step 3: Start Playback**
```
- Click Play on Deck 1
- Listen to track (Cue with headphones)
- Click Play on Deck 2 when ready to transition
```

**Step 4: Mix with Crossfader**
```
- Crossfader centered (50%) = Both decks equal
- Move left = More Deck 1
- Move right = More Deck 2
```

**Step 5: Beatmatch (Optional)**
```
- Use Pitch slider on Deck 2 to match BPM
- When beats align, transition complete!
```

---

## ⚙️ Audio Settings

### Selecting Audio Backend

**Via GUI:**
```
Settings Tab → Audio Backend Dropdown
1. PulseAudio (Recommended for most)
2. ALSA (Low-latency option)
3. JACK (Professional studios)
```

**Via Command Line:**
```bash
violet-dj --audio-backend pulseaudio
```

### Sample Rate

**Default:** 48 kHz (Industry standard)

**Change in Settings:**
```
Settings → Audio Configuration → Sample Rate
- 44.1 kHz (CD quality)
- 48 kHz (Professional) ← Recommended
- 96 kHz (High-resolution)
```

### Buffer Size

**Default:** 256 samples (Safe for most systems)

**Adjust for latency:**
```
Lower = Less latency, more CPU usage
- 128 samples (High-end systems only)
- 256 samples (Recommended default)
- 512+ samples (Low-end systems)
```

---

## 🚀 Next Steps

1. **[User Manual](USER_MANUAL.md)** - Learn all features
2. **[Hardware Setup](HARDWARE_SETUP.md)** - Connect your equipment
3. **[MIDI Mapping](MIDI_MAPPING.md)** - Customize your controller
4. **[Troubleshooting](TROUBLESHOOTING.md)** - Fix common issues

---

## 💬 Getting Help

- **📖 Documentation**: https://violet-dj.github.io
- **🐛 Issues**: https://github.com/violet-dj/violet-dj-mixer/issues
- **💬 Discussions**: https://github.com/violet-dj/violet-dj-mixer/discussions
- **🎵 Discord**: [Join community](https://discord.gg/violet-dj)

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] Application launches without errors
- [ ] Audio devices detected in Settings
- [ ] Can load an audio file
- [ ] Can play audio (hear sound output)
- [ ] MIDI controller detected (if connected)
- [ ] Bluetooth devices visible (if enabled)

**If any checks fail**, see [Troubleshooting](TROUBLESHOOTING.md).

---

Happy Mixing! 🎧
