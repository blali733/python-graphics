import numpy as np


def flip_and_check(image, mask, mask_stains):
    stains = []
    if mask.sum() != 0:
        flipped = np.flip(mask, axis=1)
        common = np.multiply(mask, flipped)
        if common.sum() == 0:
            # TODO flip elements of mask stains
            pass
        else:
            # TODO decide what to do in that case
            pass
    else:
        return stains