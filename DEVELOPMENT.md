# Development Guide - Spaceship Simulator

## Architecture Overview

The project uses a **modular, component-based architecture** for easy expansion:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SpaceshipSimulator (ShowBase)                 │
│                  (main.py - Main game loop)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  ShipState   │  │   Galaxy     │  │   InputHandler       │   │
│  │  (ship.py)   │  │ (universe.py)│  │ (input_handler.py)   │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              HUD System (hud/panel.py)                     │  │
│  │  ┌─────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐  │  │
│  │  │ Radar   │  │ CommsScr │  │StatusPanel │  │Viewport  │  │  │
│  │  └─────────┘  └──────────┘  └────────────┘  └──────────┘  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│                    Utils (math_utils.py)                         │
│                    Config (constants.py)                         │
└─────────────────────────────────────────────────────────────────┘
```

## Module Reference

### `spaceship_simulator/config/constants.py`
- **Purpose**: All game constants, configuration, and localization strings
- **Usage**: Import `get_string(key, language)` for UI text, use constants for game parameters
- **Extend**: Add new constants here, then reference throughout the codebase

**Example**:
```python
from spaceship_simulator.config.constants import MAX_VELOCITY, get_string

print(get_string("welcome", "en"))  # "SPACESHIP SIMULATOR v0.1"
print(MAX_VELOCITY)  # 100.0
```

### `spaceship_simulator/ship/ship.py`
- **Purpose**: Manages all ship state: position, velocity, rotation, systems (energy, shields, etc.)
- **Main Class**: `ShipState`
- **Key Methods**:
  - `update(dt)`: Called per frame to update physics and systems
  - `_update_energy()`, `_update_oxygen()`, `_update_shields()`: System regeneration
  - `_update_axes()`: Recalculate facing direction based on rotation

**Adding a Ship System** (Example: Fuel):
```python
# In ship.py ShipState.__init__():
self.fuel = 100.0
self.max_fuel = 100.0

# Add update method:
def _update_fuel(self, dt):
    # Fuel consumption logic
    drain = 10.0 * dt  # Per second
    self.fuel = clamp(self.fuel - drain, 0, self.max_fuel)

# Call in update():
self._update_fuel(dt)
```

### `spaceship_simulator/world/universe.py`
- **Purpose**: Procedural galaxy generation and entity management
- **Main Classes**:
  - `Entity`: Represents planets, stations, anomalies
  - `Galaxy`: Manages all entities, spatial queries

**Adding Entities** (Example: Black Holes):
```python
# In Galaxy._generate_entities():
for i in range(10):
    name = f"BlackHole-{i+1}"
    pos = self._random_position()
    black_hole = Entity(name, "blackhole", pos, radius=1000.0)
    self.entities.append(black_hole)
    self._add_to_sector(black_hole)
```

### `spaceship_simulator/input_handler.py`
- **Purpose**: Maps keyboard input to ship commands
- **Main Class**: `InputHandler`
- **Usage**: Accepts keybinds in `setUp()`, updates `ship.thrust_input`, `ship.yaw_input`, etc.

**Adding Controls** (Example: Toggle Shields):
```python
# In setup():
self.app.accept("t", self._toggle_shields)

# Add method:
def _toggle_shields(self):
    if self.ship.shield > 0:
        self.ship.shield = 0
    else:
        self.ship.shield = self.ship.max_shield
```

### `spaceship_simulator/hud/panel.py`
- **Purpose**: HUD panels for displaying game information
- **Main Classes**:
  - `HUDPanel`: Base class for all panels
  - `Radar`, `CommsScreen`, `StatusPanel`: Specific panels

**Creating a New Panel**:
```python
# In hud/panel.py:
class TargetingPanel(HUDPanel):
    def __init__(self, app, ship_state):
        super().__init__(app, "Target", x=0.3, y=-0.8, width=0.3, height=0.15)
        self.ship = ship_state
        self._build_ui()
    
    def _build_ui(self):
        # Create text nodes for display
        pass
    
    def update(self):
        # Update display each frame
        pass

# In main.py:
self.targeting = TargetingPanel(self, self.ship)
self.hud_panels.append(self.targeting)
```

### `spaceship_simulator/utils/math_utils.py`
- **Purpose**: Common math helpers (clamp, distance, lerp, etc.)
- **Usage**: Import needed functions: `from spaceship_simulator.utils.math_utils import clamp`

---

## Common Tasks

### Task: Add a New Weapon Type

1. **Create the weapon class** in `ship/weapons.py`:
```python
class Weapon:
    def __init__(self, name, energy_cost, cooldown, range):
        self.name = name
        self.energy_cost = energy_cost
        self.cooldown_timer = 0
        self.cooldown_max = cooldown
        self.range = range
    
    def can_fire(self):
        return self.cooldown_timer <= 0
    
    def fire(self):
        if self.can_fire():
            self.cooldown_timer = self.cooldown_max
            return True
        return False
    
    def update(self, dt):
        self.cooldown_timer -= dt
