from __future__ import annotations
import numpy as np
from numba import njit
from zenoengine.core.partition_geometry import partition_table


@njit
def curvature_operator(values: np.ndarray, dim: int) -> np.ndarray:
    """
    Computes symbolic curvature ℛ[𝒜] from the field values using partition geometry.

    Args:
        values: ndarray of real values representing the field ψ or 𝒜.
        dim: Spatial dimension (1, 2, or 3).

    Returns:
        ndarray of the same shape as `values` containing the curvature.
    """
    shape = values.shape
    p_table = partition_table(500)
    result = np.zeros_like(values)

    if dim == 1:
        nx = shape[0]
        for i in range(nx):
            c = min(int(abs(values[i]) * 50), 499)
            l = min(int(abs(values[(i - 1) % nx]) * 50), 499)
            r = min(int(abs(values[(i + 1) % nx]) * 50), 499)
            result[i] = 2 * p_table[c] - p_table[l] - p_table[r]

    elif dim == 2:
        nx, ny = shape
        for i in range(nx):
            for j in range(ny):
                c = min(int(abs(values[i, j]) * 50), 499)
                neighbors = [
                    values[(i - 1) % nx, j],
                    values[(i + 1) % nx, j],
                    values[i, (j - 1) % ny],
                    values[i, (j + 1) % ny],
                ]
                result[i, j] = sum(
                    p_table[c] - p_table[min(int(abs(n) * 50), 499)]
                    for n in neighbors
                )

    elif dim == 3:
        nx, ny, nz = shape
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    c = min(int(abs(values[i, j, k]) * 50), 499)
                    neighbors = [
                        values[(i - 1) % nx, j, k],
                        values[(i + 1) % nx, j, k],
                        values[i, (j - 1) % ny, k],
                        values[i, (j + 1) % ny, k],
                        values[i, j, (k - 1) % nz],
                        values[i, j, (k + 1) % nz],
                    ]
                    result[i, j, k] = sum(
                        p_table[c] - p_table[min(int(abs(n) * 50), 499)]
                        for n in neighbors
                    )

    else:
        raise ValueError("Unsupported dimension for curvature_operator")

    return result
