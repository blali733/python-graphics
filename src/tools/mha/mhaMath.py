import numpy as np


def med_2_float(med_image_slice, relative=True):
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
        max_val = np.iinfo(np.int16).max  # Specification of dataset says, that only positive values of int16 are used.
    val = 1/max_val
    temp = med_image_slice.astype(np.float).copy()
    temp *= val  # Legends say that division is longer operation.
    return temp


def med_2_uint8(med_image_slice, relative=True):
    """
    Converts any np.array into uint8 format compatible with images.

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
        max_val = np.iinfo(np.int16).max  # Specification of dataset says, that only positive values of int16 are used.
    val = 255/max_val
    temp = med_image_slice.astype(np.float).copy()
    temp *= val  # Legends say that division is longer operation.
    return temp.astype(np.uint8)


def med_image_binearize(med_image_slice, level=0):
    """
    Function binearizing numpy arrays

    Parameters
    ----------
    med_image_slice : np.array
        image to be binearized
    level : int
        level at which binearization would be performed; default 0

    Returns
    -------
    np.array
        binearized image as nparray
    """
    level = level+0.5
    return (med_image_slice > level)*1
