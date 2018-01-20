import numpy as np


def find_common_parts(manual_segmentation, manual_segmentation_stains, automatic_segmentation, extra_pixels=5, common_percentage=90):
    """

    Parameters
    ----------
    manual_segmentation : nparray
        Manual segmentation mask
    manual_segmentation_stains : list of tuples
        Result of get_list_of_stains() form pimutils.mask.separator
    automatic_segmentation : nparray
        Automated segmentation mask
    extra_pixels
    common_percentage

    Returns
    -------
    list, list
        Returns set of two list compatible with get_list_of_stains() results
    """
    tumor = []
    not_tumor = []
    if automatic_segmentation.sum() != 0:
        pass
    return tumor, not_tumor
