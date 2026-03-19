"""
ObjectManager - Factory and registry for game objects
======================================================

Creates game objects and registers them in all necessary managers at once.
"""

from typing import List, Tuple, Callable, Type, TYPE_CHECKING
from .scalable import GameObject

if TYPE_CHECKING:
    from .zoom_manager import ZoomManager


class ObjectManager:
    """
    Factory + registry for game objects.
    Creates objects and registers them in zoom/update/input managers.
    """

    def __init__(self, zoom_manager: "ZoomManager"):
        self.zoom_manager = zoom_manager
        self._objects: List[GameObject] = []
        self._bindings: List[Tuple[Callable, Callable]] = []

    def create(self, cls: Type[GameObject], name: str, **kwargs) -> GameObject:
        """Create game object and register it in all managers."""
        obj = cls(**kwargs)
        self.zoom_manager.register_object(obj, name=name)
        self._objects.append(obj)
        print(f"[ObjectManager] Created and registered: {name}")
        return obj

    def bind(self, func: Callable, trigger: Callable[[str], bool]) -> None:
        """Bind action to a trigger. trigger(key) -> bool decides when to fire."""
        self._bindings.append((func, trigger))

    def update_all(self, dt: float) -> None:
        """Update all game objects, then re-apply zoom transforms."""
        for obj in self._objects:
            obj.tick(dt)
        self.zoom_manager.update_transform()

    def handle_input(self, key: str) -> None:
        """Fire all bindings whose trigger matches the key."""
        for func, trigger in self._bindings:
            if trigger(key):
                func()
