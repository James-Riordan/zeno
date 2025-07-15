from concurrent.futures import ThreadPoolExecutor
import numpy as np
from typing import Callable, Optional

def parallel_nd_loop(
    shape: tuple[int, ...],
    fn: Callable[[tuple[int, ...]], None],
    max_workers: Optional[int] = None
) -> None:
    """
    Apply `fn(index)` across an N-dimensional array in parallel.
    Each index is a tuple (i, j, k, ...) over np.ndindex(shape).
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(fn, list(np.ndindex(shape)))
