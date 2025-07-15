from __future__ import annotations
import numpy as np

def laplacian_nd(array: np.ndarray, dimension: int) -> np.ndarray:
    """
    Compute a discrete Laplacian using finite differences.
    Assumes periodic boundary conditions (wrap-around).
    Works for 1D, 2D, or 3D arrays.
    """
    result = -2 * dimension * array
    for axis in range(dimension):
        result += np.roll(array, shift=+1, axis=axis)
        result += np.roll(array, shift=-1, axis=axis)
    return result
