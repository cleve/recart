"""
Game constants, configuration, and language strings.
"""

# ============================================================================
# LANGUAGE STRINGS (English/Spanish)
# ============================================================================

STRINGS = {
    "en": {
        # Main HUD labels
        "radar": "RADAR",
        "comms": "COMMUNICATIONS",
        "status": "STATUS",
        "weapons": "WEAPONS",
        "viewport": "SPACE VIEW",
        
        # Status labels
        "energy": "Energy",
        "shield": "Shield",
        "hull": "Hull",
        "oxygen": "Oxygen",
        "atmosphere": "Atmosphere",
        "velocity": "Velocity",
        "acceleration": "Acceleration",
        "cargo": "Cargo",
        "crew": "Crew",
        
        # Units
        "units": "u",
        "percent": "%",
        
        # Messages
        "welcome": "SPACESHIP SIMULATOR v0.1",
        "press_f1_help": "[F1] Help",
        "distance": "Distance",
        "unknown": "UNKNOWN",
        "no_targets": "No targets detected",
        "no_messages": "No messages",
        
        # Controls help
        "controls": "CONTROLS",
        "control_panel": "TOUCH CONTROL",
        "control_panel_status": "Touch grid online",
        "landing": "Landing",
        "retro_propulsors": "Retro-propulsors",
        "deploy_solar_panels": "Deploy solar panels",
        "free_trash": "Free trash",
        "emergency_stop": "Emergency stop",
        "thrust": "W/S - Thrust",
        "yaw": "A/D - Yaw",
        "pitch": "Q/E - Pitch",
        "roll": "Z/X - Roll",
        "strafe": "Space/Ctrl - Vertical strafe",
        "view_modes": "F1-F4 - View modes",
        "help": "H - Help toggle",
        "pause": "P - Pause",
        "exit": "ESC - Exit",
    },
    "es": {
        # Main HUD labels
        "radar": "RADAR",
        "comms": "COMUNICACIONES",
        "status": "ESTADO",
        "weapons": "ARMAS",
        "viewport": "VISTA ESPACIAL",
        
        # Status labels
        "energy": "Energía",
        "shield": "Escudo",
        "hull": "Casco",
        "oxygen": "Oxígeno",
        "atmosphere": "Atmósfera",
        "velocity": "Velocidad",
        "acceleration": "Aceleración",
        "cargo": "Carga",
        "crew": "Tripulación",
        
        # Units
        "units": "u",
        "percent": "%",
        
        # Messages
        "welcome": "SIMULADOR DE NAVE ESPACIAL v0.1",
        "press_f1_help": "[F1] Ayuda",
        "distance": "Distancia",
        "unknown": "DESCONOCIDO",
        "no_targets": "Sin objetivos detectados",
        "no_messages": "Sin mensajes",
        
        # Controls help
        "controls": "CONTROLES",
        "control_panel": "CONTROL TACTIL",
        "control_panel_status": "Panel tactil en linea",
        "landing": "Aterrizaje",
        "retro_propulsors": "Retropropulsores",
        "deploy_solar_panels": "Desplegar paneles solares",
        "free_trash": "Liberar basura",
        "emergency_stop": "Parada de emergencia",
        "thrust": "W/S - Empuje",
        "yaw": "A/D - Guiñada",
        "pitch": "Q/E - Cabeceo",
        "roll": "Z/X - Alabeo",
        "strafe": "Espacio/Ctrl - Desplazamiento vertical",
        "view_modes": "F1-F4 - Modos de vista",
        "help": "H - Mostrar/ocultar ayuda",
        "pause": "P - Pausa",
        "exit": "ESC - Salir",
    }
}

# ============================================================================
# GAME PARAMETERS
# ============================================================================

# Window
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Spaceship Simulator"

# Physics — tuned for a massive capital ship (heavy, sluggish feel)
MAX_VELOCITY = 200.0          # top linear speed (reduced for heavy ship)
MAX_ACCELERATION = 100.0
ACCELERATION_RATE = 0.02      # slow to spool up (exponential decay factor)
DECELERATION_RATE = 0.025     # slow to bleed off speed
ROTATION_SPEED = 0.5          # degrees/frame; massive ships turn slowly
STRAFE_SPEED = 40.0           # up/down thruster speed (units/s)

# Ship Systems
INITIAL_ENERGY = 100.0
MAX_ENERGY = 100.0
ENERGY_REGEN_RATE = 5.0  # per second
INITIAL_SHIELD = 80.0
MAX_SHIELD = 100.0
SHIELD_REGEN_RATE = 3.0  # per second
INITIAL_OXYGEN = 100.0
MAX_OXYGEN = 100.0
OXYGEN_DRAIN_RATE = 2.0  # per second (when not in atmosphere)

# Radar
RADAR_RANGE = 50000.0  # Distance units
RADAR_UPDATE_RATE = 0.5  # seconds

# Universe
GALAXY_SIZE = 100000.0  # Size of the galaxy
INITIAL_SECTOR = (50, 50, 50)  # Starting position
SECTOR_SIZE = 1000.0  # Size of each sector
NUM_PLANETS = 150
NUM_STATIONS = 50
NUM_ANOMALIES = 30

# HUD
HUD_FONT_SIZE = 20
HUD_COLOR_PRIMARY = (0.0, 1.0, 0.0)  # Green
HUD_COLOR_SECONDARY = (0.0, 0.7, 0.7)  # Cyan
HUD_COLOR_WARNING = (1.0, 0.5, 0.0)  # Orange
HUD_COLOR_DANGER = (1.0, 0.0, 0.0)  # Red
HUD_OPACITY = 0.8


def get_string(key: str, language: str = "en") -> str:
    """Get a localized string."""
    lang_dict = STRINGS.get(language, STRINGS["en"])
    return lang_dict.get(key, f"[{key}]")
