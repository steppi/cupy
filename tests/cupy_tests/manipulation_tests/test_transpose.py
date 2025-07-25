from __future__ import annotations

import unittest

import numpy
import pytest

import cupy
from cupy import testing
from cupy.exceptions import AxisError


class TestTranspose(unittest.TestCase):

    @testing.numpy_cupy_array_equal()
    def test_moveaxis1(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.moveaxis(a, [0, 1], [1, 2])

    @testing.numpy_cupy_array_equal()
    def test_moveaxis2(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.moveaxis(a, 1, -1)

    @testing.numpy_cupy_array_equal()
    def test_moveaxis3(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.moveaxis(a, [0, 2], [1, 0])

    @testing.numpy_cupy_array_equal()
    def test_moveaxis4(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.moveaxis(a, [2, 0], [1, 0])

    @testing.numpy_cupy_array_equal()
    def test_moveaxis5(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.moveaxis(a, [2, 0], [0, 1])

    @testing.numpy_cupy_array_equal()
    def test_moveaxis6(self, xp):
        a = testing.shaped_arange((2, 3, 4, 5, 6), xp)
        return xp.moveaxis(a, [0, 2, 1], [3, 4, 0])

    # dim is too large
    def test_moveaxis_invalid1_1(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(AxisError):
                xp.moveaxis(a, [0, 1], [1, 3])

    def test_moveaxis_invalid1_2(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(AxisError):
                xp.moveaxis(a, [0, 1], [1, 3])

    def test_moveaxis_invalid1_3(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(AxisError):
                xp.moveaxis(a, 0, 3)

    # dim is too small
    def test_moveaxis_invalid2_1(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(AxisError):
                xp.moveaxis(a, [0, -4], [1, 2])

    def test_moveaxis_invalid2_2(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(AxisError):
                xp.moveaxis(a, [0, -4], [1, 2])

    def test_moveaxis_invalid2_3(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(AxisError):
                xp.moveaxis(a, -4, 0)

    # len(source) != len(destination)
    def test_moveaxis_invalid3_1(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.moveaxis(a, [0, 1, 2], [1, 2])

    def test_moveaxis_invalid3_2(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.moveaxis(a, 0, [1, 2])

    # len(source) != len(destination)
    def test_moveaxis_invalid4_1(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.moveaxis(a, [0, 1], [1, 2, 0])

    def test_moveaxis_invalid4_2(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.moveaxis(a, [0, 1], 1)

    # Use the same axis twice
    def test_moveaxis_invalid5_1(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(AxisError):
                xp.moveaxis(a, [1, -1], [1, 3])

    def test_moveaxis_invalid5_2(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.moveaxis(a, [0, 1], [-1, 2])

    def test_moveaxis_invalid5_3(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.moveaxis(a, [0, 1], [1, 1])

    @testing.numpy_cupy_array_equal()
    def test_rollaxis(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.rollaxis(a, 2)

    def test_rollaxis_failure(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.rollaxis(a, 3)

    @testing.numpy_cupy_array_equal()
    def test_swapaxes(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.swapaxes(a, 2, 0)

    def test_swapaxes_failure(self):
        for xp in (numpy, cupy):
            a = testing.shaped_arange((2, 3, 4), xp)
            with pytest.raises(ValueError):
                xp.swapaxes(a, 3, 0)

    @testing.numpy_cupy_array_equal()
    def test_transpose(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return a.transpose(-1, 0, 1)

    @testing.numpy_cupy_array_equal()
    def test_transpose_empty(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return a.transpose()

    @testing.numpy_cupy_array_equal()
    def test_transpose_none(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return a.transpose(None)

    @testing.numpy_cupy_array_equal()
    def test_external_transpose(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.transpose(a, (-1, 0, 1))

    @testing.numpy_cupy_array_equal()
    def test_external_transpose_all(self, xp):
        a = testing.shaped_arange((2, 3, 4), xp)
        return xp.transpose(a)


ARRAY_SHAPES_TO_TEST = (
    (5, 2),
    (5, 2, 3),
    (5, 2, 3, 4),
)


class TestMatrixTranspose:

    @testing.with_requires('numpy>=2.0')
    def test_matrix_transpose_raises_error_for_1d(self):
        msg = "matrix transpose with ndim < 2 is undefined"
        arr = cupy.arange(48)
        with pytest.raises(ValueError, match=msg):
            arr.mT

    @testing.numpy_cupy_array_equal()
    def test_matrix_transpose_equals_transpose_2d(self, xp):
        arr = xp.arange(48).reshape((6, 8))
        return arr

    @testing.with_requires('numpy>=2.0')
    @pytest.mark.parametrize("shape", ARRAY_SHAPES_TO_TEST)
    @testing.numpy_cupy_array_equal()
    def test_matrix_transpose_equals_swapaxes(self, xp, shape):
        vec = xp.arange(shape[-1])
        arr = xp.broadcast_to(vec, shape)
        return arr.mT
