---
description: "Add a new world entity (planet, station, or anomaly) to the spaceship simulator galaxy"
argument-hint: "Describe the new entity: type, name, position, radius, and any special properties"
agent: "agent"
---

Add a new world entity to the spaceship simulator following the existing patterns in [spaceship_simulator/world/universe.py](../../spaceship_simulator/world/universe.py).

## Requirements

1. **Entity class** — Use or extend the `Entity` class in `universe.py`. If the new entity needs unique behavior, subclass `Entity`.
2. **Galaxy generation** — Register the entity in `Galaxy._generate_entities()`. Add it to the starter cluster if it should be visible on spawn, otherwise add it to the procedural generation loop.
3. **Sector indexing** — Call `self._add_to_sector(entity)` after appending to `self.entities`.
4. **Language strings** — Add display name strings in both `"en"` and `"es"` keys in [spaceship_simulator/config/constants.py](../../spaceship_simulator/config/constants.py) if new UI labels are needed.
5. **Radar** — Verify the entity type string is handled in the radar/HUD rendering logic if a new type is introduced.

## Conventions

- Entity `type` string must be lowercase: `"planet"`, `"station"`, `"anomaly"`, `"asteroid"`, or a new slug.
- Position is a `Vec3` imported from `panda3d.core`.
- Radius is a `float` in world units.
- Follow the existing `(name, etype, pos, radius)` tuple pattern for the starter cluster.

## Task

$ARGUMENTS

Implement the entity following the conventions above. Show all changes across the relevant files.
