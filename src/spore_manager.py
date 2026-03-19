"""
SporeManager - Manages visual size of all Spore objects
=========================================================

Stores current size and updates all registered spores at once.
"""

import numpy as np
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .spore import Spore
    from .zoom_manager import ZoomManager


class SporeManager:

    def __init__(self, zoom_manager: "ZoomManager", initial_size: float = 0.05):
        self._spores: List["Spore"] = []
        self._zoom_manager = zoom_manager
        self.size = initial_size

    def register(self, spore: "Spore") -> None:
        self._spores.append(spore)

    def increase_size(self, factor: float = 1.2) -> None:
        self.size *= factor
        self._update_all()
        print(f"[SporeManager] Size: {self.size:.3f}")

    def decrease_size(self, factor: float = 1.2) -> None:
        self.size /= factor
        self._update_all()
        print(f"[SporeManager] Size: {self.size:.3f}")

    def _update_all(self) -> None:
        for spore in self._spores:
            spore.real_scale = np.array([self.size, self.size, self.size])
        self._zoom_manager.update_transform()
