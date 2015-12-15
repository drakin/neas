# License (Modified BSD)
#
# Copyright (C) 2011, the scikit-image team All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of skimage nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# links:
# https://github.com/scikit-image/scikit-image/blob/master/skimage/draw/
# https://github.com/scikit-image/scikit-image/blob/master/skimage/draw/draw.py
# https://github.com/scikit-image/scikit-image/blob/master/skimage/draw/_draw.pyx
import numpy as np
from math import *


def _coords_inside_image(rr, cc, shape, val=None):
    """
    Return the coordinates inside an image of a given shape.
    Parameters
    ----------
    rr, cc : (N,) ndarray of int
        Indices of pixels.
    shape : tuple
        Image shape which is used to determine the maximum extent of output
        pixel coordinates.
    val : ndarray of float, optional
        Values of pixels at coordinates [rr, cc].
    Returns
    -------
    rr, cc : (N,) array of int
        Row and column indices of valid pixels (i.e. those inside `shape`).
    val : (N,) array of float, optional
        Values at `rr, cc`. Returned only if `val` is given as input.
    """
    mask = (rr >= 0) & (rr < shape[0]) & (cc >= 0) & (cc < shape[1])
    if val is not None:
        return rr[mask], cc[mask], val[mask]
    return rr[mask], cc[mask]

def circle_perimeter(cy, cx,  radius,
                     method='bresenham', shape=None):
    """Generate circle perimeter coordinates.
    Parameters
    ----------
    cy, cx : int
        Centre coordinate of circle.
    radius: int
        Radius of circle.
    method : {'bresenham', 'andres'}, optional
        bresenham : Bresenham method (default)
        andres : Andres method
    shape : tuple, optional
        Image shape which is used to determine the maximum extent of output pixel
        coordinates. This is useful for circles which exceed the image size.
        By default the full extent of the circle are used.
    Returns
    -------
    rr, cc : (N,) ndarray of int
        Bresenham and Andres' method:
        Indices of pixels that belong to the circle perimeter.
        May be used to directly index into an array, e.g.
        ``img[rr, cc] = 1``.
    Notes
    -----
    Andres method presents the advantage that concentric
    circles create a disc whereas Bresenham can make holes. There
    is also less distortions when Andres circles are rotated.
    Bresenham method is also known as midpoint circle algorithm.
    Anti-aliased circle generator is available with `circle_perimeter_aa`.
    References
    ----------
    .. [1] J.E. Bresenham, "Algorithm for computer control of a digital
           plotter", IBM Systems journal, 4 (1965) 25-30.
    .. [2] E. Andres, "Discrete circles, rings and spheres", Computers &
           Graphics, 18 (1994) 695-706.
    Examples
    --------
    >>> from skimage.draw import circle_perimeter
    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> rr, cc = circle_perimeter(4, 4, 3)
    >>> img[rr, cc] = 1
    >>> img
    array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
           [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
    """

    rr = list()
    cc = list()

    x = 0
    y = radius
    d = 0

    dceil = 0
    dceil_prev = 0

    cmethod=''
    if method == 'bresenham':
        d = 3 - 2 * radius
        cmethod = 'b'
    elif method == 'andres':
        d = radius - 1
        cmethod = 'a'
    else:
        raise ValueError('Wrong method')

    while y >= x:
        rr.extend([y, -y, y, -y, x, -x, x, -x])
        cc.extend([x, x, -x, -x, y, y, -y, -y])

        if cmethod == 'b':
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
        elif cmethod == 'a':
            if d >= 2 * (x - 1):
                d = d - 2 * x
                x = x + 1
            elif d <= 2 * (radius - y):
                d = d + 2 * y - 1
                y = y - 1
            else:
                d = d + 2 * (y - x - 1)
                y = y - 1
                x = x + 1
    if shape is not None:
        return _coords_inside_image(np.array(rr, dtype=np.intp) + cy,
                                    np.array(cc, dtype=np.intp) + cx,
                                    shape)
    return (np.array(rr, dtype=np.intp) + cy,
            np.array(cc, dtype=np.intp) + cx)

