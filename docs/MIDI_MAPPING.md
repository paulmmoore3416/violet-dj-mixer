# MIDI Mapping Guide

## Complete MIDI Controller Configuration

---

## Understanding MIDI

### MIDI Basics

**MIDI (Musical Instrument Digital Interface)**
- Standard protocol for musical devices
- Sends control messages (CC = Control Change)
- CC range: 0-127 values per channel
- 16 channels available per connection

### Controller Types

**Hardware Controllers**
- DJ Mixers with USB/MIDI output
- MIDI keyboards and synthesizers
- Drum machines with MIDI
- Professional turntables

**Controller Elements**
- Knobs (rotary encoders)
- Faders (linear potentiometers)
- Buttons (momentary switches)
- Jog wheels (rotary encoders)

---

## Auto-Detection

### How Violet DJ Detects Controllers

1. **Scan for USB MIDI devices** - Uses ALSA MIDI
2. **Identify manufacturer/model** - Based on USB IDs
3. **Load default mapping** - Pre-built for known models
4. **Apply mappings** - Controls automatically work

### Supported Manufacturers

**Complete List:**
- Pioneer (DDJ, CDJ, DJM series)
- Numark (Mixtrack, Terminal, NS7)
- Reloop (Terminal Mix, RP-2000)
- Native Instruments (Traktor series)
- Denon DJ (Prime, MCX series)
- Rane (Seventy, Seventy-Two)
- Allen & Heath (Xone series)
- Akai Professional (Akai MPCs)
- Technics (SL-1200, SL-100N)
- Stanton (Turntables with MIDI)
- Korg (KORG Volca, NanoKontrol)
- Roland (TR-8, TR-9, other units)
- Yamaha (PSR, DX series)
- Elektron (Rytm, Analog Four)
- Moog (Minitaur, Moogerfooger)

---

## Manual Mapping

### Create Custom Mapping

**Step-by-Step:**

1. **Connect controller via USB**
   ```
   Plug in MIDI controller
   Violet DJ detects automatically
   ```

2. **Open MIDI Mapping**
   ```
   Controllers Tab → MIDI Mapping
   ```

3. **Map a Control**
   ```
   Right-click mixer function (e.g., "Deck 1 Volume")
   Move physical controller knob
   Mapping auto-records MIDI CC value
   Name the mapping
   Click Save
   ```

4. **Test Mapping**
   ```
   Move physical control
   Verify UI responds
   Adjust range if needed
   ```

5. **Save Profile**
   ```
   Controllers Tab → Save Profile
   Name: "My Controller X"
   Contains all mappings
   ```

### MIDI CC Reference

**Common MIDI CC Assignments:**

| CC # | Function | Range |
|------|----------|-------|
| 0-7 | Volume/Pan | 0-127 |
| 8-15 | Pan/Aux | 0-127 |
| 16-19 | Knobs 1-4 | 0-127 |
| 20-23 | Knobs 5-8 | 0-127 |
| 32-39 | LSB (fine control) | 0-127 |
| 64-95 | Switch buttons | 0/127 |
| 120-127 | Channel mode messages | 0/127 |

---

## Mapping Profiles

### Save Profile

```
1. Configure all MIDI mappings
2. Controllers Tab → Save Profile
3. Enter profile name
4. File saved to ~/.config/violet-dj/profiles/
```

### Load Profile

```
1. Controllers Tab → Load Profile
2. Select saved profile
3. All mappings restored
4. Ready to use
```

### Share Profiles

Profiles are stored as JSON:
```bash
~/.config/violet-dj/profiles/my_controller.json
```

**Share with community:**
- Upload to GitHub discussions
- Include controller model
- Include mapping explanation

---

## Popular Controller Mappings

### Pioneer DDJ-400

**Pre-configured Controls:**
- Deck 1 Jog Wheel → Pitch/Seek
- Deck 1 Volume Fader → Channel Volume
- EQ High/Mid/Low → EQ Controls
- Crossfader → Master Crossfader
- CUE/MASTER buttons → Monitor Select
- SYNC button → Beat Sync
- PLAY/PAUSE → Playback Control
- LOAD buttons → Load track

### Numark Mixtrack 3

**Mapping:**
- Left Jog → Deck 1 control
- Right Jog → Deck 2 control
- Crossfader → Master crossfader
- Volume sliders → Channel faders
- EQ knobs → 3-band EQ
- Filter → Low-pass filter
- Cue/Master → Monitor blend

### Reloop Terminal Mix

**Controls:**
- Turntable sections → Deck control
- Mixer channels → Channel faders
- Master volume → Output level
- Monitor section → Headphone mix
- FX section → Effect controls

