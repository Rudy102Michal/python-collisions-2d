import pygame as pg
import math
import numpy as np

class Ball2D:

    def __init__(self, draw_func, x, y, radius, rotation, colour=(0, 200, 50)):
        self._draw_func = draw_func
        self._position = np.array([x, y])
        self._radius = radius
        self._angle = rotation
        self._colour = colour
        self._velocity = np.array([10, 10])

    def draw(self):
        if self._draw_func:
            self._draw_func(self._position, self._radius, self._colour, self._angle)

    def update(self, dt):
        self._position += self._velocity * dt

    def inc_rot(self, dt):
        self._angle = self._angle + dt * math.pi / 2

pg.init()

window = pg.display.set_mode((1000, 500))

pg.display.set_caption("Collisions 2D")


def draw_circle(pos, r, col, rot):
    pg.draw.circle(window, col, pos, r)
    radius_end = (pos[0] + 0.8 * r * math.cos(rot), pos[1] + 0.8 * r * math.sin(rot))
    pg.draw.line(window, (100, 100, 100), pos, radius_end, 3)


should_run = True
c = Ball2D(draw_circle, 200, 200, 80, math.pi / 2)

while should_run:
    pg.time.delay(100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            should_run = False

   # pg.draw.circle(window, (0, 255, 0), (200, 200), 80)
    c.draw()
    c.update(0.016)
    c.inc_rot(0.016)
    pg.display.update()
