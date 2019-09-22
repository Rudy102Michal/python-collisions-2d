import pygame as pg
import math
import random
from numpy import array as Vector
from colorsys import hsv_to_rgb
import argparse

from drawers import CircleDrawer
from ball import Ball2D
from collision_handler import CircleCollisionHandler

BACKGROUND_COLOUR = (126, 161, 217)
WINDOW_SIZE = (1000, 500)
DEFAULT_BALL_COUNT = 4
DEFAULT_BALL_COLOUR = (45, 173, 60)
DEFAULT_INERTIA = 1.0


def build_arg_parser():
    parser = argparse.ArgumentParser(description="Simulation of colliding round objects in 2D space.By M. Gornicki")
    parser.add_argument("-W", "--width", type=int, help="Define screen width. Default: {}".format(WINDOW_SIZE[0]))
    parser.add_argument("-H", "--height", type=int, help="Define screen height. Default: {}".format(WINDOW_SIZE[1]))
    parser.add_argument("-b", "--balls", type=int,
                        help="Define initial number of collision objects. Default: {}".format(DEFAULT_BALL_COUNT))
    user_input_group = parser.add_mutually_exclusive_group()
    user_input_group.add_argument("-u", "--enable_user", action="store_true",
                       help="Allows user to spawn collision objects. Enabled by default.")
    user_input_group.add_argument("-d", "--disable_user", action="store_true",
                       help="Stop user from spawning collision objects. Disabled by default.")
    colouring_group = parser.add_mutually_exclusive_group()
    colouring_group.add_argument("--rgb", help="Define object colour in RGB format, i.e. '(R,G,B).'")
    colouring_group.add_argument("--hsv", action="store_true", help="Objects are coloured according to their mass.")
    parser.add_argument("--fps", action="store_true", help="Print current framerate to the standard output.")
    parser.add_argument("-i", "--inertia", type=float,
                        help="Objects' inertia. Value range [0, 1]. 0 -> resilient, 1 -> non-resilient")
    return parser


def process_arguments(args):
    global WINDOW_SIZE
    parameters = dict()
    if args.width:
        WINDOW_SIZE = (args.width, WINDOW_SIZE[1])
    if args.height:
        WINDOW_SIZE = (WINDOW_SIZE[0], args.height)
    if args.balls is not None and args.balls >= 0:
        parameters['BALL_COUNT'] = args.balls
    else:
        parameters['BALL_COUNT'] = DEFAULT_BALL_COUNT
    if args.disable_user:
        parameters['USER_INTERACTION'] = False
    else:
        parameters['USER_INTERACTION'] = True
    if args.rgb:
        parameters['HSV'] = False
        try:
            parameters['BALL_COLOUR'] = tuple([max(0, min(255, int(x))) for x in args.rgb.strip('()').split(',')])
        except:
            print("Wrong RGB format. Using default colour {}".format(DEFAULT_BALL_COLOUR))
            parameters['BALL_COLOUR'] = DEFAULT_BALL_COLOUR
    else:
        parameters['HSV'] = True
    parameters['DISPLAY_FPS'] = True if args.fps else False
    if args.inertia:
        parameters['INERTIA'] = max(0.0, min(args.inertia, 1.0))
    else:
        parameters['INERTIA'] = DEFAULT_INERTIA
    return parameters


def hsv_ball_colour_setter(colour, mass):
    hue = max(0.0, min(mass - 1.0, 20.0)) / 20.0
    return tuple(round(x * 255.0) for x in hsv_to_rgb(hue, 1.0, 1.0))


def rgb_ball_colour_setter(colour, mass):
    return colour


def spawn_balls(no_of_balls, window, params):
    balls = []
    i = 0
    while i < no_of_balls:
        radius = random.randrange(10, 50)
        x = random.randrange(radius + 5, WINDOW_SIZE[0] - radius - 5)
        y = random.randrange(radius + 5, WINDOW_SIZE[1] - radius - 5)
        rotation = random.uniform(0.0, math.pi)
        ang_velocity = random.uniform(-math.pi * 0.5, math.pi * 0.5)
        velocity = Vector([random.uniform(-15.0, 15.0), random.uniform(-15.0, 15.0)])
        c_setter = hsv_ball_colour_setter if params.get('HSV') else rgb_ball_colour_setter
        b = Ball2D(x, y, radius, params.get('BALL_COLOUR', DEFAULT_BALL_COLOUR), colour_setter=c_setter)
        b.set_drawer(CircleDrawer(window, b.get_position(), BACKGROUND_COLOUR, False))
        b.set_angular_velocity(ang_velocity)
        b.set_velocity(velocity * 10)
        if CircleCollisionHandler.detect_any_collision(balls, b):
            i -= 1
        else:
            balls.append(b)
        i += 1
    return balls


def spawn_user_ball(position, velocity, window, params):
    drawer = CircleDrawer(window, position, BACKGROUND_COLOUR, False)
    radius = random.randrange(10, 50)
    c_setter = hsv_ball_colour_setter if params.get('HSV') else rgb_ball_colour_setter
    ball = Ball2D(position[0], position[1], radius, params.get('BALL_COLOUR', DEFAULT_BALL_COLOUR), drawer=drawer,
                  colour_setter=c_setter)
    ball.set_velocity(velocity)
    return ball


if __name__ == "__main__":

    parser = build_arg_parser()
    parameters = process_arguments(parser.parse_args())

    random.seed()
    pg.init()

    window = pg.display.set_mode(WINDOW_SIZE)

    pg.display.set_caption("Collisions 2D")

    # Fill the whole background once at the beginning
    window.fill(BACKGROUND_COLOUR)
    pg.display.update()

    previous_time = pg.time.get_ticks()

    balls = spawn_balls(parameters.get("BALL_COUNT", DEFAULT_BALL_COUNT), window, parameters)

    collision_handler = CircleCollisionHandler(WINDOW_SIZE, parameters.get('INERTIA', DEFAULT_INERTIA))

    new_ball_position = None

    should_run = True

    while should_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                should_run = False
            if parameters.get('USER_INTERACTION'):
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    new_ball_position = Vector(event.pos)
                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    if new_ball_position is not None:
                        new_ball_velocity = Vector(event.pos) - new_ball_position
                        balls.append(spawn_user_ball(new_ball_position, new_ball_velocity, window, parameters))
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

        if parameters.get('DISPLAY_FPS') and dt > 0.0:
            print(1.0 / dt)
        pg.display.update(dirty_rects)
