"""
Trajectories - Generate DiffDrive trajectories for all control patterns
========================================================================

Returns a list of trajectories. Each trajectory is a list of states [x, y, theta].
"""

import numpy as np
from itertools import permutations
from .math import DiffDrive


def _gen_taus(N, pattern_length, tau, seed=None):
    switch_num = pattern_length - 1  # внутренних точек переключения
    rng = np.random.default_rng(seed)
    mid = rng.uniform(0.0, tau, size=(N, switch_num))
    out = np.empty((N, switch_num + 2), dtype=float)
    out[:, 0] = 0.0
    out[:, 1:1 + switch_num] = mid
    out[:, -1] = float(tau)
    out = np.sort(out, axis=1)
    out = out[:, 1:] - out[:, :-1]
    return out


def _gen_patterns(length):
    controls = [
        np.array([ 0,  1]),
        np.array([ 0, -1]),
        np.array([ 1,  0]),
        np.array([-1,  0]),
    ]
    result = []
    for combo in permutations(controls, length):
        valid = all(not np.array_equal(combo[i], -combo[i + 1]) for i in range(length - 1))
        if valid:
            result.append(combo)
    return result


def generate_trajectories(start_state, pattern_length, tau, N, seed=None, pattern_index=None):
    """
    Generate trajectories for control patterns of given length.

    Args:
        start_state:    [x, y, theta]
        pattern_length: number of controls in each pattern
        tau:            total time per trajectory
        N:              number of random tau sets per pattern
        seed:           random seed
        pattern_index:  if given, use only that one pattern; otherwise use all patterns

    Returns:
        list of trajectories, each = list of np.array([x, y, theta])
    """
    all_patterns = _gen_patterns(pattern_length)
    patterns = [all_patterns[pattern_index]] if pattern_index is not None else all_patterns
    taus_list = _gen_taus(N=N, pattern_length=pattern_length, tau=tau, seed=seed)

    drive = DiffDrive()
    trajectories = []

    for pattern in patterns:
        for taus in taus_list:
            drive.reset(*start_state)
            states = [np.array(start_state, dtype=float)]
            for i, control in enumerate(pattern):
                next_state = drive.step(control, taus[i])
                states.append(next_state.copy())
            trajectories.append(states)

    return trajectories
