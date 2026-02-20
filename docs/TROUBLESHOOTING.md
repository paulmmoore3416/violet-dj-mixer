# Troubleshooting Guide

## 🔍 Common Issues & Solutions

---

## 🔊 Audio Issues

### No Sound Output

**Problem:** Application runs but no audio heard from speakers/headphones.

**Solutions:**

```bash
# 1. Check audio devices detected
violet-dj --list-devices

# 2. Verify audio backend running
pactl info  # For PulseAudio
alsactl info  # For ALSA

# 3. Test audio system
speaker-test -t sine -f 1000 -l 1

# 4. Check volume levels
alsamixer  # ALSA mixer
pavucontrol  # PulseAudio mixer
```

**Steps to Fix:**
1. Open Settings Tab
2. Check Audio Backend: PulseAudio / ALSA
3. Verify Output Device selected
4. Increase Master fader to 75%+
5. Check Ubuntu volume not muted (speaker icon)
6. Restart audio backend:
   ```bash
   pulseaudio --kill && sleep 2 && pulseaudio --start
   ```

### Crackling/Distorted Audio

**Cause:** Buffer underruns or incompatible sample rate

**Fix:**
1. Settings Tab → Buffer Size
2. Increase from 256 to 512 samples
3. Reduce system CPU load (close other apps)
4. Check audio cables for interference
5. Use shielded audio cables

### Low Volume

**Check:**
1. Master Fader set to 100% (top position)
2. Ubuntu system volume at 80%+
3. Speaker/headphone volume at 50%+
4. Track file not recorded at low level

```bash
# Check track loudness
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1:noprint_wrappers=1 track.mp3
```

### Mono Output (Not Stereo)

**Problem:** Audio in one channel only

```bash
# Check speaker/headphone connection
# Verify stereo device selected in Settings
# Test different output device

# Force stereo output
violet-dj --force-stereo
```

---

## 🎧 MIDI Controller Issues

### Controller Not Detected

**Problem:** USB MIDI controller connected but not appearing in app.

**Diagnosis:**
```bash
# List MIDI devices
aseqdump -l

# List USB devices
lsusb | grep -i audio
lsusb | grep -i midi

# Check for kernel driver
dmesg | tail -20
```

**Solutions:**

1. **Verify Connection:**
   - Try different USB port
   - Use powered USB hub
   - Check USB cable quality

2. **Install Drivers:**
   ```bash
   sudo apt update
   sudo apt install linux-image-extra-$(uname -r)
   # Reboot
   ```

3. **Violet DJ Detection:**
   - Controllers Tab → Click "Detect"
   - Wait 10 seconds for scan
   - Disconnect/reconnect device
   - Try "Detect" again

4. **Manual MIDI Connection:**
   ```bash
   # Find MIDI client ID
   aconnect -l
   
   # Connect manually
   aconnect <client>:0 14:0
   ```

5. **Try Different MIDI Library:**
   ```bash
   violet-dj --midi-backend jack
   ```

### MIDI Buttons/Knobs Not Working

**Problem:** Controller detected but controls not responding.

**Fix:**

1. **Clear Mappings:**
   ```
   Controllers Tab → Remove Old Mappings
   → Detect again
   ```

2. **Test MIDI Input:**
   ```bash
   aseqdump -p <device>
   # Move controller knob - should see data
   ```

3. **Check Mapping:**
   ```
   MIDI Mapping Tab
   → Verify control mapped to function
   → Right-click to edit
   ```

4. **Reload Mapping Profile:**
   ```
   Settings → Load Default Mapping
   ```

### Latency/Lag in MIDI

**Problem:** Controller response delayed.

**Solutions:**
1. Settings → Reduce Buffer Size (256 → 128)
2. Settings → Audio Backend → Switch to JACK
3. Close background applications
4. Disable Bluetooth on Ubuntu machine
5. Use USB 3.0 port instead of 2.0

---

## 🎵 Audio File Issues

### Can't Open Audio File

