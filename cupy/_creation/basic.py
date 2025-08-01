from __future__ import annotations

import math
from typing import Any

import numpy

import cupy
from cupy._core.internal import _get_strides_for_order_K, _update_order_char
from cupy.typing._types import (
    _OrderKACF, _OrderCF, _ShapeLike, DTypeLike, NDArray,
)


def empty(
        shape: _ShapeLike,
        dtype: DTypeLike = float,
        order: _OrderCF = 'C',
) -> NDArray[Any]:
    """Returns an array without initializing the elements.

    Args:
        shape (int or tuple of ints): Dimensionalities of the array.
        dtype (data-type, optional): Data type specifier.
        order ({'C', 'F'}): Row-major (C-style) or column-major
            (Fortran-style) order.

    Returns:
        cupy.ndarray: A new array with elements not initialized.

    .. seealso:: :func:`numpy.empty`

    """
    return cupy.ndarray(shape, dtype, order=order)


def _new_like_order_and_strides(
        a, dtype, order, shape=None, *, get_memptr=True):
    """
    Determine order and strides as in NumPy's PyArray_NewLikeArray.

    (see: numpy/core/src/multiarray/ctors.c)
    """
    order = order.upper()
    if order not in ['C', 'F', 'K', 'A']:
        raise ValueError('order not understood: {}'.format(order))

    if numpy.isscalar(shape):
        shape = (shape,)

    # Fallback to c_contiguous if keep order and number of dimensions
    # of new shape mismatch
    if order == 'K' and shape is not None and len(shape) != a.ndim:
        return 'C', None, None

    order = chr(_update_order_char(
        a.flags.c_contiguous, a.flags.f_contiguous, ord(order)))

    if order == 'K':
        strides = _get_strides_for_order_K(a, numpy.dtype(dtype), shape)
        order = 'C'
        size = math.prod(shape) if shape is not None else a.size
        memptr = cupy.empty(size, dtype=dtype).data if get_memptr else None
        return order, strides, memptr
    else:
        return order, None, None


def empty_like(
        prototype: NDArray[Any],
        dtype: DTypeLike = None,
        order: _OrderKACF = 'K',
        subok: None = None,
        shape: _ShapeLike | None = None,
) -> NDArray[Any]:
    """Returns a new array with same shape and dtype of a given array.

    This function currently does not support ``subok`` option.

    Args:
        a (cupy.ndarray): Base array.
        dtype (data-type, optional): Data type specifier.
            The data type of ``a`` is used by default.
        order ({'C', 'F', 'A', or 'K'}): Overrides the memory layout of the
            result. ``'C'`` means C-order, ``'F'`` means F-order, ``'A'`` means
            ``'F'`` if ``a`` is Fortran contiguous, ``'C'`` otherwise.
            ``'K'`` means match the layout of ``a`` as closely as possible.
        subok: Not supported yet, must be None.
        shape (int or tuple of ints): Overrides the shape of the result. If
            ``order='K'`` and the number of dimensions is unchanged, will try
            to keep order, otherwise, ``order='C'`` is implied.

    Returns:
        cupy.ndarray: A new array with same shape and dtype of ``a`` with
        elements not initialized.

    .. seealso:: :func:`numpy.empty_like`

    """
    if subok is not None:
        raise TypeError('subok is not supported yet')
    if dtype is None:
        dtype = prototype.dtype

    order, strides, memptr = _new_like_order_and_strides(
        prototype, dtype, order, shape)
    shape = shape if shape else prototype.shape
    return cupy.ndarray(shape, dtype, memptr, strides, order)


def eye(
        N: int,
        M: int | None = None,
        k: int = 0,
        dtype: DTypeLike = float,
        order: _OrderCF = 'C',
) -> NDArray[Any]:
    """Returns a 2-D array with ones on the diagonals and zeros elsewhere.

    Args:
        N (int): Number of rows.
        M (int): Number of columns. ``M == N`` by default.
        k (int): Index of the diagonal. Zero indicates the main diagonal,
            a positive index an upper diagonal, and a negative index a lower
            diagonal.
        dtype (data-type, optional): Data type specifier.
        order ({'C', 'F'}): Row-major (C-style) or column-major
            (Fortran-style) order.

    Returns:
        cupy.ndarray: A 2-D array with given diagonals filled with ones and
        zeros elsewhere.

    .. seealso:: :func:`numpy.eye`

    """
    if M is None:
        M = N
    ret = zeros((N, M), dtype=dtype, order=order)
    if k <= -N or k >= M:
        return ret
    ret.diagonal(k).fill(1)
    return ret


