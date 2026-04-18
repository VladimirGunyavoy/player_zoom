"""
Simplified InputManager for player_zoom
Handles only basic commands: zoom, movement, UI
"""

from ursina import held_keys, mouse, application
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .scene_setup import SceneSetup
    from .zoom_manager import ZoomManager
    from .window_manager import WindowManager
    from .object_manager import ObjectManager


class InputManager:
    """
    Simplified class for handling user input in player_zoom.
    Supports only basic commands.

    Components can be registered after initialization to avoid circular dependencies.
    """
    def __init__(self):
        self.scene_setup: Optional["SceneSetup"] = None
        self.zoom_manager: Optional["ZoomManager"] = None
        self.window_manager: Optional["WindowManager"] = None
        self.object_manager: Optional["ObjectManager"] = None

        print(f"[DEBUG] InputManager initialized (simplified version)")

    def register_scene_setup(self, scene_setup: "SceneSetup") -> None:
        """Register SceneSetup component."""
        self.scene_setup = scene_setup
        print(f"   scene_setup: registered")

    def register_zoom_manager(self, zoom_manager: "ZoomManager") -> None:
        """Register ZoomManager component."""
        self.zoom_manager = zoom_manager
        print(f"   zoom_manager: registered")

    def register_window_manager(self, window_manager: "WindowManager") -> None:
        """Register WindowManager component."""
        self.window_manager = window_manager
        print(f"   window_manager: registered")

    def register_object_manager(self, object_manager: "ObjectManager") -> None:
        """Register ObjectManager component."""
        self.object_manager = object_manager
        print(f"   object_manager: registered")

    def handle_input(self, key: str) -> None:
        """Handle key press."""

        # Exit
        if key == 'escape':
            application.quit()
            return

        # Fullscreen mode
        if key == 'f11' and self.window_manager:
            self.window_manager.toggle_fullscreen()
            print(f"   [Window] Fullscreen: {'enabled' if self.window_manager.is_fullscreen() else 'disabled'}")
            return

        # Toggle cursor
        if key == 'alt' and self.scene_setup:
            self.scene_setup.toggle_freeze()
            return

        # If input is frozen, don't process scene-level commands
        if self.scene_setup and self.scene_setup.input_frozen:
            return

        # === GAME OBJECTS ===
        if self.object_manager:
            self.object_manager.handle_input(key)

        # === ZOOM ===
        if self.zoom_manager:
            if key == 'e' or key == 'scroll up':
                self.zoom_manager.zoom_in()
                print("   [Zoom] Zoom in")
                return

            if key == 'q' or key == 'scroll down':
                self.zoom_manager.zoom_out()
                print("   [Zoom] Zoom out")
                return

            if key == 'r':
                self.zoom_manager.reset_zoom()
                print("   [Zoom] Reset")
                return

        # === FRAME ===
        if key == 'u' and self.scene_setup:
            self.scene_setup.toggle_frame()
            return

        # === DEBUG ===
        if key == 'h':
            self._print_debug_info()
            return

    def _print_debug_info(self):
        """Print debug information."""
        print("\n" + "=" * 50)
        print("DEBUG INFO")
        print("=" * 50)

        if self.scene_setup:
            print(f"Camera position: {self.scene_setup.player.position}")
            print(f"Camera rotation: y={self.scene_setup.player.rotation_y}, "
                  f"x={self.scene_setup.player.camera_pivot.rotation_x}")
            print(f"Cursor locked: {self.scene_setup.cursor_locked}")
            print(f"Input frozen: {self.scene_setup.input_frozen}")

        if self.zoom_manager:
            print(f"Zoom transform: a={self.zoom_manager.a_transformation:.4f}")
            print(f"Zoom translation: {self.zoom_manager.b_translation}")
            print(f"Registered objects: {len(self.zoom_manager.objects)}")

            # Look point
            look_x, look_z = self.zoom_manager.identify_invariant_point()
            print(f"Look point: ({look_x:.4f}, {look_z:.4f})")

        if self.scene_setup:
            print(f"Frame visible: {self.scene_setup.frame.is_visible()}")

        print("=" * 50 + "\n")

    def update(self):
        """Update state (called every frame)."""
        # Currently nothing, but can add logic here
        pass