```

2. **Add weapons to ShipState** in `ship/ship.py`:
```python
from spaceship_simulator.ship.weapons import Weapon

class ShipState:
    def __init__(self):
        # ... existing code ...
        self.primary_weapon = Weapon("Plasma Cannon", 10, 0.5, 5000)
        self.secondary_weapon = Weapon("Missile", 15, 2.0, 10000)
```

3. **Wire up input** in `input_handler.py`:
```python
self.app.accept("f", self._fire_primary)

def _fire_primary(self):
    if self.ship.primary_weapon.fire():
        self.app.add_comms_message("Weapon fired!")
```

4. **Update HUD** in `hud/panel.py`:
```python
class WeaponPanel(HUDPanel):
    def update(self):
        primary_status = "Ready" if self.ship.primary_weapon.can_fire() else "Cooling"
        # Display status
```

---

### Task: Add a New Ship System Status

1. **Add to ShipState** in `ship/ship.py`:
```python
self.heat_level = 50.0
self.max_heat = 100.0
```

2. **Add to StatusPanel** in `hud/panel.py`:
```python
def _build_ui(self):
    # ... existing code ...
    heat_text = self.app.task_mgr.create_text_node("HeatStatus")
    heat_text.set_text(f"Heat: {self.ship.heat_level:.0f}%")
```

3. **Add logic to ship.update()** in `ship/ship.py`:
```python
def _update_heat(self, dt):
    # Heat rises with weapon use, decays over time
    self.heat_level = clamp(self.heat_level - 10.0 * dt, 0, self.max_heat)

# In update():
self._update_heat(dt)
```

---

### Task: Generate Unique Sectors

The `Galaxy` class generates a single procedural galaxy at game start. To add sector-based travel:

```python
# In world/universe.py:
class Sector:
    def __init__(self, x, y, z, seed):
        self.position = (x, y, z)
        self.entities = self._generate_entities(seed)
    
    def _generate_entities(self, seed):
        # Generate unique entities for this sector
        pass

# In main.py:
current_sector = self.universe.get_sector(x, y, z)
nearby_entities = current_sector.entities
```

---

## Debugging Tips

### Print Ship State
```python
print(f"Pos: {self.ship.position}, Vel: {self.ship.velocity.length():.1f}")
print(f"Energy: {self.ship.energy:.0f}, Shield: {self.ship.shield:.0f}")
```

### Add a Debug Overlay
```python
# In main.py, add to update:
if DEBUG:
    print(f"FPS: {globalClock.get_fps():.0f}, Entities: {len(self.universe.entities)}")
```

### Test a Specific Module
```bash
poetry run python -c "
from spaceship_simulator.world.universe import Galaxy
g = Galaxy(seed=42)
print(f'Generated {len(g.entities)} entities')
for e in g.entities[:3]:
    print(e)
"
```

---

## Performance Optimization

### Entity Culling
For large entity counts, optimize radar/rendering:
```python
# Only process nearby entities
visible = self.universe.get_nearby_entities(self.ship.position, RADAR_RANGE)
for entity in visible:
    # Process only visible entities
```

### Reduce Update Frequency
Some systems don't need per-frame updates:
```python
# In main.py:
self.radar_update_timer = 0
if self.radar_update_timer <= 0:
    self._update_radar()
    self.radar_update_timer = 0.5  # Update every 0.5 seconds
else:
    self.radar_update_timer -= dt
```

---

## Testing

### Unit Test Example (Optional)
```python
# tests/test_ship.py
from spaceship_simulator.ship.ship import ShipState

def test_ship_velocity():
    ship = ShipState()
    ship.thrust_input = 1.0
    ship.update(0.1)
    assert ship.velocity.length() > 0
```

Run with:
```bash
poetry add --group dev pytest
poetry run pytest tests/
```

---

## Next Steps

1. **Run the game**: `poetry run spaceship`
2. **Test controls**: Try WASD, QE, ZX, and F1-F4
3. **Explore**: Check out the radar and communications panels
4. **Expand**: Add weapons, NPCs, or new systems using the patterns above

---

## Resources

- **Panda3D Docs**: https://docs.panda3d.org/1.10/python/
- **Python 3.9+**: https://www.python.org/
- **Poetry**: https://python-poetry.org/docs/

---

**Happy hacking! 🚀**
