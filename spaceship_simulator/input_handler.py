"""
HUD input handler for spaceship simulator.
"""

from panda3d.core import KeyboardButton


class InputHandler:
    """Manages keyboard input and maps to ship commands."""
    
    def __init__(self, ship_state, game_app):
        self.ship = ship_state
        self.app = game_app
        
        # Key states
        self.keys_pressed = set()
    
    def setup(self):
        """Setup input event handlers."""
        # Watch for keyboard events
        self.app.accept("w", self._on_w_down)
        self.app.accept("w-up", self._on_w_up)
        self.app.accept("s", self._on_s_down)
        self.app.accept("s-up", self._on_s_up)
        
        self.app.accept("a", self._on_a_down)
        self.app.accept("a-up", self._on_a_up)
        self.app.accept("d", self._on_d_down)
        self.app.accept("d-up", self._on_d_up)
        
        self.app.accept("q", self._on_q_down)
        self.app.accept("q-up", self._on_q_up)
        self.app.accept("e", self._on_e_down)
        self.app.accept("e-up", self._on_e_up)
        
        self.app.accept("z", self._on_z_down)
        self.app.accept("z-up", self._on_z_up)
        self.app.accept("x", self._on_x_down)
        self.app.accept("x-up", self._on_x_up)
        
        self.app.accept("space", self._on_space_down)
        self.app.accept("space-up", self._on_space_up)
        self.app.accept("control", self._on_control_down)
        self.app.accept("control-up", self._on_control_up)
        
        # View modes
        self.app.accept("f1", self.app.set_view_mode, [0])
        self.app.accept("f2", self.app.set_view_mode, [1])
        self.app.accept("f3", self.app.set_view_mode, [2])
        self.app.accept("f4", self.app.set_view_mode, [3])
        
        # Help
        self.app.accept("h", self.app.toggle_help)
        
        # Pause
        self.app.accept("p", self.app.toggle_pause)
        
        # Exit
        self.app.accept("escape", self.app.userExit)
    
    def update(self):
        """Update ship input based on key states."""
        self.ship.thrust_input = 0.0
        self.ship.yaw_input = 0.0
        self.ship.pitch_input = 0.0
        self.ship.roll_input = 0.0
        self.ship.strafe_input = 0.0
        
        if "w" in self.keys_pressed:
            self.ship.thrust_input = 1.0
        if "s" in self.keys_pressed:
            self.ship.thrust_input = -1.0
        
        if "a" in self.keys_pressed:
            self.ship.yaw_input = 1.0
        if "d" in self.keys_pressed:
            self.ship.yaw_input = -1.0
        
        if "q" in self.keys_pressed:
            self.ship.pitch_input = -1.0
        if "e" in self.keys_pressed:
            self.ship.pitch_input = 1.0
        
        if "z" in self.keys_pressed:
            self.ship.roll_input = -1.0
        if "x" in self.keys_pressed:
            self.ship.roll_input = 1.0
        
        if "space" in self.keys_pressed:
            self.ship.strafe_input = 1.0
        if "control" in self.keys_pressed:
            self.ship.strafe_input = -1.0
    
    def _on_w_down(self):
        self.keys_pressed.add("w")
    
    def _on_w_up(self):
        self.keys_pressed.discard("w")
    
    def _on_s_down(self):
        self.keys_pressed.add("s")
    
    def _on_s_up(self):
        self.keys_pressed.discard("s")
    
    def _on_a_down(self):
        self.keys_pressed.add("a")
    
    def _on_a_up(self):
        self.keys_pressed.discard("a")
    
    def _on_d_down(self):
        self.keys_pressed.add("d")
    
    def _on_d_up(self):
        self.keys_pressed.discard("d")
    
    def _on_q_down(self):
        self.keys_pressed.add("q")
    
    def _on_q_up(self):
        self.keys_pressed.discard("q")
    
    def _on_e_down(self):
        self.keys_pressed.add("e")
    
    def _on_e_up(self):
        self.keys_pressed.discard("e")
    
    def _on_z_down(self):
        self.keys_pressed.add("z")
    
    def _on_z_up(self):
        self.keys_pressed.discard("z")
    
    def _on_x_down(self):
        self.keys_pressed.add("x")
    
    def _on_x_up(self):
        self.keys_pressed.discard("x")
    
    def _on_space_down(self):
        self.keys_pressed.add("space")
    
    def _on_space_up(self):
        self.keys_pressed.discard("space")
    
    def _on_control_down(self):
        self.keys_pressed.add("control")
    
    def _on_control_up(self):
        self.keys_pressed.discard("control")
