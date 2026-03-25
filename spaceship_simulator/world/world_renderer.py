"""
3D rendering for world entities.
"""

from panda3d.core import Vec4


class WorldRenderer:
    """Renders nearby entities (planets, stations, anomalies) in the 3D world."""

    def __init__(self, app, universe, ship):
        self.app = app
        self.universe = universe
        self.ship = ship

        self.root = self.app.render.attach_new_node("WorldEntities")
        self.render_distance = 14000.0
        self.max_visible = 60

        # Entity -> NodePath
        self.nodes = {}
        self._create_nodes()

    def _create_nodes(self):
        """Create one visual node per entity and keep it hidden until nearby."""
        for entity in self.universe.entities:
            model = self._load_model_for_type(getattr(entity, "type", "planet"))
            node = self.root.attach_new_node(entity.name)
            model.reparent_to(node)
            node.set_pos(entity.position)
            node.set_scale(self._visual_scale(entity))
            node.set_color_scale(*self._color_for_type(getattr(entity, "type", "planet")))
            node.hide()
            self.nodes[entity] = node

    def _load_model_for_type(self, entity_type):
        """Load a simple model by type using Panda's built-in assets."""
        et = str(entity_type).lower()
        if et == "station":
            return self.app.loader.load_model("models/misc/rgbCube")
        return self.app.loader.load_model("models/misc/sphere")

    def _visual_scale(self, entity):
        """Map simulation radius to readable visual size."""
        et = getattr(entity, "type", "planet").lower()
        if et == "station":
            return 45.0
        if et == "anomaly":
            return 30.0
        return max(40.0, min(130.0, entity.radius * 0.035))

    def _color_for_type(self, entity_type):
        """RGBA color by entity type."""
        et = str(entity_type).lower()
        if et == "station":
            return Vec4(1.0, 0.72, 0.2, 1.0)
        if et == "anomaly":
            return Vec4(1.0, 0.28, 0.28, 1.0)
        return Vec4(0.35, 0.62, 1.0, 1.0)

    def update(self, dt):
        """Show nearby entities and hide distant ones."""
        del dt  # Reserved for future animation.

        nearby = self.universe.get_nearby_entities(self.ship.position, self.render_distance)
        visible = set(nearby[:self.max_visible])

        for entity, node in self.nodes.items():
            if entity in visible:
                node.set_pos(entity.position)
                node.show()
            else:
                node.hide()
