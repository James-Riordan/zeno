from __future__ import annotations
import numpy as np
from numba import njit

@njit
def entropy_operator(values: np.ndarray, dim: int) -> np.ndarray:
    """
    Symbolic entropy curvature operator 𝒮*[𝒜].

    Computes -‖∇𝒜‖ · 𝒜 using discrete gradients along each axis.
    Assumes periodic boundary conditions.

    Arguments:
        values: ndarray of shape (...), real or complex
        dim: int (1, 2, or 3)

    Returns:
        entropy_force: ndarray of same shape as `values`
    """
    grad_squared = np.zeros_like(values)

    for axis in range(dim):
        forward = np.roll(values, -1, axis=axis)
        backward = np.roll(values, 1, axis=axis)
        grad = 0.5 * (forward - backward)
        grad_squared += grad**2

    grad_mag = np.sqrt(grad_squared)
    return -grad_mag * values
