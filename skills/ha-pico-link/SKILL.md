---
name: ha-pico-link
triggers: ["Lutron Pico", "Caséta", "Pico remote", "pico-link", "Pico Link", "Lutron Caséta Pico remote", "Pico button", "Pico configuration", "Pico Link setup"]
description: "Use when the user wants to set up a Lutron Caséta Pico remote in Home Assistant via pico-link. Branches: user mentions \"pico-link\" or \"Pico Link\", says \"set up a Pico remote\", or wants to map Pico buttons to HA entities (lights, fans, covers, media players, switches). Covers HACS installation, device configuration by type (P2B, 2B, 3BRL, 4B), domain-specific behavior, and timing calibration. Does NOT cover the built-in lutron_caseta device trigger approach — use ha-lighting-automation for that."
metadata:
  version: 1
  source: pico-link (smartqasa/pico-link)
---

# Pico Link — Universal Pico-to-HA Controller

[Pico Link](https://github.com/smartqasa/pico-link) is a **Pico-only** custom integration that listens to `lutron_caseta_button_event` and maps button presses to **domain-aware** HA actions with tap/hold distinction, step/ramp patterns, and deterministic STOP semantics. One domain per device (except 4B Picos — those use scene buttons instead). The Pico Link integration must already be installed and configured in HA before this skill applies.

## Leading words

- **Pico** — any Lutron Caséta wireless remote, distinguished by type (P2B, 2B, 3BRL, 4B). The same word describes both the hardware and the running configuration.
- **domain-aware** — the integration reads the controlled domain (lights, fans, covers, media players, switches) and adjusts each button's effect to match. One Pico type, five possible personalities.

## Step 1 — Install pico-link

Pick one path:

- **HACS**: HACS → Integrations → ⋮ → Custom Repositories → add `https://github.com/smartqasa/pico-link` (type: Integration) → Install → Restart HA.
- **Manual**: copy the `custom_components/pico_link/` directory into `config/custom_components/` → Restart HA.

**Completion criterion**: the integration appears in HA Settings → Devices & Services after restart, and (after Step 2) `lutron_caseta_button_event` events produce logged actions.

## Step 2 — Configure devices in configuration.yaml

### Structure

```yaml
pico_link:
  defaults:   # optional — global overrides
  devices:    # required — one entry per Pico
```

Each **device entry** must define `type`, identify the Pico (`name` or `device_id`), and pick **exactly one domain** (except 4B). See the Pico type table below.

### Pico types

| Type | Layout | Buttons | Hold? | Domain logic? | Use |
|------|--------|---------|-------|---------------|-----|
| **P2B** | Paddle | `on`, `off` | yes | yes | Lights, fans, covers, media |
| **2B** | On/Off | `on`, `off` | yes | yes | Lights, fans, covers, media |
| **3BRL** | On/Raise/Stop/Lower/Off | `on`, `raise`, `stop`, `lower`, `off` | yes | yes | Full device control |
| **4B** | 4 scenes | `button_1`–`button_3`, `off` | no | no (uses `buttons:` map) | Scenes, scripts, any action |

**Completion criterion**: every Pico in the house has exactly one `pico_link` device entry.

### Config parameters — all devices

| Param | Required | Default | Note |
|-------|----------|---------|------|
| `type` | yes | — | One of `P2B`, `2B`, `3BRL`, `4B` |
| `name` | see note | — | Pico's HA device name OR `device_id` (one required) |
| `device_id` | see note | — | Direct device registry ID |
| Domain key | yes (not 4B) | — | One of: `lights:`, `fans:`, `covers:`, `media_players:`, `switches:` |
| `buttons:` | 4B only | `{}` | Scene/action mapping |
| `middle_button` | 3BRL only | domain default | Custom STOP behavior |
| `light_on_pct` | no | `100` | ON brightness |
| `light_low_pct` | no | `5` | Minimum dim |
| `light_step_pct` | no | `10` | Dim step size |
| `light_transition_on` | no | `0` | Fade-in seconds |
| `light_transition_off` | no | `0` | Fade-out seconds |
| `fan_on_pct` | no | `100` | ON speed |
| `cover_open_pos` | no | `100` | ON open position |
| `cover_step_pct` | no | `10` | Cover step % |
| `cover_inverted` | no | `false` | Reverses Open/Close |
| `media_player_vol_step` | no | `10` | Volume step % |

And the optional top-level `defaults:` block, which holds global overrides:

| `defaults` sub-param | Default | Note |
|------|---------|------|
| `hold_time_ms` | `400` | Tap↔Hold threshold (safe range: 300–500) |
| `step_time_ms` | `650` | Ramp repeat interval (safe range: 600–1000) |
| `middle_button` | domain default | Global STOP override (see STOP section) |

Full parameter details disclosed in [`PARAMETERS.md`](PARAMETERS.md).

**Completion criterion**: every required field filled for each Pico, and no configured Pico has more than one domain.

## Step 3 — Validate

1. **Restart HA** — `config.check` alone does not load custom integrations
2. **Press each button** on every configured Pico
3. **Check each domain**: lights dim/step/ramp, fans speed up/down/reverse, covers open/close/stop, media players play/next/vol/mute, switches toggle
4. **Check the STOP button** (3BRL) behaves as expected per the domain table below

**Completion criterion**: every button press produces the expected HA action with no unhandled events in the logs.

## Domain behavior reference

Every action is **domain-aware** — the same physical Pico button does different things depending on what it controls.

### Lights

| Button | Action |
|--------|--------|
| ON | `turn_on` → `light_on_pct` brightness |
| OFF | `turn_off` (with transition if set) |
| RAISE | step up (`light_step_pct`) or ramp |
| LOWER | step down or ramp |
| STOP | no-op |

### Fans

| Button | Action |
|--------|--------|
| ON | `set_percentage` → `fan_on_pct` |
| OFF | `turn_off` |
| RAISE | speed step up |
| LOWER | speed step down |
| STOP | `reverse_direction` |

### Covers

| Button | Action |
|--------|--------|
| ON | `open_cover` → `cover_open_pos` |
| OFF | `close_cover` |
| RAISE | step open or ramp open |
| LOWER | step close or ramp close |
| STOP | `stop_cover` |

### Media Players

| Button | Action |
|--------|--------|
| ON | `media_play` (or `media_play_pause`) |
| OFF | `media_next_track` |
| RAISE | `volume_up` |
| LOWER | `volume_down` |
| STOP | `volume_mute` (toggle) |

### Switches

| Button | Action |
|--------|--------|
| ON | `turn_on` |
| OFF | `turn_off` |
| Others | no-op |

## Timing — tap vs hold, step vs ramp

Pico Link distinguishes **tap** (brief press) from **hold** (long press) and **step** (single action on tap) from **ramp** (repeated actions while held).

### Defaults

| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| `hold_time_ms` | `400` | 300–500 | Press longer = hold |
| `step_time_ms` | `650` | 600–1000 | Repeat interval while held |

**Do not override unless you observe a problem.** Too-short `hold_time_ms` fires holds on slow taps; too-long misses quick holds. Override at `defaults:` level to apply globally, or per-device.

## STOP button resolution (3BRL only)

The STOP action resolves in this order:

1. Device-level `middle_button:` (per-device override)
2. Global default `middle_button` (under `defaults:`)
3. Domain default (from table below)

### Domain defaults

| Domain | STOP behavior |
|--------|---------------|
| Covers | `stop_cover` |
| Fans | `reverse_direction` |
| Lights | no-op |
| Media Players | `volume_mute` (toggle) |
| Switches | no-op |

### Custom STOP actions

Override `middle_button:` with a YAML action list. Each action can reference assigned entities via **placeholders**:

```yaml
middle_button:
  - action: light.turn_on
    target:
      entity_id:
        - lights          # expands to all lights assigned to this Pico
        - light.accent_lamp
    data:
      brightness_pct: 80
```

### Placeholder expansion

| Placeholder | Expands to |
|-------------|-----------|
| `covers` | All covers assigned to this Pico |
| `fans` | All fans assigned to this Pico |
| `lights` | All lights assigned to this Pico |
| `media_players` | All media players assigned to this Pico |
| `switches` | All switches assigned to this Pico |

## 4B Pico — scene buttons

4-button Picos have no domain — instead use `buttons:`:

```yaml
- name: Scene Pico
  type: 4B
  buttons:
    button_1:
      - action: scene.turn_on
        target:
          entity_id: scene.movie_mode
    button_2:
      - action: script.dim_living_room
    button_3:
      - action: light.turn_off
        target:
          entity_id:
            - light.kitchen
            - light.living_room
    off:
      - action: homeassistant.turn_off
        target:
          area_id: main_floor
```

## Sample — full configuration

```yaml
pico_link:
  defaults:
    hold_time_ms: 400
    step_time_ms: 650

  devices:
    - name: Kitchen Paddle
      type: P2B
      lights:
        - light.kitchen_main
      light_transition_on: 1
      light_transition_off: 3

    - name: Living Room Fan
      type: 3BRL
      fans:
        - fan.living_room
      fan_on_pct: 40

    - name: Shade Remote
      type: 3BRL
      covers:
        - cover.living_room_shade

    - name: Office Media
      type: 3BRL
      media_players:
        - media_player.office_sonos
      media_player_vol_step: 5

    - name: Scene Pico
      type: 4B
      buttons:
        button_1:
          - action: scene.turn_on
            target:
              entity_id: scene.movie
