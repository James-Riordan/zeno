from __future__ import annotations
import numpy as np
from numba import njit, prange
from zenoengine.fields.field import SymbolicField
from zenoengine.core.partition_geometry import partition_table

# Cached curvature and torsion tensors for metrics/export
cached_last_curvature = np.zeros((1,), dtype=np.float64)
cached_last_torsion = np.zeros((1,), dtype=np.float64)

def symbolic_pgns_operator(field: SymbolicField) -> np.ndarray:
    psi = field.values
    shape = psi.shape
    dim = field.config.dimension

    p_table = partition_table(500)

    result = np.zeros_like(psi)
    curvature = np.zeros_like(psi)
    torsion = np.zeros_like(psi)

    if dim == 1:
        _pgns_kernel_1d(psi, result, curvature, torsion, p_table, shape[0])
    elif dim == 2:
        _pgns_kernel_2d(psi, result, curvature, torsion, p_table, shape[0], shape[1])
    elif dim == 3:
        _pgns_kernel_3d(psi, result, curvature, torsion, p_table, shape[0], shape[1], shape[2])
    else:
        raise ValueError("Unsupported PGNS dimension")

    global cached_last_curvature, cached_last_torsion
    cached_last_curvature = curvature
    cached_last_torsion = torsion

    return result

@njit(parallel=True)
def _pgns_kernel_1d(psi, result, curv, tors, p_table, nx):
    for i in prange(nx):
        center = psi[i]
        left = psi[(i - 1) % nx]
        right = psi[(i + 1) % nx]

        c = min(int(abs(center) * 50), 499)
        l = min(int(abs(left) * 50), 499)
        r = min(int(abs(right) * 50), 499)

        R = 2 * p_table[c] - p_table[l] - p_table[r]
        T = p_table[r] - p_table[l]

        curv[i] = R
        tors[i] = T
        result[i] = R + T

@njit(parallel=True)
def _pgns_kernel_2d(psi, result, curv, tors, p_table, nx, ny):
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

            R = 0.0
            for n in neighbors:
                R += p_table[c] - p_table[min(int(abs(n) * 50), 499)]

            left = psi[(i - 1) % nx, j]
            right = psi[(i + 1) % nx, j]
            down = psi[i, (j - 1) % ny]
            up = psi[i, (j + 1) % ny]

            T = (
                p_table[min(int(abs(right) * 50), 499)] - p_table[min(int(abs(left) * 50), 499)]
                + p_table[min(int(abs(up) * 50), 499)] - p_table[min(int(abs(down) * 50), 499)]
            )

            curv[i, j] = R
            tors[i, j] = T
            result[i, j] = R + T

@njit(parallel=True)
def _pgns_kernel_3d(psi, result, curv, tors, p_table, nx, ny, nz):
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

                R = 0.0
                for n in neighbors:
                    R += p_table[c] - p_table[min(int(abs(n) * 50), 499)]

                T = (
                    p_table[min(int(abs(psi[(i + 1) % nx, j, k]) * 50), 499)]
                    - p_table[min(int(abs(psi[(i - 1) % nx, j, k]) * 50), 499)]
                    + p_table[min(int(abs(psi[i, (j + 1) % ny, k]) * 50), 499)]
                    - p_table[min(int(abs(psi[i, (j - 1) % ny, k]) * 50), 499)]
                    + p_table[min(int(abs(psi[i, j, (k + 1) % nz]) * 50), 499)]
                    - p_table[min(int(abs(psi[i, j, (k - 1) % nz]) * 50), 499)]
                )

                curv[i, j, k] = R
                tors[i, j, k] = T
                result[i, j, k] = R + T