**Error:** "Unsupported format" or file won't load.

**Check Supported Formats:**
```
✓ MP3  ✓ WAV  ✓ FLAC  ✓ OGG  ✓ AAC
✓ M4A  ✓ ALAC ✓ AIFF  ✓ WMA
```

**If file format supported:**

```bash
# Check file validity
ffprobe track.mp3

# Try converting with FFmpeg
ffmpeg -i track.mp3 -codec copy track_converted.mp3
```

**If format not supported:**
```bash
# Convert to supported format
ffmpeg -i track.wma -c:a libmp3lame track.mp3
```

### Waveform Not Displaying

**Problem:** No visual waveform in deck.

**Cause:** Audio decoder issue or corrupt file

**Fix:**
1. Try different audio file
2. Settings → Refresh Visualizers
3. Restart application
4. Check file not corrupted:
   ```bash
   ffplay track.mp3  # Should play
   ```

### Slow Track Loading

**Problem:** Takes >5 seconds to load track.

**Solution:**
1. Use SSD instead of HDD
2. Close other applications
3. Check file size (>500MB files slower to analyze)
4. Disable Waveform Caching (if available):
   ```
   Settings → Waveform Analysis → Disable Pre-cache
   ```

---

## 🔗 Bluetooth Issues

### Bluetooth Devices Not Found

**Problem:** No Bluetooth devices appear in Violet DJ.

```bash
# Check Bluetooth enabled
rfkill list bluetooth

# If blocked, unblock
rfkill unblock bluetooth

# Check Bluetooth service
sudo systemctl status bluetooth
```

**Pair Device First:**
1. Ubuntu Settings → Bluetooth
2. Toggle Bluetooth On
3. Put device in pairing mode
4. Click device name to pair
5. Then check Violet DJ Settings

### Can't Connect to Paired Device

**Issue:** Device paired but not connecting in app.

```bash
# List paired devices
bluetoothctl paired-devices

# Manually connect
bluetoothctl connect <MAC_ADDRESS>
```

**In Violet DJ:**
1. Settings Tab → Bluetooth
2. Check "Enable Bluetooth Audio"
3. Uncheck "Enable Multiple Bluetooth" (test single device first)
4. Select device from dropdown
5. If still no audio, restart:
   ```bash
   sudo systemctl restart bluetooth
   ```

### Multiple Bluetooth Connections Not Working

**Limit:** Most Bluetooth adapters support 1-2 simultaneous connections.

**Check Connection Count:**
```bash
bluetoothctl info  # Shows connected devices
```

**Fix:**
1. Verify adapter supports multi-connect:
   ```bash
   hciconfig
   ```
2. Some devices must disconnect when another connects
3. Try "Multiple Bluetooth" toggle in Settings Off/On
4. Reconnect devices in order

### Bluetooth Audio Choppy/Stuttering

**Cause:** Interference from Wi-Fi (both use 2.4GHz)

**Solutions:**
1. Move away from Wi-Fi router
2. Use 5GHz Wi-Fi if available
3. Disable Wi-Fi temporarily:
   ```bash
   nmcli radio wifi off
   ```
4. Close Bluetooth app on other devices
5. Reduce Bluetooth device distance (<5m)
6. Use Bluetooth 5.0+ devices (better range)

---

## 📡 Wi-Fi Device Issues

### Wi-Fi Devices Not Discovered

**Problem:** No network audio devices showing.

**Check Network:**
```bash
# Verify Wi-Fi connected
nmcli connection show

# Test network connectivity
ping 8.8.8.8
```

**Enable Discovery:**
```
Settings Tab → Network Configuration
✓ Enable Wi-Fi Device Discovery
```

**Manual mDNS Discovery:**
```bash
sudo apt install avahi-discover
avahi-discover &  # Search for Bonjour services
```

### Connection to Network Device Fails

**Debug:**
```bash
# Check firewall
sudo ufw status

# If blocking, allow local network
sudo ufw allow from 192.168.1.0/24
```

