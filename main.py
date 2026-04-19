"""
PLAYER ZOOM - Camera and Zoom Sandbox
======================================

Controls:
- WASD: movement
- Mouse: look around
- Space/Shift: up/down
- Alt: release/capture cursor
- Escape: exit
- Q/E: zoom out/in
- R: reset zoom
- F11: fullscreen mode
- U: toggle frame visibility
- H: debug info
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np

from ursina import Ursina, Entity, color
from ursina.models.procedural.circle import Circle


from src.scene_setup import SceneSetup
from src.zoom_manager import ZoomManager
from src.window_manager import WindowManager
from src.color_manager import ColorManager
from src.scalable import ScalableFloor
from src.input_manager import InputManager
from src.update_manager import UpdateManager
from src.object_manager import ObjectManager
from src.screen_manager import ScreenManager, Message
from src.spore import Spore, GhostSpore
from src.spore_manager import SporeManager
from src.shared_context import SharedContext
from src.tau_manager import TauManager

print("=" * 50)
print("PLAYER ZOOM - Sandbox")
print("=" * 50)

app = Ursina()

# ===== MANAGERS =====
color_manager = ColorManager()
window_manager = WindowManager(monitor='main', fullscreen=False)
input_manager = InputManager()
update_manager = UpdateManager()

# ===== SCENE =====
scene_setup = SceneSetup(
    init_position=(1.5, -1, -2),
    init_rotation_x=21,
    init_rotation_y=-35,
    color_manager=color_manager,
    input_manager=input_manager,
    update_manager=update_manager
)

zoom_manager = ZoomManager(scene_setup, color_manager=color_manager)
scene_setup.register_frame_in_zoom(zoom_manager)

floor = ScalableFloor(
    model='quad',
    scale=40,
    rotation_x=90,
    color=color_manager.get_color('scene', 'floor'),
    texture='white_cube',
    texture_scale=(40, 40)
)
zoom_manager.register_object(floor, name='floor')

# ===== SHARED CONTEXT =====
shared_context = SharedContext()
shared_context.bind('look_point', lambda: zoom_manager.real_look_point, default=np.zeros(2))


# ===== TAU MANAGER =====
tau_manager = TauManager(initial=0.5)
shared_context.bind('tau', lambda: tau_manager.tau, default=tau_manager.tau)

# ===== OBJECT MANAGER =====
object_manager = ObjectManager(zoom_manager)

spore_manager = SporeManager(zoom_manager)
object_manager.register_spore_manager(spore_manager)


# ===== SCREEN MANAGER =====
screen_manager = ScreenManager()

screen_manager.add_message(Message(
    name='look_point',
    position=(-0.79, 0.48),
    offset=(0.0, 0.0),
    getter=lambda: f"Look: [{shared_context.look_point[0]:5.2f} {shared_context.look_point[1]:5.2f}]"
))

screen_manager.add_message(Message(
    name='tau',
    position=(-0.79, 0.46),
    offset=(0.0, 0.0),
    getter=lambda: f"Tau:  {shared_context.tau:5.3f}"
))




object_manager.create(cls=Spore, name='spore', position=(1, 1))
object_manager.create(cls=GhostSpore, name='ghost_spore_0', ctx=shared_context)
spore_manager.get('ghost_spore_0').color = color.white
spore_manager.get('ghost_spore_0').alpha = 0.5

a_max = 1/2
object_manager.create(cls=GhostSpore, name='ghost_spore_1', ctx=shared_context)
spore_manager.get('ghost_spore_1').tick = lambda: setattr(spore_manager.get('ghost_spore_1'), 'real_position', spore_manager.get('ghost_spore_0').real_position + shared_context.tau * np.array([spore_manager.get('ghost_spore_0').real_position[2], 0, -a_max]))

object_manager.create(cls=GhostSpore, name='ghost_spore_2', ctx=shared_context)
spore_manager.get('ghost_spore_2').tick = lambda: setattr(spore_manager.get('ghost_spore_2'), 'real_position', spore_manager.get('ghost_spore_0').real_position + shared_context.tau * np.array([spore_manager.get('ghost_spore_0').real_position[2], 0, +a_max]))
spore_manager.get('ghost_spore_2').color = color.red
spore_manager.get('ghost_spore_2').alpha = 0.5




object_manager.bind(tau_manager.decrease, trigger=lambda key: key == '1', key='1', description='decrease tau')
object_manager.bind(tau_manager.increase, trigger=lambda key: key == '2', key='2', description='increase tau')
object_manager.bind(spore_manager.decrease_size, trigger=lambda key: key == '3', key='3', description='decrease spore size')
object_manager.bind(spore_manager.increase_size, trigger=lambda key: key == '4', key='4', description='increase spore size')

screen_manager.add_bindings_help(object_manager, position=(-0.79, 0.35))






# ===== REGISTER COMPONENTS =====
input_manager.register_scene_setup(scene_setup)
input_manager.register_zoom_manager(zoom_manager)
input_manager.register_window_manager(window_manager)
input_manager.register_object_manager(object_manager)

update_manager.register_input_manager(input_manager)
update_manager.register_scene_setup(scene_setup)
update_manager.register_zoom_manager(zoom_manager)
update_manager.register_object_manager(object_manager)
update_manager.register_screen_manager(screen_manager)
update_manager.register_shared_context(shared_context)

# ===== LOOP =====
def update():
    import time  # ursina replaces built-in time with its own module providing time.dt
    update_manager.update_all(time.dt)

def input(key):
    input_manager.handle_input(key)

print("Ready. WASD to move, Q/E zoom, Alt cursor, Esc exit.")
print("=" * 50)

if __name__ == '__main__':
    app.run()
