from __future__ import annotations
import numpy as np
from numba import njit

@njit(parallel=True)
def compute_laplacian_nd(array: np.ndarray, dim: int) -> np.ndarray:
    """
    Periodic-boundary N-dimensional Laplacian:
    ∇²psi ≈ sum over neighbors - 2d * center
    """
    result = -2 * dim * array.copy()
    for axis in range(dim):
        result += np.roll(array, 1, axis=axis)
        result += np.roll(array, -1, axis=axis)
    return result
