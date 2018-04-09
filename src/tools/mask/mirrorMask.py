import numpy as np
from src.tools.matrix import resizer


def flip_and_check(image, mask, mask_stains):
    """
    SUFFERS HEAVY DAMAGE IN LOGIC, DO NOT USE.

    Method responsible for generating mirrored masks of manual segmentation. Returns only stains which are fully
    separated from original one.

    Parameters
    ----------
    image : np.array
        Slice of mha image.
    mask : np.array
        Mask corresponding to slice.
    mask_stains : list
        List of stains in mask.

    Returns
    -------
        List of stains.
    """
    stains = []
    if mask.sum() != 0:
        flipped = np.flip(mask, axis=1)
        common = np.multiply(mask, flipped)
        if common.sum() == 0:
            for tup in mask_stains:
                mask_part = tup[1]
                x = tup[2]
                y = tup[3]
                part_shape = mask_part.shape
                mask_part = resizer.expand(mask_part, [x, y], part_shape, mask.shape)
                mask_part = np.flip(mask_part, axis=1)
                x = mask.shape[0]-x-part_shape[0]
                image_part = resizer.shrink(np.multiply(image, mask_part), [x, y], part_shape)
                mask_part = resizer.shrink(mask_part, [x, y], part_shape)
                if image_part.sum() != 0:
                    stains.append((image_part, mask_part, x, y))
        else:
            # Not worth the effort to separate candidates
            pass
    return stains
