from __future__ import annotations
import numpy as np
from numba import njit

@njit
def nonlinear_operator(values: np.ndarray) -> np.ndarray:
    """
    Symbolic self-focusing / nonlinear term: |𝒜|² · 𝒜

    This term models harmonic focusing like a symbolic Kerr effect.
    (symbolic analog of cubic nonlinearity)

    Args:
        values: input psi field

    Returns:
        |𝒜|² · 𝒜 term
    """
    return np.abs(values)**2 * values
