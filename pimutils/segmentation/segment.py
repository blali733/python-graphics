import numpy as np


def flair(image_slice):
    return np.zeros(image_slice.shape, dtype=image_slice.dtype)


def t1(image_slice):
    return np.zeros(image_slice.shape, dtype=image_slice.dtype)


def t1c(image_slice):
    return np.zeros(image_slice.shape, dtype=image_slice.dtype)


def t2(image_slice):
    return np.zeros(image_slice.shape, dtype=image_slice.dtype)
