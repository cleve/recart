"""
Ship state and systems management.
"""

from panda3d.core import Vec3
from spaceship_simulator.config.constants import (
    INITIAL_ENERGY, MAX_ENERGY, ENERGY_REGEN_RATE,
    INITIAL_SHIELD, MAX_SHIELD, SHIELD_REGEN_RATE,
    INITIAL_OXYGEN, MAX_OXYGEN, OXYGEN_DRAIN_RATE,
    MAX_VELOCITY, MAX_ACCELERATION, ACCELERATION_RATE,
    ROTATION_SPEED, STRAFE_SPEED,
)
from spaceship_simulator.utils.math_utils import clamp, exponential_decay


class ShipState:
    """Manages ship state: position, velocity, systems."""
    
    def __init__(self):
        # Position and movement
        self.position = Vec3(0, 0, 0)
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        
        # Rotation (Euler angles: heading, pitch, roll)
        self.heading = 0.0  # Yaw
        self.pitch = 0.0
        self.roll = 0.0
        
        # Local axes (forward, up, right)
        self.forward = Vec3(0, 0, -1)  # -Z is forward in Panda3D
        self.up = Vec3(0, 1, 0)
        self.right = Vec3(1, 0, 0)
        
        # System states
        self.energy = INITIAL_ENERGY
        self.shield = INITIAL_SHIELD
        self.hull = 100.0
        self.oxygen = INITIAL_OXYGEN
        self.atmosphere = 0.0  # 0-100, presence of breathable air
        self.cargo = 0.0  # Available cargo space %
        self.crew_health = 100.0  # Overall crew health %
        
        # Thrust input (-1 to 1)
        self.thrust_input = 0.0
        self.strafe_input = 0.0  # Vertical strafe
        
        # Rotation input (-1 to 1)
        self.yaw_input = 0.0
        self.pitch_input = 0.0
        self.roll_input = 0.0
        
        # Helm status
        self.in_atmosphere = False
        self.docked = False
        self.alert_level = 0  # 0=normal, 1=yellow, 2=red
    
    def update(self, dt: float):
        """Update ship state based on time delta."""
        # Update velocity based on thrust input (forward/backward)
        desired_forward_speed = self.thrust_input * MAX_VELOCITY
        current_forward_speed = self.velocity.dot(self.forward)  # Project velocity onto forward axis
        
        new_forward_speed = exponential_decay(
            current_forward_speed,
            desired_forward_speed,
            ACCELERATION_RATE,
            dt
        )
        
        # Set velocity in forward direction (Vec3 * float, not float * Vec3)
        self.velocity = self.forward * new_forward_speed
        
        # Add strafe movement (vertical — Space = up, Ctrl = down)
        strafe_amount = self.strafe_input * STRAFE_SPEED
        self.velocity += self.up * strafe_amount
        
        # Update position
        self.position += self.velocity * dt
        
        # Update rotation
        if self.yaw_input != 0:
            self.heading += self.yaw_input * ROTATION_SPEED
        if self.pitch_input != 0:
            self.pitch += self.pitch_input * ROTATION_SPEED
        if self.roll_input != 0:
            self.roll += self.roll_input * ROTATION_SPEED
        
        # Clamp pitch to -90 to 90 degrees
        self.pitch = clamp(self.pitch, -90, 90)
        
        # Recalculate local axes based on rotation
        self._update_axes()
        
        # Update ship systems
        self._update_energy(dt)
        self._update_oxygen(dt)
        self._update_shields(dt)
    
    def _update_axes(self):
        """Recalculate forward, up, right vectors based on rotation."""
        import math
        
        # Convert to radians
        h = math.radians(self.heading)
        p = math.radians(self.pitch)
        r = math.radians(self.roll)
        
        # Calculate forward vector (based on heading and pitch)
        self.forward = Vec3(
            math.sin(h) * math.cos(p),
            -math.sin(p),
            -math.cos(h) * math.cos(p)
        )
        
        # Calculate right vector (perpendicular to forward, affected by yaw)
        right_h = math.radians(self.heading + 90)
        self.right = Vec3(
            math.sin(right_h),
            0,
            -math.cos(right_h)
        )
        
        # Calculate up vector (perpendicular to both)
        self.up = self.forward.cross(self.right).normalized()
    
    def _update_energy(self, dt: float):
        """Update energy levels with regeneration."""
        regen_amount = ENERGY_REGEN_RATE * dt
        self.energy = clamp(self.energy + regen_amount, 0, MAX_ENERGY)
    
    def _update_oxygen(self, dt: float):
        """Update oxygen levels."""
        if not self.in_atmosphere:
            drain = OXYGEN_DRAIN_RATE * dt
            self.oxygen = clamp(self.oxygen - drain, 0, MAX_OXYGEN)
        else:
            # Regenerate slowly in atmosphere
            regen = 10.0 * dt
            self.oxygen = clamp(self.oxygen + regen, 0, MAX_OXYGEN)
    
    def _update_shields(self, dt: float):
        """Update shield levels with regeneration."""
        regen_amount = SHIELD_REGEN_RATE * dt
        self.shield = clamp(self.shield + regen_amount, 0, MAX_SHIELD)
    
    def set_alert_level(self, level: int):
        """Set alert level (0=normal, 1=yellow, 2=red)."""
        self.alert_level = clamp(level, 0, 2)
