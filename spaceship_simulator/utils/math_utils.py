"""
Math utilities for spaceship simulator.
"""

from panda3d.core import Vec3
import math


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def distance(pos1: Vec3, pos2: Vec3) -> float:
    """Calculate distance between two 3D positions."""
    return (pos1 - pos2).length()


def angle_between(vec1: Vec3, vec2: Vec3) -> float:
    """Calculate angle between two vectors in degrees."""
    v1_norm = vec1.normalized()
    v2_norm = vec2.normalized()
    dot = v1_norm.dot(v2_norm)
    dot = clamp(dot, -1.0, 1.0)
    return math.degrees(math.acos(dot))


def normalize(vec: Vec3) -> Vec3:
    """Normalize a vector."""
    return vec.normalized()


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between two values."""
    return a + (b - a) * clamp(t, 0.0, 1.0)


def exponential_decay(current: float, target: float, decay_rate: float, dt: float) -> float:
    """Exponential decay towards a target value."""
    return current + (target - current) * (1.0 - math.exp(-decay_rate * dt))
