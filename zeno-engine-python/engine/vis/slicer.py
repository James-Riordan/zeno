from __future__ import annotations
import numpy as np


def central_slice(field: np.ndarray) -> np.ndarray:
    """
    For 3D+ tensors, extract the central 2D slice for visualization.
    For 2D, returns as-is. For 1D, expands to 2D line display.
    """
    dim = field.ndim
    if dim == 3:
        center = field.shape[0] // 2
        return field[center, :, :]
    elif dim == 2:
        return field
    elif dim == 1:
        return np.expand_dims(field, axis=0)
    else:
        raise ValueError("Unsupported tensor dimension for slicing")
