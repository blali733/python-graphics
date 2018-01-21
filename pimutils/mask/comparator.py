import numpy as np


def compare(manual_mask, generated_mask, silent=False):
    """
    Generator of statistics when comparing two masks.

    THIS CODE HAS BUGS, AND IT IS SO LOW PRIORITY TO FIX IT.

    Parameters
    ----------
    manual_mask : np.array
        Mask obtained from manual segmentation by expert
    generated_mask : np.array
        Mask generated programatically
    silent : bool optional
        Disables printing values when set to True.

    Returns
    -------
    float
        Percentage of manual segmentation covered by automatic one.
    int
        Number of pixels not matching manual segmentation
    """
    manual_sum = manual_mask.sum()
    overshoot_sum = np.multiply(generated_mask, np.logical_not(manual_mask)).sum()
    common_part = np.multiply(generated_mask, manual_mask).sum()
    if not silent:
        print("Common mask part: " + (common_part/manual_sum).__str__()
              + "%, generated mask contains " + overshoot_sum.__str__() + " additional pixels.")
    return common_part/manual_sum, overshoot_sum


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
