import numpy as np


# def med_image_binearize(med_image_slice, level=0, dtype=np.uint8):
#     """
#     Function binearizing nparrays
#
#     Parameters
#     ----------
#     med_image_slice : nparray
#         image to be binearized
#     level : int
#         level at which binearization would be performed; default 0
#     dtype : npdatatype
#         data type of resulting array; default np.uint8
#
#     Returns
#     -------
#         binearized image as nparray
#     """
#     temp = np.zeros(med_image_slice.shape, dtype=dtype)
#     for x in range(med_image_slice.shape[0] - 1):
#         for y in range(med_image_slice.shape[1] - 1):
#             if med_image_slice[x, y] > level:
#                 temp[x, y] = 1
#     return temp

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
