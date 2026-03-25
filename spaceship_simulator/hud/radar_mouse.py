"""
Mouse interaction for radar targets.
"""

import math


class RadarMouseInteractor:
    """Handles mouse clicks on radar blips and prints navigation guidance."""

    def __init__(self, app, hud, ship):
        self.app = app
        self.hud = hud
        self.ship = ship

        # Screen-space click tolerance in aspect2d units.
        self.click_radius = 0.035

    def setup(self):
        """Register mouse events."""
        self.app.accept("mouse1", self._on_left_click)

    def _on_left_click(self):
        """Handle left mouse click and resolve radar target under cursor."""
        if not self.app.mouseWatcherNode.has_mouse():
            return

        mouse = self.app.mouseWatcherNode.get_mouse()
        get_aspect = getattr(self.app, "getAspectRatio", None)
        if callable(get_aspect):
            aspect_ratio = get_aspect()
        else:
            aspect_ratio = 1.0
        aspect_x = mouse.x * aspect_ratio
        aspect_z = mouse.y

        target = self.hud.pick_radar_target(aspect_x, aspect_z, self.click_radius)
        if target is None:
            return

        entity = target["entity"]
        rel = entity.position - self.ship.position
        distance = rel.length()

        world_bearing = math.degrees(math.atan2(rel.x, -rel.z))
        rel_bearing = self._normalize_angle(world_bearing - self.ship.heading)

        horizontal_hint = self._horizontal_hint(rel_bearing)
        vertical_hint = self._vertical_hint(rel.y)

        description = self._entity_description(entity)
        msg = (
            f"[RADAR] {entity.name}: {description}. "
            f"Distance {distance/1000:.2f} ku. "
            f"Turn {horizontal_hint}. {vertical_hint}."
        )
        self.app.add_comms_message(msg)

    @staticmethod
    def _normalize_angle(deg_value):
        """Normalize angle to [-180, +180]."""
        return ((deg_value + 180.0) % 360.0) - 180.0

    @staticmethod
    def _horizontal_hint(rel_bearing):
        """Return a heading adjustment hint from a relative bearing."""
        if abs(rel_bearing) < 8.0:
            return "straight ahead"
        if rel_bearing > 0:
            return f"right {abs(rel_bearing):.0f} deg"
        return f"left {abs(rel_bearing):.0f} deg"

    @staticmethod
    def _vertical_hint(delta_y):
        """Return vertical movement hint based on Y delta."""
        if abs(delta_y) < 80.0:
            return "Maintain current altitude"
        if delta_y > 0:
            return f"Climb {abs(delta_y):.0f} units"
        return f"Descend {abs(delta_y):.0f} units"

    @staticmethod
    def _entity_description(entity):
        """Build a short entity description for COMMS."""
        etype = getattr(entity, "type", "unknown").lower()
        if etype == "station":
            return "Orbital station and potential docking point"
        if etype == "anomaly":
            return "Unstable anomaly with unusual readings"
        if etype == "planet":
            return "Planetary body of scientific interest"
        return f"{etype.capitalize()} contact"