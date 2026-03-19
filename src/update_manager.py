"""
Update Manager - Centralized update handler
===========================================

Manages all per-frame updates in a centralized way.
Based on v16_picker UpdateManager but simplified for player_zoom sandbox.
"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .scene_setup import SceneSetup
    from .zoom_manager import ZoomManager
    from .input_manager import InputManager
    from .object_manager import ObjectManager


class UpdateManager:
    """
    Centralized class for calling update methods every frame.
    Simplified version adapted for player_zoom sandbox.

    Components can be registered after initialization to avoid circular dependencies.
    """

    def __init__(self):
        self.scene_setup: Optional["SceneSetup"] = None
        self.zoom_manager: Optional["ZoomManager"] = None
        self.input_manager: Optional["InputManager"] = None
        self.object_manager: Optional["ObjectManager"] = None

    def register_scene_setup(self, scene_setup: "SceneSetup") -> None:
        """Register SceneSetup component."""
        self.scene_setup = scene_setup

    def register_zoom_manager(self, zoom_manager: "ZoomManager") -> None:
        """Register ZoomManager component."""
        self.zoom_manager = zoom_manager

    def register_input_manager(self, input_manager: "InputManager") -> None:
        """Register InputManager component."""
        self.input_manager = input_manager

    def register_object_manager(self, object_manager: "ObjectManager") -> None:
        """Register ObjectManager component."""
        self.object_manager = object_manager

    def update_all(self, dt: float) -> None:
        """
        Main method that should be called every frame from the main loop.

        Args:
            dt: Delta time from Ursina (time.dt)
        """
        # Update input manager (per-frame input logic)
        if self.input_manager:
            self.input_manager.update()

        # Update scene (player movement, camera, etc.)
        if self.scene_setup:
            self.scene_setup.update(dt)

        # Update game objects (moves them + re-applies zoom transforms)
        if self.object_manager:
            self.object_manager.update_all(dt)

        # Update zoom system (calculate invariant point)
        if self.zoom_manager:
            self.zoom_manager.identify_invariant_point()
