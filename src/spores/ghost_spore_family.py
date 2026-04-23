"""
GhostSporeFamily - Grid of ghost spores via recursive double integrator evolution
==================================================================================

Grid: i=1..n_tau (generations/time), j=-n_u..n_u (control values)

Evolution:
  state(0, j) = root (ghost_spore_0) for all j
  state(i, j) = di.step(state(i-1, j), u_j, delta_tau)

  delta_tau = tau / n_tau
  u_j       = (j / n_u) * a_max

Graph edges (drawn later):
  time:    (i,j) -- (i+1,j)
  control: (i,j-1) -- (i,j) -- (i,j+1)

Rebuild (new Entity objects): only when n_tau or n_u changes.
Recompute positions: every tick (cursor move, tau, a_max changes).
"""

import numpy as np
from typing import Dict, Tuple, TYPE_CHECKING
from .spore import GhostSpore
from ..math.double_integrator import DoubleIntegrator

if TYPE_CHECKING:
    from ..core.shared_context import SharedContext
    from .spore_manager import SporeManager


class GhostSporeFamily:

    def __init__(self, root: GhostSpore, spore_manager: "SporeManager", ctx: "SharedContext"):
        self._root = root
        self._spore_manager = spore_manager
        self._ctx = ctx
        self._di = DoubleIntegrator(ctx)
        self._nodes: Dict[Tuple[int, int], GhostSpore] = {}
        self._n_tau: int = -1
        self._n_u: int = -1
        self._generation: int = 0
        self._build()

    def _build(self) -> None:
        for spore in self._nodes.values():
            spore.enabled = False
        self._nodes.clear()

        pm = self._ctx.param_manager
        n_tau = int(pm.n_tau)
        n_u = int(pm.n_u)
        self._n_tau = n_tau
        self._n_u = n_u

        for i in range(1, n_tau + 1):
            for j in range(-n_u, n_u + 1):
                name = f'family_g{self._generation}_{i}_{j}'
                spore = self._spore_manager.create(GhostSpore, name)
                spore.alpha = 0.4
                self._nodes[(i, j)] = spore

        self._generation += 1
        print(f"[GhostSporeFamily] Built {n_tau}x{2*n_u+1} grid (gen {self._generation})")

    def _recompute(self) -> None:
        self._di.tick()
        pm = self._ctx.param_manager
        n_tau = self._n_tau
        n_u = self._n_u
        a_max = self._di.a_max
        tau = pm.tau
        dt = tau / n_tau if n_tau > 0 else tau

        root_pos = self._root.real_position  # [x, y_offset, v]

        for i in range(1, n_tau + 1):
            for j in range(-n_u, n_u + 1):
                u_j = (j / n_u) * a_max if n_u > 0 else 0.0
                parent_pos = root_pos if i == 1 else self._nodes[(i - 1, j)].real_position
                s = self._di.step(x0=parent_pos[0], v0=parent_pos[2], u=u_j, t=dt)
                self._nodes[(i, j)].real_position = np.array([s[0], 0.01, s[1]])

    def tick(self) -> None:
        pm = self._ctx.param_manager
        n_tau = int(pm.n_tau)
        n_u = int(pm.n_u)

        if n_tau != self._n_tau or n_u != self._n_u:
            self._build()

        if n_tau == 0:
            return

        self._recompute()
