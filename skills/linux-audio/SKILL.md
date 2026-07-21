---

name: linux-audio
description: |
  Use when diagnosing or fixing Linux audio problems on PipeWire or WirePlumber; triggers include "no sound on Linux", "PipeWire audio", "WirePlumber issue", "wrong audio device", and "Pro Audio profile".
tools:
  - terminal
  - read_file
preconditions:
  - PipeWire or PulseAudio running (pactl/wpctl available)
  - alsa-utils installed (amixer, aplay, speaker-test)

---

## Diagnostic Sequence

When the user reports "no audio" but PipeWire/PulseAudio shows sinks running with active streams and non-zero volume, the problem is almost always at the **ALSA hardware mixer layer** — a switch or amplifier that PipeWire's volume controls don't touch.

### Step 1: Quick Sanity Check

```bash
pactl info | grep -E "Server Name|Default Sink"
pactl list short sinks
pactl list short sink-inputs
```

Verify: default sink exists, is not suspended/RUNNING, has sink-inputs feeding it, volume > 0%, not muted.

### Step 2: Check ALSA Hardware Switches

PipeWire volume ≠ ALSA hardware state. Pro Audio profile is especially dangerous — it exposes raw PCM devices and **bypasses all jack detection and port switching**, leaving hardware amps in whatever state they were last left in.

```bash
# Check all relevant mixer controls on the default card
amixer -c0 sget Master
amixer -c0 sget Headphone
amixer -c0 sget 'Headphone+LO'
amixer -c0 sget Speaker
amixer -c0 sget PCM
amixer -c0 sget Front
```

Common gotchas:
- **Headphone switch OFF** — very common. On many codecs (Realtek ALC662, ALC255, etc.), the main analog output path routes through the headphone amplifier, so if the Headphone switch is OFF, NO analog output works — even the rear Line Out jack.
- **Master at low volume** — PipeWire shows 95% but ALSA Master is at 30% with -30dB attenuation.
- **Auto-Mute Mode Enabled** — mutes speakers when something is (or appears to be) plugged into the headphone jack.

### Step 3: Check Jack Detection

```bash
amixer -c0 contents | grep -A2 "Jack" | grep -E "name|values"
```

Jack detection says what's physically connected. Compare with where the user says their speakers/headphones are plugged. Pro Audio profile ignores this entirely.

### Step 4: Inspect Codec Hardware Nodes

When ALSA switches look right but still no sound, the amplifier may be muted at the HDA codec level:

```bash
cat /proc/asound/card0/codec#0 | grep -A10 "Node 0x1b" | grep -E "Node|Amp-Out vals|Pin-ctls|Pin Default"
```

**Critical**: `Amp-Out vals: [0x80 0x80]` means the amplifier is **hardware-muted** (0x80 = mute bit set). `[0x00 0x00]` means unmuted.

### Step 5: Fix

```bash
# Unmute headphone path
amixer -c0 sset Headphone on

# Set Master to 100%
amixer -c0 sset Master 100%

# Verify amp unmuted
cat /proc/asound/card0/codec#0 | grep -A3 "Node 0x1b" | grep "Amp-Out vals"
# Should show: [0x00 0x00]

# Test
speaker-test -D hw:0,0 -t sine -f 440 -l 1 -c 2
# Or: pw-play /usr/share/sounds/alsa/Front_Center.wav
```

## Pro Audio Profile Specifics

When the card is using the `pro-audio` profile (check with `pactl list cards | grep "Active Profile"`), PipeWire creates separate sinks for each PCM device without port switching logic. This means:

- Jack detection is **ignored** — audio goes to hw:0,0 regardless of what's plugged in where
- Traditional profiles (`output:analog-stereo`) show as `available: no` because no port is detected as connected — this is normal, not a bug
- The Pro Audio profile is the correct choice when you want direct PCM access; the traditional profiles are for auto-switching between jacks

## Persistence

ALSA mixer changes made with `amixer sset` survive until reboot. To make permanent:

```bash
sudo alsactl store
```

## Pitfalls

- Never assume PipeWire volume = hardware volume. Always check `amixer` when debugging no-audio issues.
- On Realtek codecs, the Headphone switch often controls the main output amp, not just the front headphone jack. If it's off, ALL analog output may be dead.
- `Master` being at 64% with `[on]` looks fine in PipeWire but is -23dB attenuated at the hardware level.
- Don't switch from Pro Audio to `output:analog-stereo` just because the latter shows `available: no` — that profile requires jack detection to see a connected device, and if jack detection is flaky or the port mapping is wrong, it won't help.
