"""
HUD base components for the spaceship simulator.
"""

from panda3d.core import TextNode, Point3
from spaceship_simulator.config.constants import HUD_FONT_SIZE, HUD_COLOR_PRIMARY


class HUDPanel:
    """Base class for HUD panels."""
    
    def __init__(self, app, title: str, x: float, y: float, width: float, height: float):
        self.app = app
        self.title = title
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_objs = []
    
    def add_text(self, label: str, color=HUD_COLOR_PRIMARY, size: int = HUD_FONT_SIZE):
        """Add a text element to the panel."""
        text = self.app.task_mgr.create_text_node(self.title)
        text.set_text(label)
        text.set_text_color(*color, 1.0)
        text.set_font_size(size)
        return text
    
    def update(self):
        """Update panel content."""
        pass
    
    def cleanup(self):
        """Cleanup HUD elements."""
        for text in self.text_objs:
            text.remove_node()
        self.text_objs.clear()


class Radar(HUDPanel):
    """Radar display showing nearby entities."""
    
    def __init__(self, app, ship_state, universe):
        super().__init__(app, "Radar", x=-1.0, y=0.7, width=0.25, height=0.25)
        self.ship = ship_state
        self.universe = universe
        self._build_ui()
    
    def _build_ui(self):
        """Build radar UI elements."""
        # Title
        title_text = self.app.task_mgr.create_text_node("RadarTitle")
        title_text.set_text("RADAR")
        title_text.set_text_color(0, 1, 0, 1)
        title_text.set_font_size(16)
        title_node = self.app.camera.attach_new_node(title_text)
        title_node.set_pos(Point3(self.x + 0.02, 0, self.y - 0.02))
        self.text_objs.append(title_node)
    
    def update(self):
        """Update radar with nearby entities."""
        from spaceship_simulator.config.constants import RADAR_RANGE
        nearby = self.universe.get_nearby_entities(self.ship.position, RADAR_RANGE)
        
        # Show up to 5 closest entities
        for i, entity in enumerate(nearby[:5]):
            dist = (entity.position - self.ship.position).length()
            text = f"{entity.name[:10]} {dist:.0f}u"
            # Update or create text node


class CommsScreen(HUDPanel):
    """Communication alerts and messages."""
    
    def __init__(self, app, ship_state):
        super().__init__(app, "Comms", x=-0.3, y=0.7, width=0.25, height=0.25)
        self.ship = ship_state
        self.messages = []
        self._build_ui()
    
    def _build_ui(self):
        """Build comms UI."""
        title_text = self.app.task_mgr.create_text_node("CommsTitle")
        title_text.set_text("COMMUNICATIONS")
        title_text.set_text_color(0, 0.7, 0.7, 1)
        title_text.set_font_size(16)
        title_node = self.app.camera.attach_new_node(title_text)
        title_node.set_pos(Point3(-0.28, 0, 0.68))
        self.text_objs.append(title_node)
    
    def add_message(self, message: str):
        """Add a message to the queue."""
        self.messages.append(message)
        if len(self.messages) > 5:
            self.messages.pop(0)
    
    def update(self):
        """Update comms display."""
        pass


class StatusPanel(HUDPanel):
    """General ship status display."""
    
    def __init__(self, app, ship_state):
        super().__init__(app, "Status", x=0.65, y=0.7, width=0.3, height=0.25)
        self.ship = ship_state
        self._build_ui()
    
    def _build_ui(self):
        """Build status UI."""
        title_text = self.app.task_mgr.create_text_node("StatusTitle")
        title_text.set_text("STATUS")
        title_text.set_text_color(0, 1, 0, 1)
        title_text.set_font_size(16)
        title_node = self.app.camera.attach_new_node(title_text)
        title_node.set_pos(Point3(0.67, 0, 0.68))
        self.text_objs.append(title_node)
    
    def update(self):
        """Update status display."""
        from spaceship_simulator.config.constants import get_string
        
        status_lines = [
            f"{get_string('energy', 'en')}: {self.ship.energy:.0f}%",
            f"{get_string('shield', 'en')}: {self.ship.shield:.0f}%",
            f"{get_string('hull', 'en')}: {self.ship.hull:.0f}%",
            f"{get_string('oxygen', 'en')}: {self.ship.oxygen:.0f}%",
            f"{get_string('velocity', 'en')}: {self.ship.velocity.length():.0f}u",
        ]
