import numpy as np


class CollisionHandler:

    def __init__(self, bound_size):
        self._width = bound_size[0]
        self._height = bound_size[1]

    def handle_boundaries(self, objects):
        raise NotImplementedError()

    @staticmethod
    def detect_any_collision(objects, subject):
        raise NotImplementedError()


class CircleCollisionHandler(CollisionHandler):

    def __init__(self, bound_size):
        CollisionHandler.__init__(self, bound_size)

    def handle_boundaries(self, objects):
        for o in objects:
            r = o.get_radius()
            vel = o.get_velocity()
            pos = o.get_position()
            if pos[0] <= r or pos[0] >= (self._width - r):
                vel[0] *= -1
            if pos[1] <= r or pos[1] >= (self._height - r):
                vel[1] *= -1
            o.set_velocity(vel)

    @staticmethod
    def detect_any_collision(objects, subject):
        for o in objects:
            dist = np.sqrt(np.sum((o.get_position() - subject.get_position())**2))
            if dist < (o.get_radius() + subject.get_radius()):
                return True
        else:
            return False
