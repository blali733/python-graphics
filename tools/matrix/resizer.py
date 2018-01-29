import numpy as np
import scipy.misc as spm
import math


def resize(image, x, y=0, upscale=False):
    """
    Function resizes image to fit given shape.

    In case of images less than given size and upscale parameter set to False, image would be centered (with top left
    skid on uneven division) and cells with no data would be filled with 0's.

    Parameters
    ----------
    image : nparray
        Input image data
    x : int
        X size of output image
    y : int optional
        Y size of output image
    upscale : bool optional
        Defines if image should be upscaled, or surrounded by zeros if it is too small

    Returns
    -------
    nparray
        Rescaled image.
    """
    if y != 0:
        size = [x, y]
    else:
        size = [x, x]
    if upscale:
        return spm.imresize(image, size)
    else:
        isize = image.shape
        if isize[0] >= size[0]:
            if isize[1] >= size[1]:
                return spm.imresize(image, size)
            else:
                image = spm.imresize(image, [size[0], isize[1]])
                diff_x = (size[1]-isize[1])/2
                return np.pad(image, ((0, 0), (math.floor(diff_x), math.ceil(diff_x))), mode="constant")
        else:
            if isize[1] >= size[1]:
                image = spm.imresize(image, [isize[0], size[1]])
                diff_y = (size[0] - isize[0]) / 2
                return np.pad(image, ((math.floor(diff_y), math.ceil(diff_y)), (0, 0)), mode="constant")
            else:
                diff_y = (size[0] - isize[0]) / 2
                diff_x = (size[1] - isize[1]) / 2
                return np.pad(image, ((math.floor(diff_y), math.ceil(diff_y)), (math.floor(diff_x), math.ceil(diff_x))),
                              mode="constant")


def shrink(mask, origin, size, absolute=False):
    x = origin[0]
    y = origin[1]
    if absolute:
        mx = size[0]
        my = size[1]
    else:
        mx = x + size[0]
        my = y + size[1]
    return mask[x:mx, y:my]


def expand(mask, origin, size, desired_size):
    """
    Expands np.array by zeroes.

    DOES NOT check if desired size is big enough, think before use.

    Parameters
    ----------
    mask
    origin
    size
    desired_size

    Returns
    -------

    """
    x = origin[0]
    y = origin[1]
    mx = x + size[0]
    my = y + size[1]
    if desired_size[0]-mx < 0:
        print("Error")
    return np.pad(mask, ([x, desired_size[0]-mx], [y, desired_size[1]-my]), mode="constant")
