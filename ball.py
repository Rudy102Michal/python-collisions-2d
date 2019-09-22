import math
import numpy as np


class Ball2D:

    def __init__(self, x, y, radius, rotation=0.0, mass=1.0, colour=(45, 173, 60), drawer=None):
        self._position = np.array([float(x), float(y)])
        self._radius = radius
        self._angle = rotation
        self._mass = (radius / 10.0) * 2
        self._colour = colour
        self._velocity = np.array([10, 10])
        self._angular_velocity = 0
        self._drawer = drawer

    def draw(self):
        return self._drawer.draw(self._position, self._radius, self._colour, self._angle) if self._drawer else []

    def draw_cleanup(self):
        return self._drawer.draw_cleanup(self._radius) if self._drawer else []

    def update(self, delta):
        self._position += self._velocity * delta
        self._angle += self._angular_velocity * delta

    def set_drawer(self, drawer):
        self._drawer = drawer

    def get_position(self):
        return self._position

    def get_radius(self):
        return self._radius

    def set_velocity(self, velocity):
        self._velocity = velocity

    def get_velocity(self):
        return self._velocity

    def set_angular_velocity(self, angular_velocity):
        self._angular_velocity = angular_velocity

    def get_angular_velocity(self):
        return self._angular_velocity

    def get_mass(self):
        return self._mass

    def get_inertia(self):
        return (self._radius ** 2) * self._mass
