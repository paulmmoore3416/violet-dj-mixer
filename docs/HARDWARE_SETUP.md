# Hardware Setup Guide

## 🎛️ DJ Controllers

### Universal MIDI Setup

All USB MIDI controllers work via standard MIDI protocol:

1. **Connect** via USB
2. **Violet DJ** will auto-detect
3. **Controllers tab** → See mapped controls
4. **Customize** mappings as needed

### Supported Manufacturers

**Pioneer Equipment**
- DDJ-400, DDJ-SB3, DDJ-SZ2, DDJ-RX, DDJ-1000
- CDJ Series (Mixers & Players)
- DJM Mixers (DJM-900NXS2, DJM-700, etc.)

**Numark**
- Numark Mixtrack Series
- Numark NS7III
- DJ2GO Touch

**Reloop**
- Reloop Terminal Mix
- Reloop Beat Mix
- RP-2000M

**Native Instruments**
- Traktor Kontrol Series
- Traktor Audio Interfaces

**Denon DJ**
- Denon DJ Prime
- MCX8000

**Rane**
- Rane Seventy
- Rane Seventy-Two

**Other Equipment**
- Allen & Heath (Xone series)
- Akai Professional
- Technics Turntables
- Stanton Turntables
- Korg Instruments
- Roland Devices
- Yamaha Controllers

### Manual Mapping

For unsupported controllers:

1. **Controllers Tab**
2. **MIDI Mapping** section
3. **Right-click** on mixer function
4. **Move controller knob/slider**
5. **Mapping saved automatically**
6. **Test** control movement

---

## 🎙️ Audio Interfaces

### USB Audio Interfaces

**Installation:**
```bash
# Connect interface via USB
# Violet DJ auto-detects

# Verify in Settings
Settings → Audio Devices → Output Device
```

**Recommended Interfaces:**
- Focusrite Scarlett Series
- Native Instruments Komplete Audio
- PreSonus AudioBox
- Behringer U-Phoria
- Roland Rubix Series
- Audient ASP800
- RME Babyface

### Professional Sound Cards

**PCI/Thunderbolt Cards:**
```bash
# List installed sound cards
aplay -l
cat /proc/asound/cards
```

**JACK Configuration (Advanced):**
```bash
# For zero-latency professional setup
# Open JACK controller
qjackctl &

# Configure sample rate, buffer size
# Connect Violet DJ to JACK inputs/outputs
```

---

## 🔊 Speakers & Headphones

### Connect Speakers

**USB Powered Speakers:**
1. Connect to USB port
2. Settings → Audio Devices → Output
3. Select speakers from dropdown
4. Test with track

**3.5mm Audio Out:**
1. Connect to audio interface output
2. Settings → Audio Devices
3. Select device
4. Test playback

### Connect Headphones

**Cue/Monitor Setup:**
```
1. Connect headphones to audio interface
2. Settings → Cue Output Device
3. Select headphone output
4. Click "Cue" button on deck to monitor
```

---

## 🎧 Bluetooth Devices

### Pairing Bluetooth Devices

**Ubuntu Settings:**
1. Open Settings
2. Click Bluetooth (left sidebar)
3. Toggle Bluetooth On
4. Enable pairing mode on device (headphones, speaker)
5. Device appears in list
6. Click to pair & connect

### In Violet DJ

**Single Device:**
```
Settings Tab → Bluetooth Section
1. Check "Enable Bluetooth Audio"
2. Select device from dropdown
3. Test audio output
```

**Multiple Devices (Simultaneous):**
```
Settings → Bluetooth Configuration
1. Check "Enable Multiple Bluetooth Connections"
2. Pair multiple devices in Ubuntu Settings first
3. Violet DJ will manage all connections
4. Disable individual devices in Settings as needed
```

### Troubleshooting Bluetooth

**Device not found:**
```bash
# Restart Bluetooth
sudo systemctl restart bluetooth

# Check pairing
bluetoothctl paired-devices
```

**Connection drops:**
```
- Keep device within 10 meters of Ubuntu machine
- Avoid Wi-Fi interference (2.4GHz band)
- Update Bluetooth drivers: sudo apt update && sudo apt upgrade
```

**Poor audio quality:**
```
- Move closer to machine
- Check battery level on device
- Disable other 2.4GHz devices
- Use LDAC codec if available (Bluetooth 5.0+ devices)
```

---

## 📡 Wi-Fi Audio Devices

### Network Audio Setup

**Supported Protocol:**
- Bonjour/mDNS (Apple AirPlay, Sonos, etc.)
- DLNA (Network audio streaming)

