import math
import numpy as np


class Ball2D:

    def __init__(self, x, y, radius, rotation, colour=(45, 173, 60), drawer=None):
        self._position = np.array([float(x), float(y)])
        self._radius = radius
        self._angle = rotation
        self._colour = colour
        self._velocity = np.array([10, 10])
        self._angular_velocity = math.pi / 8
        self._drawer = drawer

    def draw(self):
        return self._drawer.draw(self._position, self._radius, self._colour, self._angle) if self._drawer else tuple()

    def update(self, delta):
        self._position += self._velocity * delta
        self._angle += self._angular_velocity * delta

    def set_drawer(self, drawer):
        self._drawer = drawer

    def get_position(self):
        return self._position

    def set_velocity(self, velocity):
        self._velocity = velocity
