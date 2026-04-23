"""
ObjectManager - Factory and registry for game objects
======================================================

Creates game objects and registers them in all necessary managers at once.
"""

from typing import List, Type, Optional, TYPE_CHECKING
from .scalable import GameObject
from ..spores.spore import Spore

if TYPE_CHECKING:
    from .zoom_manager import ZoomManager
    from ..spores.spore_manager import SporeManager


class ObjectManager:

    def __init__(self, zoom_manager: "ZoomManager"):
        self.zoom_manager = zoom_manager
        self._objects: List[GameObject] = []
        self._spore_manager: Optional["SporeManager"] = None

    def register_spore_manager(self, spore_manager: "SporeManager") -> None:
        self._spore_manager = spore_manager

    def create(self, cls: Type[GameObject], name: str, **kwargs) -> GameObject:
        """Create game object and register it in all managers."""
        obj = cls(**kwargs)
        self.zoom_manager.register_object(obj, name=name)
        self._objects.append(obj)
        if self._spore_manager is not None and isinstance(obj, Spore):
            self._spore_manager.register(name, obj)
        print(f"[ObjectManager] Created and registered: {name}")
        return obj

    def tick(self) -> None:
        for obj in self._objects:
            obj.tick()
        self.zoom_manager.update_transform()
