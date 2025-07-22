import numpy as np
import pytest
from zenoengine.core.operators.nonlinear import nonlinear_operator

def test_nonlinear_operator_real_values():
    x = np.array([1.0, 2.0, 3.0])
    expected = x**3
    output = nonlinear_operator(x)
    np.testing.assert_allclose(output, expected, rtol=1e-10)

def test_nonlinear_operator_complex_values():
    x = np.array([1 + 1j, 2 + 0j, 0 + 3j])
    expected = np.abs(x)**2 * x
    output = nonlinear_operator(x)
    np.testing.assert_allclose(output, expected, rtol=1e-10)

def test_nonlinear_operator_zeros():
    x = np.zeros(5)
    expected = np.zeros(5)
    output = nonlinear_operator(x)
    np.testing.assert_array_equal(output, expected)

def test_nonlinear_operator_random():
    np.random.seed(0)
    x = np.random.randn(10) + 1j * np.random.randn(10)
    expected = np.abs(x)**2 * x
    output = nonlinear_operator(x)
    np.testing.assert_allclose(output, expected, rtol=1e-10)
