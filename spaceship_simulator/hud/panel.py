"""
HUD base components for the spaceship simulator.
"""

from panda3d.core import CardMaker, Point3, TextNode, TransparencyAttrib
from spaceship_simulator.config.constants import (
    HUD_COLOR_PRIMARY,
    HUD_COLOR_SECONDARY,
    HUD_COLOR_WARNING,
    HUD_FONT_SIZE,
    get_string,
)


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


class TouchControlPanel(HUDPanel):
    """Touch-style action panel shown on the right side of the cockpit HUD."""

    BUTTON_KEYS = [
        "landing",
        "retro_propulsors",
        "deploy_solar_panels",
        "free_trash",
        "emergency_stop",
    ]

    def __init__(self, app, ship_state):
        super().__init__(app, "TouchControl", x=0.88, y=0.16, width=0.52, height=0.50)
        self.ship = ship_state
        self.language = getattr(app, "language", "en")
        self.button_nodes = {}
        self.button_labels = {}
        self.status_text = None
        self._build_ui()

    def _make_card(self, name: str, left: float, right: float, bottom: float, top: float, color, alpha: float):
        cm = CardMaker(name)
        cm.set_frame(left, right, bottom, top)
        node = self.app.aspect2d.attach_new_node(cm.generate())
        node.set_transparency(TransparencyAttrib.M_alpha)
        node.set_color(color[0], color[1], color[2], alpha)
        self.text_objs.append(node)
        return node

    def _make_label(self, name: str, text: str, x: float, y: float, scale: float, color):
        text_node = TextNode(name)
        text_node.set_text(text)
        text_node.set_text_color(color[0], color[1], color[2], 1.0)
        text_node.set_align(TextNode.A_center)
        node = self.app.aspect2d.attach_new_node(text_node)
        node.set_pos(x, 0, y)
        node.set_scale(scale)
        self.text_objs.append(node)
        return text_node, node

    def _build_ui(self):
        panel_bg = self._make_card(
            "TouchControlPanelBg",
            self.x,
            self.x + self.width,
            self.y - self.height,
            self.y,
            HUD_COLOR_SECONDARY,
            0.14,
        )
        panel_bg.set_bin("fixed", 2)

        title_text, title_node = self._make_label(
            "TouchControlTitle",
            get_string("control_panel", self.language),
            self.x + self.width * 0.5,
            self.y - 0.05,
            0.032,
            HUD_COLOR_SECONDARY,
        )
        title_node.set_bin("fixed", 12)
        self.button_labels["title"] = title_text

        self.status_text, status_node = self._make_label(
            "TouchControlStatus",
            get_string("control_panel_status", self.language),
            self.x + self.width * 0.5,
            self.y - 0.10,
            0.020,
            HUD_COLOR_PRIMARY,
        )
        status_node.set_bin("fixed", 12)

        left = self.x + 0.04
        right = self.x + self.width - 0.04
        button_height = 0.065
        gap = 0.018
        start_top = self.y - 0.16

        for index, key in enumerate(self.BUTTON_KEYS):
            top = start_top - index * (button_height + gap)
            bottom = top - button_height
            color = HUD_COLOR_WARNING if key == "emergency_stop" else HUD_COLOR_SECONDARY
            alpha = 0.28 if key == "emergency_stop" else 0.18

            button = self._make_card(f"TouchButton{index}", left, right, bottom, top, color, alpha)
            button.set_bin("fixed", 4)
            self.button_nodes[key] = button

            label_text, label_node = self._make_label(
                f"TouchButtonLabel{index}",
                get_string(key, self.language),
                (left + right) * 0.5,
                bottom + button_height * 0.33,
                0.024,
                HUD_COLOR_WARNING if key == "emergency_stop" else HUD_COLOR_PRIMARY,
            )
            label_node.set_bin("fixed", 12)
            self.button_labels[key] = label_text

    def update(self):
        """Refresh labels and visual emphasis based on ship state."""
        self.language = getattr(self.app, "language", "en")
        self.button_labels["title"].set_text(get_string("control_panel", self.language))
        self.status_text.set_text(get_string("control_panel_status", self.language))

        for key in self.BUTTON_KEYS:
            self.button_labels[key].set_text(get_string(key, self.language))

        moving_fast = self.ship.velocity.length() > 120.0
        for key, node in self.button_nodes.items():
            if key == "emergency_stop":
                if moving_fast:
                    node.set_color(1.0, 0.2, 0.2, 0.34)
                else:
                    node.set_color(HUD_COLOR_WARNING[0], HUD_COLOR_WARNING[1], HUD_COLOR_WARNING[2], 0.24)
            else:
                node.set_color(HUD_COLOR_SECONDARY[0], HUD_COLOR_SECONDARY[1], HUD_COLOR_SECONDARY[2], 0.18)
