"""
DoubleIntegrator - 1D Double Integrator simulation
====================================================

1D double integrator (point mass on a line):
    state   = [x, x_dot]
    control = u  (scalar)

    x_ddot = u

Step is computed via exact analytical integration
(constant control over interval → exact solution for linear system).

JIT note:
    _step() is written for numba compatibility.
    To enable JIT:

        from numba import njit

        @njit
        def _step(state, u, dt):
            ...
"""

import numpy as np


def _step(state: np.ndarray, u: float, dt: float) -> np.ndarray:
    """
    Advance double integrator state by dt under constant control u.

    Exact solution:
        x_new     = x + x_dot*dt + 0.5*u*dt^2
        x_dot_new = x_dot + u*dt

    Args:
        state: [x, x_dot]
        u:     scalar control (acceleration)
        dt:    time step in seconds

    Returns:
        new state [x, x_dot]
    """
    x, x_dot = state[0], state[1]
    new = np.empty(2)
    new[0] = x + x_dot * dt + 0.5 * u * dt * dt
    new[1] = x_dot + u * dt
    return new


class DoubleIntegrator:
    """
    1D Double integrator simulation (point mass with scalar acceleration control).

    state:   [x, x_dot]
    control: u  (scalar, x_ddot = u)
    """

    def __init__(self, x: float = 0.0, x_dot: float = 0.0):
        self.state = np.array([x, x_dot], dtype=float)

    @property
    def x(self) -> float:
        return self.state[0]

    @property
    def x_dot(self) -> float:
        return self.state[1]

    def step(self, u: float, dt: float) -> np.ndarray:
        """Advance simulation by dt. Returns new state."""
        self.state = _step(self.state, float(u), dt)
        return self.state

    def reset(self, x: float = 0.0, x_dot: float = 0.0) -> None:
        """Reset state."""
        self.state[:] = [x, x_dot]

    def __repr__(self) -> str:
        return f"DoubleIntegrator(x={self.x:.3f}, x_dot={self.x_dot:.3f})"
