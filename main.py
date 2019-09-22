import pygame as pg
import math
import random
from numpy import array as Vector
from colorsys import hsv_to_rgb

from drawers import CircleDrawer
from ball import Ball2D
from collision_handler import CircleCollisionHandler

BACKGROUND_COLOUR = (126, 161, 217)
WINDOW_SIZE = (1000, 500)
BALL_COUNT = 4


def ball_colour_setter(colour, mass):
    hue = max(0.0, min(mass - 1.0, 20.0)) / 20.0
    return tuple(round(x * 255.0) for x in hsv_to_rgb(hue, 1.0, 1.0))


def spawn_balls(no_of_balls, window):
    balls = []
    i = 0
    while i < no_of_balls:
        radius = random.randrange(10, 50)
        x = random.randrange(radius + 5, WINDOW_SIZE[0] - radius - 5)
        y = random.randrange(radius + 5, WINDOW_SIZE[1] - radius - 5)
        rotation = random.uniform(0.0, math.pi)
        ang_velocity = random.uniform(-math.pi * 0.5, math.pi * 0.5)
        velocity = Vector([random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)])
        b = Ball2D(x, y, radius, rotation, colour_setter=ball_colour_setter)
        b.set_drawer(CircleDrawer(window, b.get_position(), BACKGROUND_COLOUR, True))
        b.set_angular_velocity(ang_velocity)
        b.set_velocity(velocity * 10)
        if CircleCollisionHandler.detect_any_collision(balls, b):
            i -= 1
        else:
            balls.append(b)
        i += 1
    return balls


def spawn_user_ball(position, velocity, window):
    drawer = CircleDrawer(window, position, BACKGROUND_COLOUR, False)
    radius = random.randrange(10, 50)
    ball = Ball2D(position[0], position[1], radius, drawer=drawer, colour_setter=ball_colour_setter)
    ball.set_velocity(velocity)
    return ball


if __name__ == "__main__":

    random.seed()
    pg.init()

    window = pg.display.set_mode(WINDOW_SIZE)

    pg.display.set_caption("Collisions 2D")

    # Fill the whole background once at the beginning
    window.fill(BACKGROUND_COLOUR)
    pg.display.update()

    previous_time = pg.time.get_ticks()

    balls = spawn_balls(BALL_COUNT, window)

    collision_handler = CircleCollisionHandler(WINDOW_SIZE, 1.0)

    new_ball_position = None

    should_run = True

    while should_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                should_run = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                print("DOWN")
                new_ball_position = Vector(event.pos)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                print("UP")
                if new_ball_position is not None:
                    new_ball_velocity = Vector(event.pos) - new_ball_position
                    print(new_ball_velocity)
                    balls.append(spawn_user_ball(new_ball_position, new_ball_velocity, window))
                    new_ball_position = None

        current_time = pg.time.get_ticks()
        dt = float(current_time - previous_time) / 1000.0
        previous_time = current_time
        dirty_rects = []

        for b in balls:
            rects = b.draw_cleanup()
            dirty_rects += rects

        collision_handler.handle_boundaries(balls)
        collision_handler.handle_collisions(balls)

        energy = 0.0
        for b in balls:
            rects = b.draw()
            b.update(dt)
            dirty_rects += rects

        # print(dt)
        pg.display.update(dirty_rects)
