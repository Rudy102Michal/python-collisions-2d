import pygame as pg
import math
import numpy as np


class Drawer:

    def __init__(self):
        pass

    def draw(self):
        raise NotImplementedError()


class CircleDrawer(Drawer):

    def __init__(self, surface, first_pos, background_colour=(0, 0, 0), rotating=False):
        Drawer.__init__(self)
        self._previous_pos = first_pos
        self._surface = surface
        self._bg_colour = background_colour
        self._rotating = rotating

    def draw(self, position, radius, colour, rotation=0.0):
        old_rect = pg.Rect(self._previous_pos[0] - radius,
                           self._previous_pos[1] - radius,
                           radius * 2, radius * 2)
        pg.draw.rect(self._surface, self._bg_colour, old_rect)
        new_rect = pg.Rect(position[0] - radius,
                           position[1] - radius,
                           radius * 2, radius * 2)
        i_pos = (int(round(position[0])), int(round(position[1])))  # pygame draw requires ints
        pg.draw.circle(self._surface, colour, i_pos, radius)
        if self._rotating:
            radius_end = (int(round(position[0] + 0.8 * radius * math.cos(rotation))),
                          int(round(position[1] + 0.8 * radius * math.sin(rotation))))
            pg.draw.line(self._surface, (100, 100, 100), i_pos, np.round(radius_end), 3)
        return old_rect, new_rect
