# Spaceship Simulator

A first-person arcade spaceship exploration and simulation game built with **Panda3D**.

## Overview

You are the captain of a starship navigating a procedurally-generated galaxy. Explore planets, stations, and space anomalies while managing your ship's systems—energy, shields, oxygen, and crew. The game focuses on exploration and survival in an arcade-style environment.

### Features

- **First-person cockpit view** with multiple camera modes (switchable via F1-F4)
- **Full spaceship control system**: thrust, yaw, pitch, roll, strafe
- **Real-time ship systems**: energy, shields, hull integrity, oxygen, atmosphere, cargo, crew status
- **Procedurally-generated galaxy** with 150+ planets, 50+ stations, and anomalies
- **Radar system** showing nearby entities and distances
- **Communication screen** for alerts and discoveries
- **Bilingual UI** (English/Spanish)
- **Modular architecture** for easy expansion and feature addition

---

## Setup

### Prerequisites

- Python 3.9+
- Poetry (Python dependency manager)

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd /home/mauricio/git/recart
   ```

2. **Install dependencies** using Poetry:
   ```bash
   poetry install
   ```

3. **Run the game**:
   ```bash
   poetry run spaceship
   ```

   Or, using Poetry shell:
   ```bash
   poetry shell
   python -m spaceship_simulator.main
   ```

---

## Game Controls

All controls are keyboard-based. The default layout is **arcade-style** using WASD for movement.

| Action | Key | Description |
|--------|-----|-------------|
| **Thrust Forward** | `W` | Increase forward velocity |
| **Reverse** | `S` | Reverse thrust |
| **Yaw Left** | `A` | Rotate left |
| **Yaw Right** | `D` | Rotate right |
| **Pitch Up** | `Q` | Nose up |
| **Pitch Down** | `E` | Nose down |
| **Roll Left** | `Z` | Roll counter-clockwise |
| **Roll Right** | `X` | Roll clockwise |
| **Strafe Up** | `SPACE` | Move up (vertical) |
| **Strafe Down** | `CTRL` | Move down (vertical) |
| **View Mode 1** | `F1` | First-person view |
| **View Mode 2** | `F2` | Top-down view |
| **View Mode 3** | `F3` | Rear view |
| **View Mode 4** | `F4` | Side view |
| **Help** | `H` | Toggle help display |
| **Pause** | `P` | Pause/Resume game |
| **Exit** | `ESC` | Quit game |

---

## Ship Systems

### Energy
- **Current/Max**: Displayed in real-time on status panel
- **Regens**: Automatically over time
- **Used by**: Active sensors and ship systems

### Shields
- **Current/Max**: Defensive energy barrier
- **Regens**: Slowly when not taking damage
- **Status**: Critical when below 25%

### Hull Integrity
- **Current/Max**: Ship structural integrity
- **Damage**: Reduces when shields are compromised
- **Critical**: Below 50%, ship systems may malfunction

### Oxygen
- **Current/Max**: Breathable air for crew
- **Drains**: Rapidly when not in atmosphere
- **Regenerates**: In planetary atmospheres
- **Critical**: Alert when below 25%

### Velocity & Acceleration
- **Max Velocity**: 100 units/second
- **Displayed**: Real-time in status panel
- **Physics**: Arcade-style (quick response)

### Crew Status
- **Health**: Percentage of crew operational
- **Affects**: Ship performance and repairs
- **Critical**: Below 50%, reduced performance

---

## Game Screens (HUD)

### Radar (Top-Left)
- Nearby entities within sensor range
- Distance and entity information
- Updates every 0.5 seconds

### Communication Screen (Top-Center)
- Alerts and notifications
- Discovery logs
- System warnings

### Status Panel (Top-Right)
- Real-time telemetry
- Energy, shield, oxygen levels
- Velocity and crew status

### Space View (Main)
- First-person view of the galaxy
- 4 camera modes selectable with F1-F4
- Enhanced visuals

---

## Gameplay Loop

1. **Explore**: Navigate the galaxy
2. **Discover**: Find planets, stations, anomalies
3. **Monitor**: Track ship systems
4. **Survive**: Manage resources
5. **Navigate**: Use radar for navigation

---

## Project Architecture

```
spaceship_simulator/
├── main.py                # Entry point
├── input_handler.py       # Keyboard input
├── config/
│   └── constants.py       # Game config & strings
├── ship/
│   └── ship.py           # Ship state & physics
├── world/
│   └── universe.py       # Galaxy generation
├── hud/
│   └── panel.py          # HUD panels
└── utils/
    └── math_utils.py     # Helper functions
```

---

## Development

### Running the Game
```bash
poetry run spaceship
```

### Building for Distribution
```bash
poetry build
```

### Install in Development Mode
```bash
poetry install
```

---

## Future Enhancements

- [ ] Combat and weapons system
- [ ] NPCs and trading
- [ ] Planet landing and exploration
- [ ] Enhanced graphics and effects
- [ ] Sound and music
- [ ] Save/load functionality
- [ ] Difficulty levels
- [ ] Multiplayer support
- [ ] VR support

---

## License

See [LICENSE](LICENSE) for details.

---

## Credits

- **Engine**: [Panda3D](https://www.panda3d.org/)
- **Language**: Python 3.9+
- **Package Manager**: [Poetry](https://python-poetry.org/)

---

**Ready to explore the galaxy? 🚀**
