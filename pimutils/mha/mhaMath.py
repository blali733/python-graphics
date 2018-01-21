import numpy as np


def med_2_uint8(med_image_slice, relative=True):
    """
    Converts any np.array into float format compatible with images.

    Parameters
    ----------
    med_image_slice : np.array
        Numpy array representing image
    relative : bool
        Defines if scaling value should be taken as max image value (default), or max of int16 (as stated in BRATS15
        dataset).

    Returns
    -------
    np.array
        normalized image.
    """
    if relative:
        max_val = med_image_slice.max()
        max_val = max(max_val, 1)
    else:
        max_val = np.iinfo(np.int16).max
    # temp = np.zeros(med_image_slice.shape, dtype=np.float)
    # for x in range(med_image_slice.shape[0] - 1):
    #     for y in range(med_image_slice.shape[1] - 1):
    #         temp[x, y] = med_image_slice[x, y]/max_val
    # return temp
    val = 1/max_val
    temp = med_image_slice.astype(np.float).copy()
    temp *= val
    return temp


def med_image_binearize(med_image_slice, level=0):
    """
    Function binearizing nparrays

    Parameters
    ----------
    med_image_slice : nparray
        image to be binearized
    level : int
        level at which binearization would be performed; default 0

    Returns
    -------
        binearized image as nparray
    """
    level = level+0.5
    return (med_image_slice > level)*1