**Test Connectivity:**
```bash
# Ping device IP
ping 192.168.1.100

# Test audio streaming
aplay /dev/tcp/192.168.1.100/5353
```

---

## 🖥️ Application Issues

### Application Won't Start

**Error:** "Permission denied" or immediate crash.

```bash
# Check permissions
ls -la /usr/bin/violet-dj
# Should show: -rwxr-xr-x

# Fix permissions
sudo chmod +x /usr/bin/violet-dj

# Run with debug
violet-dj --debug

# Check logs
cat ~/.violet_dj/violet_dj.log
```

### High CPU Usage

**Problem:** Application uses 80%+ CPU.

**Optimization:**

```
Settings Tab:
1. Reduce visualization quality
2. Increase buffer size (512 samples)
3. Disable waveform pre-analysis
4. Close other applications
```

**Terminal Fix:**
```bash
# Lower priority
nice -n +10 violet-dj
```

### Memory Leak (RAM keeps increasing)

**Problem:** RAM usage grows over time.

**Report Issue:**
```bash
# Get memory info
top -b -n 1 | grep violet-dj
free -h

# Copy full output to GitHub issue
```

**Workaround:** Restart app periodically

### GUI Freezes/Unresponsive

**Cause:** Large file processing

**Fix:**
1. Don't load files >1GB
2. Increase buffer size
3. Close background applications
4. Force quit:
   ```bash
   pkill -9 violet-dj
   ```

---

## 💾 Installation/Update Issues

### .deb Installation Fails

```bash
# Check for broken dependencies
sudo apt --fix-broken install

# Full install
sudo apt autoremove
sudo apt clean
sudo apt install violet-dj-mixer

# If still fails
sudo dpkg --configure -a
```

### Can't Uninstall Previous Version

```bash
# Remove completely
sudo apt remove --purge violet-dj-mixer

# Clean config
rm -rf ~/.config/violet-dj
rm -rf ~/.violet_dj

# Reinstall
sudo apt install violet-dj-mixer
```

### Update from Source Fails

```bash
# Pull latest code
git pull origin main

# Clean build
rm -rf build dist *.egg-info
pip install --upgrade -r requirements.txt

# Reinstall
python3 setup.py install --user
```

---

## 🐛 Getting More Help

### Enable Debug Logging

```bash
# Full debug output
violet-dj --loglevel DEBUG

# Save debug log
violet-dj --loglevel DEBUG > debug.log 2>&1

# Attach to GitHub issue
```

### Collect System Information

```bash
# Generate system report
violet-dj --system-info > report.txt

# Includes:
# - Ubuntu version
# - Python version
# - Audio backends available
# - Connected devices
# - Installed dependencies
```

### Report a Bug

1. [Create GitHub Issue](https://github.com/violet-dj/violet-dj-mixer/issues/new)
2. Include system report (`--system-info`)
3. Describe steps to reproduce
4. Attach debug log (`--loglevel DEBUG`)
5. Attach screenshots if applicable

---

## 📞 Support Resources

- **GitHub Issues**: [Report bugs](https://github.com/violet-dj/violet-dj-mixer/issues)
- **Discussions**: [Ask questions](https://github.com/violet-dj/violet-dj-mixer/discussions)
- **Discord Community**: [Chat with users](https://discord.gg/violet-dj)
- **Documentation**: [Full guides](https://violet-dj.github.io)

---

## ✅ Quick Checklist

System not working? Try this:

- [ ] Restart Violet DJ application
- [ ] Restart audio backend (PulseAudio/ALSA)
- [ ] Disconnect/reconnect devices
- [ ] Check Ubuntu system volume
- [ ] Verify audio output device selected
- [ ] Update system: `sudo apt update && sudo apt upgrade`
- [ ] Restart Ubuntu machine
- [ ] Reinstall from scratch: `sudo apt remove --purge violet-dj-mixer`

Still stuck? [Open an issue](https://github.com/violet-dj/violet-dj-mixer/issues)!

---

Happy Mixing! 🎧
