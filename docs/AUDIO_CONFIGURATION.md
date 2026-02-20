# Violet DJ Mixer - Audio Configuration Guide

## Audio Backends

### PulseAudio (Recommended)

**Best for:** Most Ubuntu users, modern desktops

**Pros:**
- Pre-installed on Ubuntu
- User-level daemon (no root required)
- Handles multiple applications
- Automatic device switching

**Configuration:**
```bash
# Check PulseAudio status
pactl info

# List audio devices
pactl list sinks

# Set default sink (output)
pactl set-default-sink <sink-name>

# List audio sources (input)
pactl list sources
```

### ALSA (Advanced Linux Sound Architecture)

**Best for:** Low-latency, professional recording

**Pros:**
- Low-latency performance
- Direct hardware access
- Minimal overhead

**Configuration:**
```bash
# List ALSA devices
aplay -l

# Configure ALSA
sudo alsamixer

# Save ALSA configuration
sudo alsactl store
```

### JACK (Jack Audio Connection Kit)

**Best for:** Professional studios, complex routing

**Pros:**
- Professional-grade latency
- Complex routing capabilities
- Network audio support

**Installation:**
```bash
sudo apt install jackd2 qjackctl
```

---

## Sample Rate Configuration

### Available Sample Rates

| Rate | Use Case | Quality |
|------|----------|---------|
| 44.1 kHz | CD audio, MP3 | Standard |
| 48 kHz | Professional, video | Industry standard |
| 96 kHz | High-resolution | Studio quality |
| 192 kHz | Mastering | Maximum quality |

### Set Sample Rate

**Via GUI:**
Settings Tab → Audio Configuration → Sample Rate

**Via Command Line (ALSA):**
```bash
# Edit ~/.asoundrc
pcm.!default {
    type hw
    card 0
}
ctl.!default {
    type hw
    card 0
}
```

### Supported Codecs

**Lossless (Recommended for Production)**
- WAV - Waveform Audio File Format
- FLAC - Free Lossless Audio Codec
- ALAC - Apple Lossless Audio Codec
- AIFF - Audio Interchange File Format

**Lossy (Good for Streaming)**
- MP3 - MPEG-1 Audio Layer III
- OGG - OGG Vorbis
- AAC - Advanced Audio Coding
- M4A - MPEG-4 Audio
- WMA - Windows Media Audio

---

## Driver Installation

### USB Audio Drivers

```bash
# Install audio support
sudo apt install alsa-firmware alsa-ucm-conf

# Load USB audio module
sudo modprobe snd_usb_audio

# Make persistent
echo "snd_usb_audio" | sudo tee -a /etc/modules
```

### MIDI Drivers

```bash
# Install MIDI support
sudo apt install alsa-utils libasound2-dev

# List MIDI devices
aseqdump -l

# Load kernel MIDI modules
sudo modprobe snd_seq_midi_event
sudo modprobe snd_seq_oss
```

### Bluetooth Audio Drivers

```bash
# Install Bluetooth audio support
sudo apt install pulseaudio-module-bluetooth bluez

# Restart PulseAudio
pulseaudio --kill && sleep 1 && pulseaudio --start
```

---

## Latency Optimization

### Buffer Size Settings

```
Buffer Size (Samples) | Latency (ms) | CPU Usage
256                   | 5.3          | Medium
512                   | 10.7         | Low
1024                  | 21.3         | Very Low
```

**Recommended:**
- Recording/DJing: 256 samples
- Playback: 512-1024 samples
- Live Performance: 128-256 samples

### Low-Latency Kernel (Optional)

```bash
# Install low-latency kernel
sudo apt install linux-lowlatency

# Reboot to use new kernel
sudo reboot

# Verify
uname -a | grep lowlatency
```

---

## Testing Audio

### Test Speakers

```bash
# Generate test tone
speaker-test -t sine -f 1000 -l 1

# Play audio file
aplay test.wav

# PulseAudio test
paplay test.wav
```

### Check Audio Levels

```bash
# Interactive ALSA mixer
alsamixer

# PulseAudio mixer GUI
pavucontrol &
```

---

## Troubleshooting

### No Audio Output

```bash
# Check default device
pactl info | grep "Default Sink"

# List all devices
pactl list sinks

# Set default
pactl set-default-sink <name>
```

### Crackling/Noise

```bash
# Increase buffer size (Settings Tab)
# Reduce CPU load
# Update audio drivers
sudo apt update && sudo apt upgrade

# Restart audio
pulseaudio --kill && sleep 2 && pulseaudio --start
```

### Device Not Recognized

```bash
# Check USB connection
lsusb | grep -i audio

# Reload audio modules
sudo modprobe -r snd_usb_audio
sudo modprobe snd_usb_audio

# Check kernel messages
dmesg | tail -20
```

---

## Advanced Configuration

### Multiple Audio Devices

Use JACK for complex routing:

```bash
# Start JACK
qjackctl &

# Configure connections
aconnect -l
```

### Network Audio (RTP)

```bash
# Receive audio over network
jack_netsource -H 192.168.1.100

# Send audio to network
jackd -d netone
```

---

## Audio Codec Installation

### Install Additional Codecs

```bash
# MP3 support (libmpg123)
sudo apt install libmpg123-0

# FLAC support
sudo apt install libflac8

# FFmpeg for comprehensive codec support
sudo apt install ffmpeg

# Verify codecs
ffmpeg -codecs | grep audio
```

---

Happy Mixing! 🎧
