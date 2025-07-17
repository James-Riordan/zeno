from __future__ import annotations
import numpy as np
from numba import njit

@njit
def torsion_operator(values: np.ndarray, dim: int) -> np.ndarray:
    """
    Symbolic torsion operator 𝒯[𝒜].

    Approximates twist or antisymmetric rotation via discrete differences.

    In 1D: zero.
    In 2D: ∂xA_y - ∂yA_x (approx antisymmetric curl).
    In 3D: ∇ ∧ 𝒜 (approximated via cross-derivatives).

    Args:
        values: ndarray of psi/𝒜
        dim: 1, 2, or 3

    Returns:
        torsion field: np.ndarray of same shape
    """
    torsion = np.zeros_like(values)

    if dim == 1:
        return torsion

    elif dim == 2:
        dx = np.roll(values, -1, axis=0) - np.roll(values, 1, axis=0)
        dy = np.roll(values, -1, axis=1) - np.roll(values, 1, axis=1)
        torsion = dx - dy

    elif dim == 3:
        dx = np.roll(values, -1, axis=0) - np.roll(values, 1, axis=0)
        dy = np.roll(values, -1, axis=1) - np.roll(values, 1, axis=1)
        dz = np.roll(values, -1, axis=2) - np.roll(values, 1, axis=2)
        torsion = dx + dy - dz  # placeholder, upgrade to ∇∧𝒜 later

    return torsion
