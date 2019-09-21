import pygame as pg
import math
import random

from drawers import CircleDrawer
from ball import Ball2D

BACKGROUND_COLOUR = (126, 161, 217)
WINDOW_SIZE = (1000, 500)


def spawn_balls(no_of_balls, window):
    balls = []
    for i in range(no_of_balls):
        radius = random.randrange(10, 50)
        x = random.randrange(radius + 5, WINDOW_SIZE[0] - radius - 5)
        y = random.randrange(radius + 5, WINDOW_SIZE[1] - radius - 5)
        rotation = math.pi * random.random()
        b = Ball2D(x, y, radius, rotation)
        b.set_drawer(CircleDrawer(window, b.get_position(), BACKGROUND_COLOUR, True))
        balls.append(b)
    return balls


if __name__ == "__main__":

    random.seed()
    pg.init()

    window = pg.display.set_mode(WINDOW_SIZE)

    pg.display.set_caption("Collisions 2D")

    # Fill the whole background once at the beginning
    window.fill(BACKGROUND_COLOUR)
    pg.display.update()

    previous_time = pg.time.get_ticks()

    balls = spawn_balls(2, window)

    should_run = True

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
