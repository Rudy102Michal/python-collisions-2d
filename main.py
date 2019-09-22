import pygame as pg
import math
import random
import numpy

from drawers import CircleDrawer
from ball import Ball2D
from collision_handler import CircleCollisionHandler

BACKGROUND_COLOUR = (126, 161, 217)
WINDOW_SIZE = (1000, 500)


def spawn_balls(no_of_balls, window):
    balls = []
    i = 0
    while i < no_of_balls:
        radius = random.randrange(10, 50)
        x = random.randrange(radius + 5, WINDOW_SIZE[0] - radius - 5)
        y = random.randrange(radius + 5, WINDOW_SIZE[1] - radius - 5)
        rotation = random.uniform(0.0, math.pi)
        ang_velocity = random.uniform(-math.pi * 0.5, math.pi * 0.5)
        velocity = numpy.array([random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)])
        b = Ball2D(x, y, radius, rotation)
        b.set_drawer(CircleDrawer(window, b.get_position(), BACKGROUND_COLOUR, True))
        b.set_angular_velocity(ang_velocity)
        b.set_velocity(velocity * 10)
        if CircleCollisionHandler.detect_any_collision(balls, b):
            i -= 1
        else:
            balls.append(b)
        i += 1
    return balls


if __name__ == "__main__":

    random.seed()
    pg.init()

    window = pg.display.set_mode(WINDOW_SIZE)

    norms = []
    def draw_tangent(v):
        pg.draw.line(window, (100, 100, 100), (200, 200), (200 + int(20.0 * v[0]), 200 + int(20.0 * v[1])), 3)
        norms.append(pg.Rect((200, 200), (200 + int(20.0 * v[0]), 200 + int(20.0 * v[1]))))


    pg.display.set_caption("Collisions 2D")

    # Fill the whole background once at the beginning
    window.fill(BACKGROUND_COLOUR)
    pg.display.update()

    previous_time = pg.time.get_ticks()

    balls = spawn_balls(5, window)

    collision_handler = CircleCollisionHandler(WINDOW_SIZE)

    should_run = True

    while should_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                should_run = False

        current_time = pg.time.get_ticks()
        dt = float(current_time - previous_time) / 1000.0
        previous_time = current_time
        dirty_rects = [] + norms

        for b in balls:
            rects = b.draw_cleanup()
            dirty_rects += rects

        collision_handler.handle_boundaries(balls)
        collision_handler.handle_collisions(balls, draw_tangent)

        for b in balls:
            rects = b.draw()
            b.update(dt)
            dirty_rects += rects

        print(dt)
        pg.display.update(dirty_rects)
