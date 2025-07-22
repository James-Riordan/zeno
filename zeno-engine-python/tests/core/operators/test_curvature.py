import numpy as np
from zenoengine.core.operators.curvature import curvature_operator

def test_curvature_1d():
    values = np.ones(10)
    result = curvature_operator(values, dim=1)
    assert result.shape == values.shape
    assert np.allclose(result, result[0])  # uniform input = uniform output


def test_curvature_2d():
    values = np.ones((5, 5))
    result = curvature_operator(values, dim=2)
    assert result.shape == values.shape
    assert np.allclose(result, result[0, 0])


def test_curvature_invalid_dim():
    values = np.ones((2, 2, 2, 2))
    try:
        curvature_operator(values, dim=4)
        assert False, "Expected ValueError for unsupported dim"
    except ValueError:
        pass
