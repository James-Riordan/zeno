from __future__ import annotations
import numpy as np
from numba import njit
from zeno.fields.field import SymbolicField

@njit(parallel=True)
def classical_laplacian_nd(psi: np.ndarray, dim: int) -> np.ndarray:
    """
    Fast Numba-accelerated N-dimensional Laplacian using periodic BCs.
    ∇²ψ ≈ sum over neighbors - 2d * center
    """
    result = -2 * dim * psi.copy()
    for axis in range(dim):
        result += np.roll(psi, 1, axis=axis)
        result += np.roll(psi, -1, axis=axis)
    return result

def classical_diffusion_operator(field: SymbolicField) -> np.ndarray:
    """
    Classical Laplacian-based diffusion operator: ∂ψ/∂t = ∇²ψ
    """
    return classical_laplacian_nd(field.values, field.config.dimension)