**Connection:**
1. Ensure device on same Wi-Fi network
2. Settings → Network Audio
3. Check "Enable Wi-Fi Device Discovery"
4. Available devices appear automatically
5. Click to connect

### Examples

**Apple AirPlay:**
- AirPods Pro/Max
- HomePod
- Mac computers

**Sonos System:**
- Sonos speakers automatically discovered
- Select for Violet DJ output

**Google Devices:**
- Google Home speakers
- Chromecast Audio devices

---

## 🎹 MIDI Instruments

### Connect MIDI Instruments

**USB MIDI:**
```bash
# Connect keyboard, synthesizer, or drum machine via USB
# Open Controllers Tab
# MIDI Instrument appears in device list
# Map controls as needed
```

**5-pin DIN MIDI:**
```bash
# Requires USB MIDI adapter
# Connect adapter to USB port
# Violet DJ detects adapter
# Map controls
```

### Supported Instruments

- **Keyboards**: Yamaha PSR, Roland, Korg, Casio
- **Synthesizers**: Moog, Elektron, Native Instruments
- **Drum Machines**: TR-808, TR-909, MPC-1000, etc.
- **Controllers**: AKAI APC, Push 2, Launchpad, etc.

---

## 🔌 Turntables

### Analog Turntable Setup

**Connect via Audio Interface:**
```
1. Turntable (RCA) → Audio Interface (Phono Input)
   - Use high-quality RCA cables
   - Ensure turntable grounded

2. Audio Interface (USB) → Ubuntu Computer

3. Violet DJ Settings → Audio Input Device
   - Select audio interface
   - Select turntable input (usually Line/Phono)
```

**Preamp Requirement:**
- Most turntables need preamp (included or external)
- Check interface has preamp switch

### Technics SL-1200

Professional turntable integration:
```
1. Connect to audio interface (Phono input)
2. Settings → Detect turntable input
3. Control via jog wheel (standard USB)
4. Map pitch/cue controls in MIDI Mapping
```

---

## 🎤 Microphone Setup

### Connect Microphone

```
1. Microphone (XLR) → Audio Interface (XLR Input)
2. Audio Interface (USB) → Ubuntu Computer
3. Violet DJ Settings → Microphone Input
4. Select microphone from dropdown
5. Adjust input gain
```

### Live DJ Setup

**2-Deck + Microphone:**
```
Deck 1 (Channel 1) → Music Track 1
Deck 2 (Channel 2) → Music Track 2
Microphone (Channel 3) → DJ vocals

Mix all with Master fader
Monitor each with Cue
```

---

## 🎬 Video Devices

### Connect Webcam (for VJ)

```bash
# List video devices
v4l2-ctl --list-devices

# Video I/O
Settings → Video Input Device → Select webcam
```

### HDMI Video Out (VJ Performance)

```bash
# For display/projector output
# Connect HDMI monitor/projector to Ubuntu machine
# Violet DJ can output visualization to secondary display
```

---

## 🔧 Troubleshooting

### Device Not Detected

```bash
# Check USB devices
lsusb
lsusb | grep -i audio
lsusb | grep -i midi

# Check MIDI
aseqdump -l
amidi -l

# Reinstall udev rules
sudo violet-dj --install-udev-rules
```

### Poor Audio Quality

```bash
# Check sample rate
violet-dj --check-audio

# Reduce buffer latency (Settings)
# Increase system volume before clipping
# Use professional audio cables
```

### Controller Buttons Not Working

```bash
# Test MIDI input
aseqdump -l  # Shows MIDI devices
aconnect -l  # Shows MIDI connections

# Rebuild MIDI connection
Controllers Tab → Disconnect → Re-detect
```

---

## 📚 Advanced Setup

### JACK Configuration

For professional low-latency setup:

```bash
# Install JACK
sudo apt install jackd2 qjackctl

# Start JACK with Violet DJ
qjackctl &
# Configure: 48kHz, 256 samples, Real-time enabled

# In Violet DJ
Settings → Audio Backend → JACK
# Auto-connects to JACK
```

### Multi-Device Routing

```
JACK Patchbay can route:
- Turntable → Deck 1
- Microphone → Channel 3
- External synthesizer → Sampler
- All mixed through Master
- Output to multiple destinations
```

---

## ✅ Setup Verification

Test all connected devices:

```bash
# Audio Test
violet-dj --test-audio

# MIDI Test
violet-dj --test-midi

# Device Report
violet-dj --list-devices
```

---

Happy Mixing! 🎧
