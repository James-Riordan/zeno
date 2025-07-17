from __future__ import annotations
import numpy as np

from zenoengine.core.operators.curvature import curvature_operator
from zenoengine.core.operators.torsion import torsion_operator
from zenoengine.core.operators.nonlinear import nonlinear_operator
from zenoengine.core.operators.entropy import entropy_operator

def symbolic_pgns_operator(
    psi: np.ndarray,
    dim: int,
    *,
    lambda_: float = 0.4,
    kappa: float = 0.9,
    beta: float = 0.3
) -> np.ndarray:
    """
    PGNS composite operator:
    d𝒜/dt = -i (ℛ[𝒜] + λ·𝒯[𝒜] + κ·|𝒜|²𝒜 + β·𝒮*[𝒜])

    Args:
        psi: field (real or complex)
        dim: spatial dimension (1–3)
        lambda_: torsion strength
        kappa: nonlinearity strength
        beta: entropy feedback strength

    Returns:
        Δ𝒜: symbolic evolution term
    """
    R = curvature_operator(psi, dim)
    T = torsion_operator(psi, dim)
    N = nonlinear_operator(psi)
    S = entropy_operator(psi, dim)

    return -1j * (R + lambda_ * T + kappa * N + beta * S)