def circle_perimeter_aa(cy, cx, radius,
                        shape=None):
    """Generate anti-aliased circle perimeter coordinates.
    Parameters
    ----------
    cy, cx : int
        Centre coordinate of circle.
    radius: int
        Radius of circle.
    shape : tuple, optional
        Image shape which is used to determine the maximum extent of output pixel
        coordinates. This is useful for circles which exceed the image size.
        By default the full extent of the circle are used.
    Returns
    -------
    rr, cc, val : (N,) ndarray (int, int, float)
        Indices of pixels (`rr`, `cc`) and intensity values (`val`).
        ``img[rr, cc] = val``.
    Notes
    -----
    Wu's method draws anti-aliased circle. This implementation doesn't use
    lookup table optimization.
    References
    ----------
    .. [1] X. Wu, "An efficient antialiasing technique", In ACM SIGGRAPH
           Computer Graphics, 25 (1991) 143-152.
    Examples
    --------
    >>> from skimage.draw import circle_perimeter_aa
    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> rr, cc, val = circle_perimeter_aa(4, 4, 3)
    >>> img[rr, cc] = val * 255
    >>> img
    array([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
           [  0,   0,  60, 211, 255, 211,  60,   0,   0,   0],
           [  0,  60, 194,  43,   0,  43, 194,  60,   0,   0],
           [  0, 211,  43,   0,   0,   0,  43, 211,   0,   0],
           [  0, 255,   0,   0,   0,   0,   0, 255,   0,   0],
           [  0, 211,  43,   0,   0,   0,  43, 211,   0,   0],
           [  0,  60, 194,  43,   0,  43, 194,  60,   0,   0],
           [  0,   0,  60, 211, 255, 211,  60,   0,   0,   0],
           [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
           [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=uint8)
    """

    x = 0
    y = radius
    d = 0

    dceil = 0
    dceil_prev = 0

    rr = [y, x,  y,  x, -y, -x, -y, -x]
    cc = [x, y, -x, -y,  x,  y, -x, -y]
    val = [1] * 8

    while y > x + 1:
        x += 1
        dceil = sqrt(radius**2 - x**2)
        dceil = ceil(dceil) - dceil
        if dceil < dceil_prev:
            y -= 1
        rr.extend([y, y - 1, x, x, y, y - 1, x, x])
        cc.extend([x, x, y, y - 1, -x, -x, -y, 1 - y])

        rr.extend([-y, 1 - y, -x, -x, -y, 1 - y, -x, -x])
        cc.extend([x, x, y, y - 1, -x, -x, -y, 1 - y])

        val.extend([1 - dceil, dceil] * 8)
        dceil_prev = dceil

    if shape is not None:
        return _coords_inside_image(np.array(rr, dtype=np.intp) + cy,
                                    np.array(cc, dtype=np.intp) + cx,
                                    shape,
                                    val=np.array(val, dtype=np.float))
    return (np.array(rr, dtype=np.intp) + cy,
            np.array(cc, dtype=np.intp) + cx,
            np.array(val, dtype=np.float))


def _ellipse_in_shape(shape, center, radiuses):
    """Generate coordinates of points within ellipse bounded by shape."""
    y, x = np.ogrid[0:float(shape[0]), 0:float(shape[1])]
    cy, cx = center
    ry, rx = radiuses
    distances = ((y - cy) / ry) ** 2 + ((x - cx) / rx) ** 2
    return np.nonzero(distances < 1)


def ellipse(cy, cx, yradius, xradius, shape=None):
    """Generate coordinates of pixels within ellipse.
    Parameters
    ----------
    cy, cx : double
        Centre coordinate of ellipse.
    yradius, xradius : double
        Minor and major semi-axes. ``(x/xradius)**2 + (y/yradius)**2 = 1``.
    shape : tuple, optional
        Image shape which is used to determine the maximum extent of output pixel
        coordinates. This is useful for ellipses which exceed the image size.
        By default the full extent of the ellipse are used.
    Returns
    -------
    rr, cc : ndarray of int
        Pixel coordinates of ellipse.
        May be used to directly index into an array, e.g.
        ``img[rr, cc] = 1``.
    Examples
    --------
    >>> from skimage.draw import ellipse
    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> rr, cc = ellipse(5, 5, 3, 4)
    >>> img[rr, cc] = 1
    >>> img
    array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
    """

    center = np.array([cy, cx])
    radiuses = np.array([yradius, xradius])

    # The upper_left and lower_right corners of the
    # smallest rectangle containing the ellipse.
    upper_left = np.ceil(center - radiuses).astype(int)
    lower_right = np.floor(center + radiuses).astype(int)

    if shape is not None:
        # Constrain upper_left and lower_right by shape boundary.
        upper_left = np.maximum(upper_left, np.array([0, 0]))
        lower_right = np.minimum(lower_right, np.array(shape[:2]) - 1)

    shifted_center = center - upper_left
    bounding_shape = lower_right - upper_left + 1

    rr, cc = _ellipse_in_shape(bounding_shape, shifted_center, radiuses)
    rr.flags.writeable = True
    cc.flags.writeable = True
    rr += upper_left[0]
    cc += upper_left[1]
    return rr, cc


def circle(cy, cx, radius, shape=None):
    """Generate coordinates of pixels within circle.
    Parameters
    ----------
    cy, cx : double
        Centre coordinate of circle.
    radius: double
        Radius of circle.
    shape : tuple, optional
        Image shape which is used to determine the maximum extent of output pixel
        coordinates. This is useful for circles which exceed the image size.
        By default the full extent of the circle are used.
    Returns
    -------
    rr, cc : ndarray of int
        Pixel coordinates of circle.
        May be used to directly index into an array, e.g.
        ``img[rr, cc] = 1``.
    Notes
    -----
        This function is a wrapper for skimage.draw.ellipse()
    Examples
    --------
    >>> from skimage.draw import circle
    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> rr, cc = circle(4, 4, 5)
    >>> img[rr, cc] = 1
    >>> img
    array([[0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
           [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
    """

    return ellipse(cy, cx, radius, radius, shape)