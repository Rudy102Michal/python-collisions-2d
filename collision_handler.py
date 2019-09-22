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

    @staticmethod
    def _detect_pair_collision(a, b):
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
                pos[0] = max(r, min(self._width - r, pos[0]))
            if pos[1] <= r or pos[1] >= (self._height - r):
                vel[1] *= -1
                pos[1] = max(r, min(self._height - r, pos[1]))
            o.set_velocity(vel)

    def handle_collisions(self, objects, drawer):
        for i in range(len(objects)):
            a = objects[i]
            for j in range(i + 1, len(objects)):
                b = objects[j]
                if CircleCollisionHandler._detect_pair_collision(a, b):
                    print("Collision!")
                    col_normal = a.get_position() - b.get_position()
                    col_normal /= np.linalg.norm(col_normal)

                    if np.dot(col_normal, a.get_velocity() - b.get_velocity()) >= 0.0:
                        continue

                    e = 1.0
                    J = a.get_mass() * b.get_mass() * (e + 1.0) / (a.get_mass() + b.get_mass())
                    J *= np.dot(a.get_velocity() - b.get_velocity(), col_normal)

                    u1 = a.get_velocity() - (J / a.get_mass()) * col_normal
                    u2 = b.get_velocity() + (J / b.get_mass()) * col_normal

                    a.set_velocity(u1)
                    b.set_velocity(u2)

                    # drawer(col_normal)

                    # restitution = 1.0
                    # friction = 1.0
                    # tangent = np.array([-col_normal[1], col_normal[0]])
                    # v1 = a.get_velocity() + a.get_angular_velocity() * a.get_radius() * tangent
                    # v2 = b.get_velocity() + b.get_angular_velocity() * b.get_radius() * tangent * -1
                    # relative_v = v1 - v2
                    # tan_vel_component = tangent * np.dot(relative_v, tangent)
                    # col_point1 = -col_normal * a.get_radius()
                    # col_point2 = col_normal * b.get_radius()
                    #
                    # col_response = (1.0 + restitution) * np.dot(col_normal, relative_v) \
                    #                + np.cross(col_point1, col_normal) * a.get_angular_velocity() \
                    #                - np.cross(col_point2, col_normal) * b.get_angular_velocity()
                    # col_response /= 2.0 + np.cross(col_point1, col_normal) * a.get_inertia() \
                    #                 + np.cross(col_point2, col_normal) * b.get_inertia()
                    # a_new_vel = a.get_velocity() - (col_normal - friction * tan_vel_component) * col_response / a.get_mass()
                    # b_new_vel = a.get_velocity() + (col_normal - friction * tan_vel_component) * col_response / b.get_mass()
                    # a.set_velocity(a_new_vel)
                    # b.set_velocity(b_new_vel)
                    # a_new_ang_vel = a.get_angular_velocity() - col_response \
                    #                 * np.cross(col_point1, col_normal - friction * tan_vel_component) / a.get_inertia()
                    # b_new_ang_vel = a.get_angular_velocity() + col_response \
                    #                 * np.cross(col_point2, col_normal - friction * tan_vel_component) / b.get_inertia()
                    # a.set_angular_velocity(a_new_ang_vel)
                    # b.set_angular_velocity(b_new_ang_vel)

    @staticmethod
    def detect_any_collision(objects, subject):
        for o in objects:
            if CircleCollisionHandler._detect_pair_collision(o, subject):
                return True
        else:
            return False

    @staticmethod
    def _detect_pair_collision(a, b):
        return True if np.sqrt(np.sum((a.get_position() - b.get_position())**2)) <= (a.get_radius() + b.get_radius()) \
            else False
