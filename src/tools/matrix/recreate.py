import numpy as np


def create_3d_array(layers_list, axis):
    """
    Method responsible for recreating 3d matrix form set of 2d matrices.

    Parameters
    ----------
    layers_list : list
        list of 2d np.arrays
    axis : int
        Identifier of axis of division (stacking).

    Returns
    -------
    np.array
        Result of stacking.
    """
    # TODO check if this works properly.
    array_3d = np.stack(layers_list, axis=axis)
    return array_3d


def binearize_3d_array(array, offset):
    """
    Method converts 3d np.array with any range of float values to binary array (with only 1.0 and 0.0).

    Parameters
    ----------
    array : np.array
        Array to be binearized.
    offset : float
        Value used to divide range. Higher than offset -> 1.0.

    Returns
    -------
    np.array
        Binearized array.
    """
    return (array > offset)*1
