import numpy as np


def raw_compare(mask1, mask2):
    """
    Function counting number of pixels in sets given by masks.

    Parameters
    ----------
    mask1 : np.array
        First mask.
    mask2 : np.array
        Second mask.

    Returns
    -------
    int
        Number of pixels in mask1 but not in mask2.
    int
        Number of pixels in common part.
    int
        Number of pixels in mask2 but not in mask1.
    """
    common_m1_m2 = np.multiply(mask1, mask2)
    m1_not_m2 = np.multiply(mask1, np.logical_not(mask2))
    m2_not_m1 = np.multiply(mask2, np.logical_not(mask1))
    return m1_not_m2.sum(), common_m1_m2.sum(), m2_not_m1.sum()
