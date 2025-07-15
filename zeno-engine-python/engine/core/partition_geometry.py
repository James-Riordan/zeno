from __future__ import annotations
import numpy as np
from functools import lru_cache


@lru_cache(maxsize=2048)
def partition(n: int) -> int:
    """
    Ramanujan’s symbolic partition function p(n), using Euler's recurrence.
    Used in symbolic PGNS (slow but flexible).
    """
    if n < 0:
        return 0
    if n == 0:
        return 1

    total = 0
    k = 1
    while True:
        pent1 = k * (3 * k - 1) // 2
        pent2 = k * (3 * k + 1) // 2
        if pent1 > n:
            break
        sign = -1 if (k % 2 == 0) else 1
        total += sign * partition(n - pent1)
        if pent2 <= n:
            total += sign * partition(n - pent2)
        k += 1
    return total


def partition_table(max_n: int = 500) -> np.ndarray:
    """
    Generate partition values p(0) to p(max_n) using iterative recurrence.
    Numba-friendly. Used in high-speed PGNS simulations.
    """
    p = np.zeros(max_n + 1, dtype=np.float64)
    p[0] = 1.0

    for k in range(1, max_n + 1):
        total = 0.0
        j = 1
        while True:
            pent1 = k - (j * (3 * j - 1)) // 2
            pent2 = k - (j * (3 * j + 1)) // 2
            if pent1 < 0 and pent2 < 0:
                break
            sign = -1 if (j % 2 == 0) else 1
            if pent1 >= 0:
                total += sign * p[pent1]
            if pent2 >= 0:
                total += sign * p[pent2]
            j += 1
        p[k] = total

    return p
