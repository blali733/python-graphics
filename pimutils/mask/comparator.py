import numpy as np


def compare(manual_mask, generated_mask, silent=False):
    manual_sum = manual_mask.sum()
    overshoot_sum = np.multiply(generated_mask, np.logical_not(manual_mask)).sum()
    common_part = np.multiply(generated_mask, manual_mask).sum()
    if not silent:
        print("Common mask part: " + (common_part/manual_sum).__str__()
              + "%, generated mask contains " + overshoot_sum.__str__() + " additional pixels.")
    return common_part/manual_sum, overshoot_sum
