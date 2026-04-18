"""
Spore - Static visual marker
==============================

A flat circle placed at a given (x, z) position.
Used for trajectory visualization.
"""

import numpy as np
from ursina import color, Circle
from .scalable import GameObject
from typing import Any


class Spore(GameObject):

    def __init__(self, position=None, *args: Any, **kwargs: Any):
        y_offset = 0.01
        pos_3d = (0, y_offset, 0) if position is None else (position[0], y_offset, position[1])

        super().__init__(
            model=Circle(resolution=32),
            scale=0.23,
            color=color.white,
            rotation=(90, 0, 0),
            double_sided=True,
            alpha=0.5,
            position=pos_3d,
            *args, **kwargs
        )

        self.y_offset = y_offset
        self.real_position = np.array(pos_3d, dtype=float)
