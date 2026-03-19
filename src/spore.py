"""
Spore - Static visual marker (inherits MyObject)
==================================================

A static sphere placed at a given position.
Used for trajectory visualization.
"""

import numpy as np
from ursina import color as ursina_color
from .my_object import MyObject


class Spore(MyObject):

    def __init__(self, pos=(0, 0, 0), color_value=ursina_color.green, **kwargs):
        super().__init__(radius=0, speed=0, color_value=color_value, model='quad', **kwargs)
        self.billboard = True  # всегда смотрит на камеру
        self.position = pos
        self.real_position = np.array(pos, dtype=float)

    def tick(self, dt: float) -> None:
        pass  # статичный объект, не двигается
