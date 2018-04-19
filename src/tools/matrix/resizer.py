import numpy as np
import math
import PIL.Image as pim


def imresize(image, size):
    """
    Function resizing array as image preserving data type.

    Parameters
    ----------
    image : np.array
        Input image.
    size : tuple of ints
        desired shape of image.

    Returns
    -------
    np.array
        Resized image.
    """
    pil_image = pim.fromarray(image)
    return np.array(pil_image.resize(size))


def resize(image, x, y=0, upscale=False):
    """
    Function resizes image to fit given shape.

    In case of images less than given size and upscale parameter set to False, image would be centered (with top left
    skid on uneven division) and cells with no data would be filled with 0's.

    Parameters
    ----------
    image : np.array
        Input image data
    x : int
        X size of output image
    y : int, optional
        Y size of output image
    upscale : bool, optional
        Defines if image should be upscaled, or surrounded by zeros if it is too small

    Returns
    -------
    np.array
        Rescaled image.
    """
    # Just in case:
    if x < 0 or y < 0:
        raise IndexError("Parameters can not be negative!")
    if y != 0:
        size = [x, y]
    else:
        size = [x, x]
    if upscale:
        return imresize(image, size)
    else:
        isize = image.shape
        if isize[0] >= size[0]:
            if isize[1] >= size[1]:
                return imresize(image, size)
            else:
                image = imresize(image, [size[0], isize[1]])
                diff_x = (size[1]-isize[1])/2
                return np.pad(image, ((0, 0), (math.floor(diff_x), math.ceil(diff_x))), mode="constant")
        else:
            if isize[1] >= size[1]:
                image = imresize(image, [isize[0], size[1]])
                diff_y = (size[0] - isize[0]) / 2
                return np.pad(image, ((math.floor(diff_y), math.ceil(diff_y)), (0, 0)), mode="constant")
            else:
                diff_y = (size[0] - isize[0]) / 2
                diff_x = (size[1] - isize[1]) / 2
                return np.pad(image, ((math.floor(diff_y), math.ceil(diff_y)), (math.floor(diff_x), math.ceil(diff_x))),
                              mode="constant")


def shrink(mask, origin, size, absolute=False):
    """
    Method provides cutout of mask with defined size.

    Parameters
    ----------
    mask : np.array
        Original image to be cropped.
    origin : tuple of ints
        Top left pixel of fragment.
    size : tuple of ints
        Offset or bottom right pixel.
    absolute : bool
        Defines if size is passed as pixel coordinates or offset

    Returns
    -------
    np.array
        Cropped image.
    """
    # Just in case:
    if origin[0] < 0 or origin[1] < 0 or size[0] < 0 or size[1] < 0:
        raise IndexError("Parameters can not be negative!")
    d1 = origin[0]
    d2 = origin[1]
    if absolute:
        md1 = size[0] + 1
        md2 = size[1] + 1
    else:
        md1 = d1 + size[0]
        md2 = d2 + size[1]
    return mask[d1:md1, d2:md2]


def expand(mask, origin, size, desired_size):
    """
    Expands np.array by zeroes.

    Parameters
    ----------
    mask : np.array
        Original image to be cropped.
    origin : tuple of ints
        Top left pixel of fragment in output image.
    size : tuple of ints
        Offset to the bottom right end of fragment.
    desired_size : tuple of ints
        Shape of output array.

    Returns
    -------
    np.array
        Fragment in bigger array expanded by 0's.
    """
    # Just in case:
    if origin[0] < 0 or origin[1] < 0 or size[0] < 0 or size[1] < 0 or desired_size[0] < 0 or desired_size[1] < 0:
        raise IndexError("Parameters can not be negative!")
    d1 = origin[0]
    d2 = origin[1]
    md1 = d1 + size[0]
    md2 = d2 + size[1]
    if desired_size[0]-md1 < 0 or desired_size[1]-md2 < 0:
        raise IndexError("Cannot expand to smaller container!")
    return np.pad(mask, ([d1, desired_size[0]-md1], [d2, desired_size[1]-md2]), mode="constant")
