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

from ast import pattern
import sys
import os

# Add src path to PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ursina import Ursina, application, Entity, Mesh, Vec3
from src.scene_setup import SceneSetup
from src.zoom_manager import ZoomManager
from src.window_manager import WindowManager
from src.color_manager import ColorManager
from src.scalable import ScalableFloor, Scalable
from src.input_manager import InputManager
from src.update_manager import UpdateManager
from src.object_manager import ObjectManager
from src.my_object import MyObject
from src.spore import Spore
from src.spore_manager import SporeManager
from src.scalable_line import ScalableLine
from src.scalable_surface import ScalableSurface
from src.trajectories import generate_trajectories
import numpy as np
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
# my_object_1 = object_manager.create(MyObject, 'my_object', radius=1.5, speed=1.0, color_value=color.yellow)

# ===== TRAJECTORY VISUALIZATION =====
PATTERN_COLORS = [
    color.rgb(0.27, 0.80, 0.58),   # мятный
    color.rgb(0.94, 0.45, 0.45),   # коралловый
    color.rgb(0.40, 0.65, 0.95),   # голубой
    color.rgb(0.95, 0.78, 0.30),   # золотой
    color.rgb(0.72, 0.45, 0.95),   # лавандовый
    color.rgb(0.95, 0.55, 0.20),   # оранжевый
    color.rgb(0.40, 0.88, 0.82),   # бирюзовый
    color.rgb(0.90, 0.40, 0.70),   # розовый
]

PATTERN_INDICES = [0, 1, 2, 3, 4, 5, 6, 7]  # ← список паттернов для отображения

# PATTERN_INDICES = [0, 1, 2, 3, 4, 5] 
N = 50
tau = 1
pattern_length = 2


spore_manager = SporeManager(zoom_manager)

for pi, pattern_index in enumerate(PATTERN_INDICES):
    c = PATTERN_COLORS[pi % len(PATTERN_COLORS)]
    trajectories = generate_trajectories(
        start_state=[0.0, 0.0, 0.0],
        pattern_length=pattern_length,
        tau=tau,
        N=N,
        seed=41,
        pattern_index=pattern_index
    )
    # # ---- ПОДХОД 1: споры + линии ----
    # for i, traj in enumerate(trajectories):
    #     for j, state in enumerate(traj):
    #         x, y, theta = state
    #         spore = object_manager.create(Spore, f'spore_{pi}_{i}_{j}', pos=(x, theta, y), color_value=c)
    #         spore_manager.register(spore)
    #     for k in range(len(traj) - 1):
    #         p1 = (traj[k][0], traj[k][2], traj[k][1])
    #         p2 = (traj[k+1][0], traj[k+1][2], traj[k+1][1])
    #         line = ScalableLine(p1, p2, color=c, thickness=5)
    #         zoom_manager.register_object(line, name=f'line_{pi}_{i}_{k}')

    # Сортируем траектории по углу конечной точки (веер), чтобы соседние в mesh были соседними пространственно
    trajectories.sort(key=lambda traj: np.arctan2(traj[-1][1], traj[-1][0]))

    # ---- ПОДХОД 2: полупрозрачная поверхность ----
    grid = [[(s[0], s[2], s[1]) for s in traj] for traj in trajectories]
    surface = ScalableSurface(grid, color=c, alpha=0.5, double_sided=True)
    zoom_manager.register_object(surface, name=f'surface_{pi}')

    # ---- ПОДХОД 3: скелет (wireframe сетка точек) ----
    grid = [[(s[0], s[2], s[1]) for s in traj] for traj in trajectories]
    skeleton = ScalableSurface(grid, wireframe=True, color=color.black)
    skeleton.setDepthOffset(1)
    zoom_manager.register_object(skeleton, name=f'skeleton_{pi}')


# ===== KEY BINDINGS =====
# object_manager.bind(my_object_1.decrease_speed, trigger=lambda key: key == '1' and not scene_setup.input_frozen)
# object_manager.bind(my_object_1.increase_speed, trigger=lambda key: key == '2' and not scene_setup.input_frozen)
object_manager.bind(spore_manager.decrease_size, trigger=lambda key: key == '3' and not scene_setup.input_frozen)
object_manager.bind(spore_manager.increase_size, trigger=lambda key: key == '4' and not scene_setup.input_frozen)

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
