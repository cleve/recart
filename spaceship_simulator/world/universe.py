"""
Universe and world generation.
"""

from panda3d.core import Vec3
import random
import math


class Entity:
    """A space entity (planet, station, anomaly)."""
    
    def __init__(self, name: str, entity_type: str, position: Vec3, radius: float):
        self.name = name
        self.type = entity_type  # "planet", "station", "anomaly", "asteroid"
        self.position = position
        self.radius = radius
        self.discovered = False
        self.scanned = False
    
    def __repr__(self):
        return f"{self.name} ({self.type}) @ {self.position}"


class Galaxy:
    """Procedural galaxy with sectors and entities."""
    
    def __init__(self, galaxy_size: float = 100000.0, seed: int = None):
        self.galaxy_size = galaxy_size
        self.entities = []
        self.sectors = {}  # (x, y, z) -> list of entities
        
        if seed is not None:
            random.seed(seed)
        
        self._generate_entities()
    
    def _generate_entities(self):
        """Generate planets, stations, and anomalies across the galaxy."""
        # --- Starter cluster near spawn (50, 50, 50) ---
        # Guarantees radar blips are visible right from the start.
        # Entities are within 5000 units of the origin, inside display_range=5000.
        starter = [
            ("Planet-Alpha",  "planet",  Vec3( 800,  50,  -600), 2000.0),
            ("Station-Alpha", "station", Vec3(-1200, 50,  1000),  500.0),
            ("Anomaly-Alpha", "anomaly", Vec3( 300,  50,  2800), 1500.0),
            ("Planet-Beta",   "planet",  Vec3(-3000, 50, -1500), 3000.0),
            ("Station-Beta",  "station", Vec3( 2500, 50,  2000),  500.0),
        ]
        for name, etype, pos, radius in starter:
            e = Entity(name, etype, pos, radius)
            self.entities.append(e)
            self._add_to_sector(e)

        # Generate planets
        for i in range(150):
            name = f"Planet-{i+1}"
            pos = self._random_position()
            planet = Entity(name, "planet", pos, radius=float(random.randint(1000, 5000)))
            self.entities.append(planet)
            self._add_to_sector(planet)
        
        # Generate stations
        for i in range(50):
            name = f"Station-{i+1}"
            pos = self._random_position()
            station = Entity(name, "station", pos, radius=500.0)
            self.entities.append(station)
            self._add_to_sector(station)
        
        # Generate anomalies
        for i in range(30):
            name = f"Anomaly-{i+1}"
            pos = self._random_position()
            anomaly = Entity(name, "anomaly", pos, radius=2000.0)
            self.entities.append(anomaly)
            self._add_to_sector(anomaly)
    
    def _random_position(self) -> Vec3:
        """Generate a random position in the galaxy."""
        half_size = self.galaxy_size / 2
        return Vec3(
            random.uniform(-half_size, half_size),
            random.uniform(-half_size/3, half_size/3),  # Flatter in Y (galactic plane)
            random.uniform(-half_size, half_size)
        )
    
    def _add_to_sector(self, entity: Entity):
        """Add entity to its sector."""
        sector = self._get_sector_key(entity.position)
        if sector not in self.sectors:
            self.sectors[sector] = []
        self.sectors[sector].append(entity)
    
    def _get_sector_key(self, position: Vec3, sector_size: float = 1000.0):
        """Get sector key for a position."""
        sx = int(position.x // sector_size) * sector_size
        sy = int(position.y // sector_size) * sector_size
        sz = int(position.z // sector_size) * sector_size
        return (sx, sy, sz)
    
    def get_nearby_entities(self, center: Vec3, radius: float) -> list:
        """Get entities near a position."""
        nearby = []
        for entity in self.entities:
            dist = (entity.position - center).length()
            if dist < radius:
                nearby.append(entity)
        return sorted(nearby, key=lambda e: (e.position - center).length())
    
    def get_closest_entity(self, center: Vec3) -> Entity:
        """Get the closest entity to a position."""
        entities = self.get_nearby_entities(center, self.galaxy_size)
        return entities[0] if entities else None