def identity(n: int, dtype: DTypeLike = float) -> NDArray[Any]:
    """Returns a 2-D identity array.

    It is equivalent to ``eye(n, n, dtype)``.

    Args:
        n (int): Number of rows and columns.
        dtype (data-type, optional): Data type specifier.

    Returns:
        cupy.ndarray: A 2-D identity array.

    .. seealso:: :func:`numpy.identity`

    """
    return eye(n, dtype=dtype)


def ones(
        shape: _ShapeLike,
        dtype: DTypeLike = float,
        order: _OrderCF = 'C',
) -> NDArray[Any]:
    """Returns a new array of given shape and dtype, filled with ones.

    This function currently does not support ``order`` option.

    Args:
        shape (int or tuple of ints): Dimensionalities of the array.
        dtype (data-type, optional): Data type specifier.
        order ({'C', 'F'}): Row-major (C-style) or column-major
            (Fortran-style) order.

    Returns:
        cupy.ndarray: An array filled with ones.

    .. seealso:: :func:`numpy.ones`

    """
    a = cupy.ndarray(shape, dtype, order=order)
    a.fill(1)
    return a


def ones_like(
        a: NDArray[Any],
        dtype: DTypeLike = None,
        order: _OrderKACF = 'K',
        subok: None = None,
        shape: _ShapeLike | None = None,
) -> NDArray[Any]:
    """Returns an array of ones with same shape and dtype as a given array.

    This function currently does not support ``subok`` option.

    Args:
        a (cupy.ndarray): Base array.
        dtype (data-type, optional): Data type specifier.
            The dtype of ``a`` is used by default.
        order ({'C', 'F', 'A', or 'K'}): Overrides the memory layout of the
            result. ``'C'`` means C-order, ``'F'`` means F-order, ``'A'`` means
            ``'F'`` if ``a`` is Fortran contiguous, ``'C'`` otherwise.
            ``'K'`` means match the layout of ``a`` as closely as possible.
        subok: Not supported yet, must be None.
        shape (int or tuple of ints): Overrides the shape of the result. If
            ``order='K'`` and the number of dimensions is unchanged, will try
            to keep order, otherwise, ``order='C'`` is implied.

    Returns:
        cupy.ndarray: An array filled with ones.

    .. seealso:: :func:`numpy.ones_like`

    """
    if subok is not None:
        raise TypeError('subok is not supported yet')
    if dtype is None:
        dtype = a.dtype

    order, strides, memptr = _new_like_order_and_strides(a, dtype, order,
                                                         shape)
    shape = shape if shape else a.shape
    a = cupy.ndarray(shape, dtype, memptr, strides, order)
    a.fill(1)
    return a


def zeros(
        shape: _ShapeLike,
        dtype: DTypeLike = float,
        order: _OrderCF = 'C',
) -> NDArray[Any]:
    """Returns a new array of given shape and dtype, filled with zeros.

    Args:
        shape (int or tuple of ints): Dimensionalities of the array.
        dtype (data-type, optional): Data type specifier.
        order ({'C', 'F'}): Row-major (C-style) or column-major
            (Fortran-style) order.

    Returns:
        cupy.ndarray: An array filled with zeros.

    .. seealso:: :func:`numpy.zeros`

    """
    a = cupy.ndarray(shape, dtype, order=order)
    a.data.memset_async(0, a.nbytes)
    return a


def zeros_like(
        a: NDArray[Any],
        dtype: DTypeLike = None,
        order: _OrderKACF = 'K',
        subok: None = None,
        shape: _ShapeLike | None = None,
) -> NDArray[Any]:
    """Returns an array of zeros with same shape and dtype as a given array.

    This function currently does not support ``subok`` option.

    Args:
        a (cupy.ndarray): Base array.
        dtype (data-type, optional): Data type specifier.
            The dtype of ``a`` is used by default.
        order ({'C', 'F', 'A', or 'K'}): Overrides the memory layout of the
            result. ``'C'`` means C-order, ``'F'`` means F-order, ``'A'`` means
            ``'F'`` if ``a`` is Fortran contiguous, ``'C'`` otherwise.
            ``'K'`` means match the layout of ``a`` as closely as possible.
        subok: Not supported yet, must be None.
        shape (int or tuple of ints): Overrides the shape of the result. If
            ``order='K'`` and the number of dimensions is unchanged, will try
            to keep order, otherwise, ``order='C'`` is implied.

    Returns:
        cupy.ndarray: An array filled with zeros.

    .. seealso:: :func:`numpy.zeros_like`

    """
    if subok is not None:
        raise TypeError('subok is not supported yet')
    if dtype is None:
        dtype = a.dtype

    order, strides, memptr = _new_like_order_and_strides(a, dtype, order,
                                                         shape)
    shape = shape if shape else a.shape
    a = cupy.ndarray(shape, dtype, memptr, strides, order)
    a.data.memset_async(0, a.nbytes)
    return a


