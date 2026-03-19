"""
DiffDrive - Differential drive simulation
==========================================

Unicycle model:
    state   = [x, y, theta]
    control = [v, omega]

    dx/dt     = v * cos(theta)
    dy/dt     = v * sin(theta)
    dtheta/dt = omega

Step is computed via 4th-order Runge-Kutta.

JIT note:
    _derivative and _rk4_step are written for numba compatibility.
    To enable JIT, add to both functions:

        from numba import njit

        @njit
        def _derivative(...):
            ...

        @njit
        def _rk4_step(...):
            ...

    Also replace np.empty(3) initialization style if needed.
"""

import math
import numpy as np


def _derivative(state: np.ndarray, control: np.ndarray) -> np.ndarray:
    """
    Compute state derivative for unicycle model.

    Args:
        state:   [x, y, theta]
        control: [v, omega]

    Returns:
        [dx/dt, dy/dt, dtheta/dt]
    """
    v     = control[0]
    omega = control[1]
    theta = state[2]

    dot = np.empty(3)
    dot[0] = v * math.cos(theta)
    dot[1] = v * math.sin(theta)
    dot[2] = omega
    return dot


def _rk4_step(state: np.ndarray, control: np.ndarray, dt: float) -> np.ndarray:
    """
    Advance state by dt using 4th-order Runge-Kutta.

    Args:
        state:   [x, y, theta]
        control: [v, omega]
        dt:      time step in seconds

    Returns:
        new state [x, y, theta]
    """
    k1 = _derivative(state,             control)
    k2 = _derivative(state + 0.5*dt*k1, control)
    k3 = _derivative(state + 0.5*dt*k2, control)
    k4 = _derivative(state +     dt*k3, control)
    return state + (dt / 6.0) * (k1 + 2.0*k2 + 2.0*k3 + k4)


class DiffDrive:
    """
    Differential drive robot simulation (unicycle model).

    state:   [x, y, theta]
    control: [v, omega]
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, theta: float = 0.0):
        self.state = np.array([x, y, theta], dtype=float)

    @property
    def x(self) -> float:
        return self.state[0]

    @property
    def y(self) -> float:
        return self.state[1]

    @property
    def theta(self) -> float:
        return self.state[2]

    def derivative(self, control: np.ndarray) -> np.ndarray:
        """Return state derivative for current state and given control."""
        return _derivative(self.state, control)

    def step(self, control: np.ndarray, dt: float) -> np.ndarray:
        """Advance simulation by dt. Returns new state."""
        self.state = _rk4_step(self.state, control, dt)
        return self.state

    def reset(self, x: float = 0.0, y: float = 0.0, theta: float = 0.0) -> None:
        """Reset state to given pose."""
        self.state[:] = [x, y, theta]

    def __repr__(self) -> str:
        return f"DiffDrive(x={self.x:.3f}, y={self.y:.3f}, theta={self.theta:.3f})"
