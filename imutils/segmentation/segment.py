import numpy as np


def flair(slice):
    return np.zeros(slice.shape, dtype=slice.dtype)


def t1(slice):
    return np.zeros(slice.shape, dtype=slice.dtype)


def t1c(slice):
    return np.zeros(slice.shape, dtype=slice.dtype)


def t2(slice):
    return np.zeros(slice.shape, dtype=slice.dtype)
