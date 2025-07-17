from __future__ import annotations
import numpy as np
from numba import njit, prange

from zenoengine.fields.field import SymbolicField
from zenoengine.core.partition_geometry import partition_table

# Optional: exposed for metrics/debug export
cached_last_curvature = np.zeros((1,), dtype=np.float64)
cached_last_torsion = np.zeros((1,), dtype=np.float64)


def symbolic_pgns_operator(field: SymbolicField) -> np.ndarray:
    """
    Composite PGNS operator:
    ℛ[𝒜] + 𝒯[𝒜] from partition geometry.

    Uses cached curvature/torsion values for export.
    """
    psi = field.values
    shape = psi.shape
    dim = field.config.dimension

    p_table = partition_table(500)

    result = np.zeros_like(psi)
    curvature = np.zeros_like(psi)
    torsion = np.zeros_like(psi)

    if dim == 1:
        _kernel_1d(psi, result, curvature, torsion, p_table, shape[0])
    elif dim == 2:
        _kernel_2d(psi, result, curvature, torsion, p_table, shape[0], shape[1])
    elif dim == 3:
        _kernel_3d(psi, result, curvature, torsion, p_table, shape[0], shape[1], shape[2])
    else:
        raise ValueError("PGNS operator only supports dim = 1, 2, or 3")

    global cached_last_curvature, cached_last_torsion
    cached_last_curvature = curvature
    cached_last_torsion = torsion

    return result


@njit(parallel=True)
def _kernel_1d(psi, result, R, T, p_table, nx):
    for i in prange(nx):
        center = psi[i]
        left = psi[(i - 1) % nx]
        right = psi[(i + 1) % nx]

        c = min(int(abs(center) * 50), 499)
        l = min(int(abs(left) * 50), 499)
        r = min(int(abs(right) * 50), 499)

        R[i] = 2 * p_table[c] - p_table[l] - p_table[r]
        T[i] = p_table[r] - p_table[l]
        result[i] = R[i] + T[i]


@njit(parallel=True)
def _kernel_2d(psi, result, R, T, p_table, nx, ny):
    for i in prange(nx):
        for j in range(ny):
            center = psi[i, j]
            c = min(int(abs(center) * 50), 499)

            neighbors = [
                psi[(i - 1) % nx, j],
                psi[(i + 1) % nx, j],
                psi[i, (j - 1) % ny],
                psi[i, (j + 1) % ny],
            ]

            R_val = 0.0
            for n in neighbors:
                R_val += p_table[c] - p_table[min(int(abs(n) * 50), 499)]
            R[i, j] = R_val

            l = min(int(abs(psi[(i - 1) % nx, j]) * 50), 499)
            r = min(int(abs(psi[(i + 1) % nx, j]) * 50), 499)
            u = min(int(abs(psi[i, (j + 1) % ny]) * 50), 499)
            d = min(int(abs(psi[i, (j - 1) % ny]) * 50), 499)

            T_val = (p_table[r] - p_table[l]) + (p_table[u] - p_table[d])
            T[i, j] = T_val

            result[i, j] = R_val + T_val


@njit(parallel=True)
def _kernel_3d(psi, result, R, T, p_table, nx, ny, nz):
    for i in prange(nx):
        for j in range(ny):
            for k in range(nz):
                center = psi[i, j, k]
                c = min(int(abs(center) * 50), 499)

                neighbors = [
                    psi[(i - 1) % nx, j, k],
                    psi[(i + 1) % nx, j, k],
                    psi[i, (j - 1) % ny, k],
                    psi[i, (j + 1) % ny, k],
                    psi[i, j, (k - 1) % nz],
                    psi[i, j, (k + 1) % nz],
                ]

                R_val = 0.0
                for n in neighbors:
                    R_val += p_table[c] - p_table[min(int(abs(n) * 50), 499)]
                R[i, j, k] = R_val

                T_val = (
                    p_table[min(int(abs(psi[(i + 1) % nx, j, k]) * 50), 499)]
                    - p_table[min(int(abs(psi[(i - 1) % nx, j, k]) * 50), 499)]
                    + p_table[min(int(abs(psi[i, (j + 1) % ny, k]) * 50), 499)]
                    - p_table[min(int(abs(psi[i, (j - 1) % ny, k]) * 50), 499)]
                    + p_table[min(int(abs(psi[i, j, (k + 1) % nz]) * 50), 499)]
                    - p_table[min(int(abs(psi[i, j, (k - 1) % nz]) * 50), 499)]
                )
                T[i, j, k] = T_val
                result[i, j, k] = R_val + T_val