---

## Advanced Mapping

### Multiple Decks

Map 4-deck setup:

```
Deck 1: Left half of controller
Deck 2: Right half of controller
Deck 3: Top section (if available)
Deck 4: Bottom section (if available)
```

### Customization Examples

**Example 1: EQ Mapping**
```
- Left Knob 1 → Deck 1 Low EQ
- Left Knob 2 → Deck 1 Mid EQ
- Left Knob 3 → Deck 1 High EQ
- Right Knob 1 → Deck 2 Low EQ
- Right Knob 2 → Deck 2 Mid EQ
- Right Knob 3 → Deck 2 High EQ
```

**Example 2: Effect Mapping**
```
- Button 1 → Enable Echo
- Knob 1 → Echo Mix
- Knob 2 → Echo Time
- Button 2 → Enable Reverb
- Knob 3 → Reverb Mix
- Knob 4 → Reverb Size
```

**Example 3: Sampler Mapping**
```
- Pad Bank 1-8 → Sample 1-8
- Slider 1 → Sample Volume
- Slider 2 → Sample Pitch
- Button → Record Sample
```

---

## Troubleshooting Mappings

### Control Not Responding

```
1. Verify MIDI data received
   aseqdump -p <device>
   Move control - should show data
   
2. Check mapping configuration
   Controllers Tab → Review mappings
   
3. Verify control assignment
   Right-click function
   Should show MIDI CC value
   
4. Reload profile
   Controllers Tab → Reload Profile
```

### Inverted Controls

**Problem:** Control backwards (pull fader = increase volume)

**Solution:**
1. Edit mapping
2. Check "Invert" option
3. Save profile

### Latency Issues

```
1. Reduce buffer size (Settings Tab)
2. Use USB 3.0 port
3. Disable Wi-Fi/Bluetooth temporarily
4. Close other MIDI applications
```

### Multiple Controllers

**Connect multiple MIDI devices:**

```
1. USB Port 1: Controller A
2. USB Port 2: Controller B
3. USB Port 3: Controller C

Violet DJ detects all three
Load profile for each
Mappings work simultaneously
```

---

## MIDI CC Monitoring

### Debug MIDI Input

```bash
# Monitor all MIDI data
aseqdump -l  # Shows MIDI ports

aseqdump -p <port>  # Monitor specific port
# Move controls to see CC values

# Record MIDI data
arecordmidi -l output.mid  # Records MIDI events
```

### Identify Control Values

```
1. Open MIDI mapping
2. Start MIDI monitor (aseqdump)
3. Move physical control
4. Note the CC value
5. Use that value in mapping
```

---

## Best Practices

### Organization

- **Name mappings clearly:** "EQ High Pass" not "Knob1"
- **Group by function:** All EQ together, all effects together
- **Document ranges:** Note min/max values

### Consistency

- **Keep standard layout:** Volume faders in same position
- **Use industry conventions:** Pan on certain CCs, etc.
- **Test thoroughly:** Verify all controls before performance

### Safety

- **Save before performing:** Test profile in advance
- **Create backups:** Multiple saved profiles
- **Know manual override:** Able to use mouse if needed

---

## Creating Profiles from Scratch

### Complete Walkthrough

```
1. Connect new MIDI controller

2. Controllers Tab → Clear Mappings (if needed)

3. Start mapping:
   - Fader 1 → Deck 1 Volume
   - Fader 2 → Deck 2 Volume
   - Knob 1 → Deck 1 Low EQ
   - Knob 2 → Deck 1 Mid EQ
   - Knob 3 → Deck 1 High EQ
   ... continue for all controls

4. Test each mapping:
   - Move physical control
   - Verify UI responds
   - Check range is correct

5. Save Profile:
   - Name: "My Controller X"
   - Save to library

6. Reload and verify:
   - Close application
   - Restart Violet DJ
   - Load saved profile
   - Test all controls again
```

---

## Sharing Your Mappings

### Contribute to Community

1. Create excellent mapping
2. Test thoroughly
3. Document in detail
4. Share on GitHub Discussions
5. Community benefits from your work!

### Include in Contribution

```
Profile Name: [Controller Model]
Manufacturer: [Brand]
MIDI Config:
- CC 16: Deck 1 Volume
- CC 17: Deck 2 Volume
- ... list all mappings

Notes:
- Any special considerations
- Known issues or workarounds
- Tips for best performance
```

---

## Resources

- **MIDI Spec:** https://www.midi.org/
- **CC Chart:** https://www.midi.org/specifications/item/controller-events
- **Controller Manuals:** Check manufacturer website

---

Happy Mapping! 🎧
