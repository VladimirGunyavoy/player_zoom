"""
PLAYER ZOOM - Camera and Zoom Sandbox
======================================

Simplified sandbox for camera, zoom, and control experiments.
Extracted from v16_picker for independent development.

Features:
- FirstPersonController with extended controls
- Zoom system with invariant point (look point)
- Grid floor and coordinate system
- Window and monitor management

Controls:
- WASD: movement
- Mouse: look around
- Space/Shift: up/down
- Alt: release/capture cursor
- Escape: exit
- Q/E: zoom out/in
- R: reset zoom
- F11: fullscreen mode
- H: debug info
"""

import sys
import os

# Add src path to PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ursina import Ursina, application
from src.scene_setup import SceneSetup
from src.zoom_manager import ZoomManager
from src.window_manager import WindowManager
from src.color_manager import ColorManager
from src.scalable import ScalableFloor, Scalable
from src.input_manager import InputManager
from src.update_manager import UpdateManager
from src.object_manager import ObjectManager
from src.my_object import MyObject
from ursina import color


print("=" * 50)
print("PLAYER ZOOM - Sandbox")
print("=" * 50)

# ===== INITIALIZATION =====
app = Ursina()

# ===== CREATING MANAGERS (independent, no dependencies) =====
color_manager = ColorManager()
window_manager = WindowManager(monitor='left', fullscreen=False)
input_manager = InputManager()
update_manager = UpdateManager()

print("   > Managers created")

# ===== CREATING SCENE (depends on managers) =====
scene_setup = SceneSetup(
    init_position=(1.5, -1, -2),
    init_rotation_x=21,
    init_rotation_y=-35,
    color_manager=color_manager,
    input_manager=input_manager,
    update_manager=update_manager
)

print("\nScene created")

# ===== CREATING ZOOM MANAGER =====
zoom_manager = ZoomManager(scene_setup, color_manager=color_manager)

# Register frame entities in ZoomManager (frame lives inside scene_setup)
scene_setup.register_frame_in_zoom(zoom_manager)

print("   > Zoom Manager created")

# ===== CREATING SCALABLE FLOOR =====
floor = ScalableFloor(
    model='quad',
    scale=40,
    rotation_x=90,
    color=color_manager.get_color('scene', 'floor'),
    texture='white_cube',
    texture_scale=(40, 40)
)
zoom_manager.register_object(floor, name='floor')

print("   > Floor created")

# ===== CREATING OBJECT MANAGER =====
object_manager = ObjectManager(zoom_manager)

# ===== CREATING GAME OBJECTS =====
my_object_1 = object_manager.create(MyObject, 'my_object', radius=1.5, speed=1.0, color_value=color.yellow)

# ===== KEY BINDINGS =====
object_manager.bind(my_object_1.decrease_speed, trigger=lambda key: key == '1' and not scene_setup.input_frozen)
object_manager.bind(my_object_1.increase_speed, trigger=lambda key: key == '2' and not scene_setup.input_frozen)

print("   > MyObject created (moving sphere)")

# ===== REGISTERING COMPONENTS IN MANAGERS =====
input_manager.register_scene_setup(scene_setup)
input_manager.register_zoom_manager(zoom_manager)
input_manager.register_window_manager(window_manager)
input_manager.register_object_manager(object_manager)

update_manager.register_input_manager(input_manager)
update_manager.register_scene_setup(scene_setup)
update_manager.register_zoom_manager(zoom_manager)
update_manager.register_object_manager(object_manager)

print("   > Components registered in managers")

# ===== UPDATE FUNCTIONS =====
def update():
    """Global update handler."""
    import time  # ursina replaces built-in time with its own module providing time.dt
    update_manager.update_all(time.dt)

def input(key):
    """Global input handler."""
    # All processing is delegated to InputManager
    input_manager.handle_input(key)

# ===== READY TO START =====
print("\nPlayer Zoom ready!")
print("\nAVAILABLE COMMANDS:")
print("   MOVEMENT: WASD, Space/Shift, Mouse")
print("   CURSOR: Alt (lock/unlock)")
print("   EXIT: Escape")
print("   ZOOM: Q (out), E (in), R (reset)")
print("   MY OBJECT SPEED: 1 (slower), 2 (faster)")
print("   FULLSCREEN: F11")
print("   DEBUG: H (debug info)")
print("\n" + "=" * 50)
print("SIMULATION STARTED")
print("=" * 50)

# ===== RUN =====
if __name__ == '__main__':
    app.run()