def full(
        shape: _ShapeLike,
        fill_value: Any,
        dtype: DTypeLike = None,
        order: _OrderCF = 'C',
) -> NDArray[Any]:
    """Returns a new array of given shape and dtype, filled with a given value.

    This function currently does not support ``order`` option.

    Args:
        shape (int or tuple of ints): Dimensionalities of the array.
        fill_value: A scalar value to fill a new array.
        dtype (data-type, optional): Data type specifier.
        order ({'C', 'F'}): Row-major (C-style) or column-major
            (Fortran-style) order.

    Returns:
        cupy.ndarray: An array filled with ``fill_value``.

    .. seealso:: :func:`numpy.full`

    """
    if dtype is None:
        if isinstance(fill_value, cupy.ndarray):
            dtype = fill_value.dtype
        else:
            dtype = numpy.array(fill_value).dtype
    a = cupy.ndarray(shape, dtype, order=order)
    cupy.copyto(a, fill_value, casting='unsafe')
    return a


def full_like(
        a: NDArray[Any],
        fill_value: Any,
        dtype: DTypeLike = None,
        order: _OrderKACF = 'K',
        subok: None = None,
        shape: _ShapeLike | None = None,
) -> NDArray[Any]:
    """Returns a full array with same shape and dtype as a given array.

    This function currently does not support ``subok`` option.

    Args:
        a (cupy.ndarray): Base array.
        fill_value: A scalar value to fill a new array.
        dtype (data-type, optional): Data type specifier.
            The dtype of ``a`` is used by default.
        order ({'C', 'F', 'A', or 'K'}): Overrides the memory layout of the
            result. ``'C'`` means C-order, ``'F'`` means F-order, ``'A'`` means
            ``'F'`` if ``a`` is Fortran contiguous, ``'C'`` otherwise.
            ``'K'`` means match the layout of ``a`` as closely as possible.
        subok: Not supported yet, must be None.
        shape (int or tuple of ints): Overrides the shape of the result. If
            ``order='K'`` and the number of dimensions is unchanged, will try
            to keep order, otherwise, ``order='C'`` is implied.

    Returns:
        cupy.ndarray: An array filled with ``fill_value``.

    .. seealso:: :func:`numpy.full_like`

    """
    if subok is not None:
        raise TypeError('subok is not supported yet')
    if dtype is None:
        dtype = a.dtype

    order, strides, memptr = _new_like_order_and_strides(a, dtype, order,
                                                         shape)
    shape = shape if shape else a.shape
    a = cupy.ndarray(shape, dtype, memptr, strides, order)
    cupy.copyto(a, fill_value, casting='unsafe')
    return a


# Array API compatible array.astype wrapper

def astype(x, dtype, /, *, copy=True):
    """
    Copies an array to a specified data type.

    This function is an Array API compatible alternative to
    `cupy.ndarray.astype`.

    Parameters
    ----------
    x : ndarray
        Input CuPy array to cast.
    dtype : dtype
        Data type of the result.
    copy : bool, optional
        Specifies whether to copy an array when the specified dtype matches
        the data type of the input array ``x``. If ``True``, a newly allocated
        array must always be returned. If ``False`` and the specified dtype
        matches the data type of the input array, the input array must be
        returned; otherwise, a newly allocated array must be returned.
        Defaults to ``True``.

    Returns
    -------
    out : ndarray
        An array having the specified data type.

    See Also
    --------
    ndarray.astype
    numpy.astype

    """
    if not isinstance(x, cupy.ndarray):
        raise TypeError(
            f"Input should be a CuPy array. It is a {type(x)} instead."
        )
    return x.astype(dtype, copy=copy)
