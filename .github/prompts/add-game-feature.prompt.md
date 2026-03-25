---
description: "Add a new game feature to the spaceship simulator following project conventions and architecture"
argument-hint: "Describe the feature: what it does, which systems it touches, and any special requirements"
agent: "agent"
---

Add a new feature to the spaceship simulator. The project uses a **modular, component-based architecture** with Panda3D. Before implementing, read the relevant source files to understand existing patterns.

## Architecture Map

| Concern | File |
|---------|------|
| Main game loop / task scheduling | [spaceship_simulator/main.py](../../spaceship_simulator/main.py) |
| Ship state & physics | [spaceship_simulator/ship/ship.py](../../spaceship_simulator/ship/ship.py) |
| Galaxy / world entities | [spaceship_simulator/world/universe.py](../../spaceship_simulator/world/universe.py) |
| World rendering | [spaceship_simulator/world/world_renderer.py](../../spaceship_simulator/world/world_renderer.py) |
| HUD panels | [spaceship_simulator/hud/panel.py](../../spaceship_simulator/hud/panel.py) |
| Full HUD | [spaceship_simulator/hud/realistic_hud.py](../../spaceship_simulator/hud/realistic_hud.py) |
| Input bindings | [spaceship_simulator/input_handler.py](../../spaceship_simulator/input_handler.py) |
| Constants & strings | [spaceship_simulator/config/constants.py](../../spaceship_simulator/config/constants.py) |
| Math helpers | [spaceship_simulator/utils/math_utils.py](../../spaceship_simulator/utils/math_utils.py) |

## Implementation Checklist

- [ ] Identify which modules are affected and read them before writing code.
- [ ] Keep new logic in the appropriate module (don't add ship physics to HUD code, etc.).
- [ ] Register any per-frame logic as a Panda3D task via `self.task_mgr.add(...)`.
- [ ] Add new key bindings in `InputHandler` if the feature requires player input.
- [ ] Add EN **and** ES strings to `constants.py` for any new UI text.
- [ ] Add new tunable values as named constants in `constants.py`, not as magic numbers.
- [ ] Do not over-engineer: implement only what is needed for the described feature.

## Task

$ARGUMENTS

Explore the relevant files, then implement the feature. Show all changes across every affected file.
