---
description: "Add a new HUD panel to the spaceship simulator cockpit UI with bilingual (EN/ES) support"
argument-hint: "Describe the new HUD panel: name, purpose, position on screen, and what ship data it displays"
agent: "agent"
---

Add a new HUD panel to the spaceship simulator following the architecture in [spaceship_simulator/hud/panel.py](../../spaceship_simulator/hud/panel.py) and the realistic HUD in [spaceship_simulator/hud/realistic_hud.py](../../spaceship_simulator/hud/realistic_hud.py).

## Requirements

1. **Subclass `HUDPanel`** — Create a new class in `spaceship_simulator/hud/panel.py` that extends `HUDPanel`.
2. **Implement `_build_ui()`** — Set up all `TextNode` / `DirectFrame` elements. Append every node to `self.text_objs` so `cleanup()` works automatically.
3. **Implement `update()`** — Pull data from `self.ship` (a `ShipState`) and refresh displayed text each frame.
4. **Language strings** — Add all user-visible labels to **both** `"en"` and `"es"` dictionaries in [spaceship_simulator/config/constants.py](../../spaceship_simulator/config/constants.py). Use `get_string(key, language)` in the HUD code.
5. **Register in main HUD** — Instantiate the new panel in `RealisticHUD` (or the appropriate parent), call its `update()` inside the frame task, and call `cleanup()` on teardown.

## Conventions

- Screen coordinates: x in `[-1.33, 1.33]`, y (height) in `[-1.0, 1.0]` (Panda3D aspect2d space).
- Colors: use `HUD_COLOR_PRIMARY` from `constants.py` for consistency.
- Font size: use `HUD_FONT_SIZE` constant as the default.
- Keep panel logic self-contained; do not import from other HUD files unless necessary.

## Task

$ARGUMENTS

Implement the panel following the conventions above. Show all changed files in full.
