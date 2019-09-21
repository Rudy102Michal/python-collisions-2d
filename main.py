import pygame as pg
import math
import numpy as np


BACKGROUND_COLOUR = (126, 161, 217)


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


pg.init()

window = pg.display.set_mode((1000, 500))

pg.display.set_caption("Collisions 2D")

window.fill(BACKGROUND_COLOUR)
pg.display.update()


class CircleDrawer:

    def __init__(self, first_pos, rotating=False):
        self._previous_pos = first_pos
        self._rotating = rotating

    def draw(self, position, radius, colour, rotation=0.0):
        old_rect = pg.Rect(self._previous_pos[0] - radius,
                           self._previous_pos[1] - radius,
                           radius * 2, radius * 2)
        pg.draw.rect(window, BACKGROUND_COLOUR, old_rect)
        new_rect = pg.Rect(position[0] - radius,
                           position[1] - radius,
                           radius * 2, radius * 2)
        i_pos = (int(round(position[0])), int(round(position[1])))  # pygame draw requires ints
        pg.draw.circle(window, colour, i_pos, radius)
        if self._rotating:
            radius_end = (int(round(position[0] + 0.8 * radius * math.cos(rotation))),
                          int(round(position[1] + 0.8 * radius * math.sin(rotation))))
            pg.draw.line(window, (100, 100, 100), i_pos, np.round(radius_end), 3)
        return old_rect, new_rect


should_run = True
c = Ball2D(200, 200, 80, math.pi / 2)
c.set_drawer(CircleDrawer(c.get_position(), True))

previous_time = pg.time.get_ticks()

balls = [c]

while should_run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            should_run = False

    current_time = pg.time.get_ticks()
    dt = float(current_time - previous_time) / 1000.0
    previous_time = current_time
    dirty_rects = []

    for b in balls:
        rects = b.draw()
        b.update(dt)
        dirty_rects += rects

    print(dt)
    pg.display.update(dirty_rects)
