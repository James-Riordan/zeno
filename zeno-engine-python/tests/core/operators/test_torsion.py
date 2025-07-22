import numpy as np
from zenoengine.core.operators.torsion import torsion_operator


def test_torsion_1d():
    values = np.linspace(-1, 1, 10)
    result = torsion_operator(values, dim=1)
    assert result.shape == values.shape
    assert isinstance(result[0], float)


def test_torsion_2d():
    values = np.ones((4, 4)) * 0.5
    result = torsion_operator(values, dim=2)
    assert result.shape == values.shape
    assert np.allclose(result, result[0, 0])


def test_torsion_invalid_dim():
    values = np.ones((3, 3, 3, 3))
    try:
        torsion_operator(values, dim=4)
        assert False, "Expected ValueError for unsupported dim"
    except ValueError:
        pass
