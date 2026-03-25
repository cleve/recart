"""
Main game application for Spaceship Simulator.
Built on Panda3D ShowBase.
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Point3, TextNode, WindowProperties
from spaceship_simulator.config.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    HUD_COLOR_PRIMARY, HUD_COLOR_SECONDARY,
    INITIAL_SECTOR, get_string
)
from spaceship_simulator.ship.ship import ShipState
from spaceship_simulator.world.universe import Galaxy
from spaceship_simulator.world.world_renderer import WorldRenderer
from spaceship_simulator.input_handler import InputHandler
from spaceship_simulator.hud.realistic_hud import RealisticHUD
from spaceship_simulator.hud.radar_mouse import RadarMouseInteractor


class SpaceshipSimulator(ShowBase):
    """Main game application."""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        # Set window properties using Panda3D's WindowProperties
        props = WindowProperties()
        props.set_size(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.win.request_properties(props)
        self.set_background_color(0.0, 0.0, 0.0)
        
        # Game state
        self.ship = ShipState()
        self.ship.position = Vec3(*INITIAL_SECTOR)
        self.universe = Galaxy(seed=42)  # Fixed seed for reproducibility
        self.world_renderer = None
        
        # Input
        self.input_handler = InputHandler(self.ship, self)
        self.radar_mouse = None
        
        # HUD system
        self.hud = None  # Will be initialized in _setup_hud_system
        
        # View mode (0=firstperson, 1=top, 2=rear, 3=side)
        self.view_mode = 0
        self.paused = False
        self.show_help = False
        
        # Communications queue
        self.comms_messages = []
        
        # Frame timing
        self.last_frame_time = 0
        
        self._setup_scene()
        self._setup_hud_system()
        self._setup_input()
        self._setup_tasks()
        
        # Welcome message
        self.add_comms_message(get_string("welcome", "en"))
    
    def _setup_scene(self):
        """Setup the 3D scene and camera."""
        # Disable default camera control
        self.disable_mouse()

        # Build visible entity geometry for main 3D view.
        self.world_renderer = WorldRenderer(self, self.universe, self.ship)
        
        # Setup camera for first-person view
        self.camera.set_pos(0, 5, 0)
        self.camera.look_at(Point3(0, 5, -1))
    
    def _setup_hud_system(self):
        """Setup the realistic HUD display."""
        self.hud = RealisticHUD(self, self.ship, self.universe)
        self.hud.set_view_mode(self.view_mode)
    
    
    
    def _setup_input(self):
        """Setup input handlers."""
        self.input_handler.setup()
        self.radar_mouse = RadarMouseInteractor(self, self.hud, self.ship)
        self.radar_mouse.setup()
    
    def _setup_tasks(self):
        """Setup game loop tasks."""
        self.taskMgr.add(self._game_loop, "game_loop")
        self.taskMgr.add(self._update_hud, "update_hud")
        self.taskMgr.add(self._update_camera, "update_camera")
        self.taskMgr.add(self._update_world_visuals, "update_world_visuals")
    
    def _game_loop(self, task):
        """Main game loop."""
        if self.paused:
            return task.cont
        
        current_time = globalClock.get_frame_time()
        dt = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        # Limit dt to reasonable values
        dt = min(max(dt, 0.001), 0.05)  # Between 1ms and 50ms
        
        # Update input
        self.input_handler.update()
        
        # Update ship
        self.ship.update(dt)
        
        # Check proximity to entities
        self._check_nearby_entities()
        
        return task.cont
    
    def _update_hud(self, task):
        """Update the realistic HUD display."""
        self.hud.update(task.getDt(), self.ship, self.universe, self.view_mode)
        return task.cont
    
    def _update_camera(self, task):
        """Update camera to follow ship in current view mode."""
        ship_pos = self.ship.position
        
        if self.view_mode == 0:  # First-person
            self.camera.set_pos(ship_pos + self.ship.up * 5)
            look_target = ship_pos + self.ship.forward * 20
            self.camera.look_at(look_target)
        elif self.view_mode == 1:  # Top-down
            self.camera.set_pos(ship_pos.x, ship_pos.y + 80, ship_pos.z)
            self.camera.look_at(ship_pos)
        elif self.view_mode == 2:  # Rear
            self.camera.set_pos(ship_pos - self.ship.forward * 30)
            self.camera.look_at(ship_pos)
        elif self.view_mode == 3:  # Side
            self.camera.set_pos(ship_pos + self.ship.right * 30 + self.ship.up * 10)
            self.camera.look_at(ship_pos)
        
        return task.cont

    def _update_world_visuals(self, task):
        """Update 3D world entities visibility around the ship."""
        if self.world_renderer is not None:
            self.world_renderer.update(task.getDt())
        return task.cont
    
    def _check_nearby_entities(self):
        """Check for nearby entities and trigger events."""
        from spaceship_simulator.config.constants import RADAR_RANGE
        nearby = self.universe.get_nearby_entities(self.ship.position, RADAR_RANGE)
        
        for entity in nearby:
            if not entity.discovered:
                entity.discovered = True
                msg = f"[DISCOVERY] {entity.name} detected"
                self.add_comms_message(msg)
    
    def add_comms_message(self, message: str):
        """Add a message to the communications queue."""
        self.comms_messages.append(message)
        if len(self.comms_messages) > 10:
            self.comms_messages.pop(0)
        
        # Also print to console for now
        print(f"[COMMS] {message}")
    
    def set_view_mode(self, mode: int):
        """Change the camera view mode."""
        if 0 <= mode <= 3:
            self.view_mode = mode
            modes = ["First-Person", "Top-Down", "Rear", "Side"]
            self.add_comms_message(f"View mode: {modes[mode]}")
    
    def toggle_help(self):
        """Toggle help display."""
        self.show_help = not self.show_help
        if self.show_help:
            self.add_comms_message("Help: " + get_string("controls", "en"))
    
    def toggle_pause(self):
        """Toggle game pause."""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RESUMED"
        self.add_comms_message(status)
    
    def userExit(self):
        """Handle user exit request."""
        print("Exiting spaceship simulator...")
        import sys
        sys.exit()


def main():
    """Entry point for the game."""
    app = SpaceshipSimulator()
    app.run()


if __name__ == "__main__":
    main()
