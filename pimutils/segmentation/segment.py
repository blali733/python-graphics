import numpy as np
import cv2
from pimutils.mha import mhaMath


def flair(image_slice):
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.047)*(img > 0.016)*1


def t1(image_slice):
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.017) * (img > 0.013) * 1


def t1c(image_slice):
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.045) * (img > 0.019) * 1


def t2(image_slice):
    img = mhaMath.med_2_float(image_slice, False)
    return (img < 0.05) * (img > 0.022) * 1
