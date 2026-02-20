# Violet DJ Mixer - Complete User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Mixer Basics](#mixer-basics)
3. [Controls Reference](#controls-reference)
4. [Loading & Playing Tracks](#loading--playing-tracks)
5. [Mixing Techniques](#mixing-techniques)
6. [Using Effects](#using-effects)
7. [Working with Controllers](#working-with-controllers)
8. [Advanced Features](#advanced-features)

---

## Introduction

Violet DJ Mixer is a professional digital mixing board designed to provide features comparable to high-end commercial DJ software. 

This manual covers all features and functions. For quick start, see [Getting Started Guide](GETTING_STARTED.md).

---

## Mixer Basics

### The Interface

The main mixing interface consists of several key areas:

**Left Panel: Deck 1**
- Track loaded and playback controls
- Waveform display
- Pitch/tempo control
- Position slider

**Center Panel: Master Controls**
- Crossfader (blend between Deck 1 & Deck 2)
- Master volume fader
- Master level meter
- Spectrum analyzer

**Right Panel: Deck 2**
- Track loaded and playback controls
- Waveform display
- Pitch/tempo control
- Position slider

**Bottom: Effects & Settings**
- Effect selection and controls
- Settings tabs
- Device status

### The Faders

Three types of faders in Violet DJ:

1. **Channel Faders** (Vertical)
   - Control level of each deck
   - Range: -∞ to +6dB
   - Middle position = 0dB

2. **Crossfader** (Horizontal)
   - Blend between decks
   - Left = Deck 1 only
   - Center = Both decks equal
   - Right = Deck 2 only

3. **Master Fader** (Vertical)
   - Controls overall output level
   - Should typically be at 75-100%
   - Prevent clipping (red zone)

---

## Controls Reference

### Channel Controls

**Fader**
- Volume level for that channel
- Smooth fade in/out

**EQ Knobs (Low, Mid, High)**
- Low: 50Hz - 200Hz (bass)
- Mid: 200Hz - 2kHz (vocals)
- High: 2kHz - 20kHz (treble)
- Center = 0dB (no change)
- Rotation = ±12dB adjustment

**Cue Button**
- Monitor track in headphones
- Solo track playback
- Useful for beat-matching before mixing

**Solo Button**
- Isolate channel to main output
- Used with Cue for monitoring

**Mute Button**
- Silence the channel
- Useful for effects layering

### Master Controls

**Crossfader**
- Blend between left (Deck 1) and right (Deck 2)
- S-curve for faster blending
- Linear for gradual transition

**Master Volume**
- Overall output level
- Typically 75-90% for proper headroom
- Leave 6dB of headroom (prevent clipping)

**Meter**
- Visual representation of levels
- Green = Normal (-12dB to 0dB)
- Yellow = Loud (0dB to +3dB)
- Red = Clipping/Distortion (avoid)

---

## Loading & Playing Tracks

### Loading a Track

**Method 1: Load Button**
1. Click "Load" on Deck 1 or Deck 2
2. Navigate to music folder
3. Select audio file (MP3, WAV, FLAC, etc.)
4. Click "Open"
5. Waveform displays in deck

**Method 2: Drag & Drop**
1. Open file manager with music library
2. Drag file onto deck
3. Waveform displays automatically

### Track Information Display

Once loaded, the deck shows:
- **Track Name**: File name
- **Duration**: Total length
- **BPM**: Beats per minute (auto-detected)
- **Waveform**: Visual representation
- **Key**: Detected musical key

### Playback Controls

**Play Button**
- Starts playback from current position
- Continues from where left off

**Pause Button**
- Pauses without stopping
- Resume from same position
- Different from Stop

**Cue Button**
- Sets cue point
- Can be multiple cue points
- Jump to cue with Cue button while paused

**Stop Button**
- Stops playback
- Returns to beginning

**Next/Previous Buttons**
- Skip to next/previous track in playlist
- (If using Playlist mode)

### Position Control

**Position Slider**
- Shows current playback position
- Drag to jump to specific point in track
- Visual feedback of position in waveform

**Time Display**
- Current: Shows elapsed time
- Remaining: Shows time left in track
- Duration: Total track length

### Pitch/Speed Control

**Pitch Slider**
- Adjusts playback speed and pitch
- Range: -10% to +10% (typical)
- Center = Normal speed (100%)
- Left = Slower (e.g., 95%)
- Right = Faster (e.g., 105%)

**Sync Button** (when available)
- Auto-matches tempo of Deck 2 to Deck 1
- Useful for beat-matching
- Calculates BPM difference automatically

---

## Mixing Techniques

### Basic 2-Deck Mix

**Setup**
```
Deck 1: Load "Track A"
Deck 2: Load "Track B" (ready for transition)
```

**Mixing Steps**

1. **Start Playback**
   ```
   Deck 1: Click Play
   Listen to music for ~8 bars
   ```

2. **Monitor Second Track**
   ```
   Deck 2: Cue button (listen in headphones)
   Adjust volume to match Deck 1
   ```

3. **Beat Match** (optional)
   ```
   Deck 2: Adjust Pitch slider until BPM matches Deck 1
   Watch waveform peaks align with beat
   Listen for beat synchronization
   ```

4. **Transition**
   ```
   When ready (near musical break):
   - Move Crossfader from 0% (all Deck 1) to 100% (all Deck 2)
   - Or use Deck 1 fader to fade out while Deck 2 fades in
   - Smooth transition over 8-32 bars
   ```

5. **Load Next Track**
   ```
   Once Deck 2 is now playing:
   - Deck 1: Load next track
   - Repeat from Step 2
   ```

### EQ Techniques

**Kill Bass**
- Set Low EQ to -12dB
- Removes bass from track
- Creates space or builds tension

**EQ Sweep**
- Gradually turn EQ knob
- Creates filter effect
- Builds excitement during transition

**Isolate Elements**
- Reduce Mid to isolate bass/treble
- Highlight vocals (increase Mid)
- Create unique soundscape

### Crossfader Techniques

**Linear Fade**
- Slow, smooth movement
- Even volume change
- Natural transition

**Curve Fade**
- Quick swap between tracks
- Minimal overlap period
- Dramatic effect

**Crabbing**
- Rapid back-and-forth movement
- Creates stuttering effect
- Builds energy

---

## Using Effects

### Available Effects

**Echo**
- Repeats audio signal
- Parameters:
  - Mix: Dry/wet balance
  - Time: Delay between repeats (ms)
  - Feedback: How many repeats

**Reverb**
- Simulates room reflections
- Parameters:
  - Mix: Effect intensity
  - Size: Room size simulation
  - Damping: High frequency reduction

**Chorus**
- Layers with delayed copies
- Parameters:
  - Mix: Wet/dry
  - Rate: LFO frequency
  - Depth: Amount of variation

**Flanger**
- Comb filter effect
- Parameters:
  - Mix: Effect intensity
  - Rate: LFO frequency
  - Feedback: Amount fed back

**Phaser**
- All-pass filter cascade
- Parameters:
  - Mix: Effect intensity
  - Rate: LFO speed
  - Feedback: Self-resonance

**Distortion**
- Adds harmonic content
- Parameters:
  - Mix: Effect amount
  - Drive: Input gain
  - Tone: High frequency content

**Delay**
- Repeats with specific interval
- Parameters:
  - Mix: Dry/wet balance
  - Time: Delay duration
  - Feedback: Number of repeats

### Applying Effects

1. **Select Effect**
   ```
   Effects Tab → Check checkbox for effect
   ```

2. **Adjust Parameters**
   ```
   Move Mix and Time sliders
   Listen to output
   Adjust for desired effect
   ```

3. **Assign to Channel**
   ```
   Effects Tab → Assign dropdown
   Select Deck 1, Deck 2, or Master
   Effect applies to selection
   ```

4. **Disable Effect**
   ```
   Uncheck effect checkbox
   Effect removed from signal
   ```

### Effect Tips

- **Build Excitement**: Add Reverb during transitions
- **Create Space**: Use Echo on breaks
- **Smooth Transitions**: Chorus on overlapping sections
- **Unique Sounds**: Combine multiple effects
- **Not Overdo It**: Balance effect with dry signal

---

## Working with Controllers

### MIDI Controller Setup

**Connect and Detect**
```
1. Connect controller via USB
2. Controllers Tab → Click "Detect"
3. Controller appears in list
4. Mappings auto-load
```

**Test Controller**
```
Move physical control
Should see corresponding UI element move
Audio responds accordingly
```

### MIDI Mapping

**View Current Mappings**
```
Controllers Tab → MIDI Mapping
Shows all mapped controls
Indicates channel and function
```

**Create Custom Mapping**
```
1. MIDI Mapping Table
2. Right-click on mixer function
3. Move physical controller knob/slider
4. Mapping recorded automatically
5. Name the control
6. Click Save
```

**Save Mapping Profile**
```
Controllers Tab → Save Profile
Give profile meaningful name
Useful for switching controller presets
```

**Load Mapping Profile**
```
Controllers Tab → Load Profile
Select saved profile
All mappings restored
```

---

## Advanced Features

### Hot Cues

Create quick jump points in tracks:

```
1. Deck Detail → Click "Set Cue" at position
2. Track displays cue points on waveform
3. Click cue point to jump to location
4. Useful for beat drops, breakdowns, etc.
```

### Looping

Create repeating sections:

```
1. Deck Detail → Set Loop Start (where to begin)
2. Continue playback
3. Set Loop End (where to loop back)
4. Playback repeats between points
5. Adjust Loop Length for dynamic loops
```

### Sampler

Record and playback short audio clips:

```
1. Effects Tab → Sampler
2. Click Record to capture audio
3. Click Stop to end recording
4. Playback samples with buttons
5. Layer samples for complex textures
```

### BPM Sync

Synchronize track tempos:

```
1. Deck 2 → Click Sync
2. Auto-matches Deck 2 BPM to Deck 1
3. Useful for seamless mixing
4. Manual adjustment still possible
```

### Visualization

Monitor audio visually:

```
View Tab → Toggle Visualization
- Waveform display: Real-time playback
- Spectrum analyzer: Frequency breakdown
- Level meters: Input/output levels
```

---

## Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| Space | Play/Pause active deck |
| Left Arrow | Rewind deck 5 seconds |
| Right Arrow | Forward deck 5 seconds |
| M | Toggle Master mute |
| C | Toggle Crossfader |
| E | Toggle effects |
| L | Toggle loop |
| S | Toggle sync |

---

## Best Practices

### Audio Levels
- Maintain -6dB of headroom on Master
- Peak levels in green zone (not red)
- Match input levels before mixing

### Beat Matching
- Use BPM to determine pitch needed
- Waveform peaks should align
- Listen for beat synchronization

### Transitions
- Plan transition ahead (count down bars)
- Use effects to build excitement
- Smooth volume changes

### Controller Use
- Test MIDI mapping before performance
- Save multiple profiles for different setups
- Keep controller firmware updated

### File Management
- Organize music library by BPM/genre
- Use consistent file naming
- Pre-load tracks during performance

---

For more help, see [Troubleshooting Guide](TROUBLESHOOTING.md)

Happy Mixing! 🎧
