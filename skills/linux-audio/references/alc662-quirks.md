# Realtek ALC662 rev3 — Known Quirks

## Hardware Layout (Lenovo subsystem 0x17aa36d9)

```
Node 0x14 [Pin Complex] — Line Out at Ext Rear (green jack)
  Amp-Out vals: [0x00 0x00] = unmuted
  Pin Default: 0x01014010
  Pin-ctls: 0x40: OUT

Node 0x1b [Pin Complex] — HP Out at Ext Front (headphone jack)
  Amp-Out vals: [0x80 0x80] = MUTED → [0x00 0x00] = working
  Pin Default: 0x02214020
  Pin-ctls: 0xc0: OUT HP VREF_HIZ

Node 0x15 [Pin Complex] — Speaker at Ext Rear (unused, N/A)
  Amp-Out vals: [0x80 0x80] = MUTED
  Pin Default: 0x411111f0
  Pin-ctls: 0x20: IN
```

## ALSA Mixer Controls

| Control | Function | Working State |
|---------|----------|---------------|
| Master | Main output amp (mono) | 100% [on] |
| Headphone | Front HP amp switch (controls node 0x1b mute bit) | [on] |
| Headphone+LO | Combined HP+LineOut volume | 100% |
| PCM | Digital volume | 99% |
| Front | Front channel enable | [on] |
| Auto-Mute Mode | Mute speakers on HP insert | Disabled |
| Loopback Mixing | Internal loopback | Disabled |

## The Critical Bug

On this codec, the **Headphone switch** controls the amp mute on node 0x1b via the 0x80 mute bit. When Headphone is OFF:

1. `amixer sget Headphone` → `[off]`
2. `/proc/asound/card0/codec#0` → `Amp-Out vals: [0x80 0x80]`
3. No analog audio output — neither front headphone jack nor rear line out works

This is because the ALC662 routes all analog output through node 0x1b's amplifier path. The Headphone switch is misnamed — it's really the "analog output amp enable" switch.

## Fix

```bash
amixer -c0 sset Headphone on    # Unmutes node 0x1b: [0x80 0x80] → [0x00 0x00]
amixer -c0 sset Master 100%     # Full volume at hardware level
```

## Pro Audio Profile Behavior

With `pro-audio` active:
- PCM device hw:0,0 is the only analog path
- hw:0,3/7/8 are HDMI outputs
- No jack detection, no auto-port-switching
- All traditional profiles show `available: no` because no port is detected as physically connected
- PipeWire volumes work but ALSA hardware switches are ignored — the agent must check both layers
