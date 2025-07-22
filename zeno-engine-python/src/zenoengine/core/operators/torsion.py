from __future__ import annotations
import numpy as np
from numba import njit
from zenoengine.core.partition_geometry import partition_table


@njit
def torsion_operator(values: np.ndarray, dim: int) -> np.ndarray:
    """
    Computes symbolic torsion 𝒯[𝒜] from the field values using partition geometry.

    Torsion is defined as the directional gradient using partition-weighted symbolic differences.

    Args:
        values: ndarray of real values representing the field ψ or 𝒜.
        dim: Spatial dimension (1, 2, or 3).

    Returns:
        ndarray of the same shape as `values` containing the torsion values.
    """
    shape = values.shape
    p_table = partition_table(500)
    result = np.zeros_like(values)

    if dim == 1:
        nx = shape[0]
        for i in range(nx):
            l = min(int(abs(values[(i - 1) % nx]) * 50), 499)
            r = min(int(abs(values[(i + 1) % nx]) * 50), 499)
            result[i] = p_table[r] - p_table[l]

    elif dim == 2:
        nx, ny = shape
        for i in range(nx):
            for j in range(ny):
                l = min(int(abs(values[(i - 1) % nx, j]) * 50), 499)
                r = min(int(abs(values[(i + 1) % nx, j]) * 50), 499)
                d = min(int(abs(values[i, (j - 1) % ny]) * 50), 499)
                u = min(int(abs(values[i, (j + 1) % ny]) * 50), 499)

                result[i, j] = (p_table[r] - p_table[l]) + (p_table[u] - p_table[d])

    elif dim == 3:
        nx, ny, nz = shape
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    l = min(int(abs(values[(i - 1) % nx, j, k]) * 50), 499)
                    r = min(int(abs(values[(i + 1) % nx, j, k]) * 50), 499)
                    d = min(int(abs(values[i, (j - 1) % ny, k]) * 50), 499)
                    u = min(int(abs(values[i, (j + 1) % ny, k]) * 50), 499)
                    b = min(int(abs(values[i, j, (k - 1) % nz]) * 50), 499)
                    f = min(int(abs(values[i, j, (k + 1) % nz]) * 50), 499)

                    result[i, j, k] = (
                        (p_table[r] - p_table[l])
                        + (p_table[u] - p_table[d])
                        + (p_table[f] - p_table[b])
                    )

    else:
        raise ValueError("Unsupported dimension for torsion_operator")

    return result
