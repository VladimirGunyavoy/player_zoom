"""
TauManager - Simulation time step controller
=============================================

Stores tau — an independent simulation parameter (not Ursina's dt).
Keys 1/2 decrease/increase tau.
"""


class TauManager:

    def __init__(self, initial: float = 1.0, factor: float = 1.06,
                 min_tau: float = 0.0, max_tau: float = 5.0):
        self.factor = factor
        self.min_tau = min_tau
        self.max_tau = max_tau
        self.tau: float = initial

    def increase(self) -> None:
        self.tau = min(self.tau * self.factor, self.max_tau)
        print(f"[TauManager] tau: {self.tau:.3f}")

    def decrease(self) -> None:
        self.tau = max(self.tau / self.factor, self.min_tau)
        print(f"[TauManager] tau: {self.tau:.3f}")
