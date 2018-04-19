import numpy as np


def gen_matrix(dtype):
    mat = np.zeros([7, 7], dtype=dtype)
    mat[1, 2] = 1
    mat[2, 1] = 1
    mat[2, 2] = 1
    mat[2, 3] = 1
    mat[3, 3] = 1
    mat[3, 4] = 1
    mat[4, 1] = 1
    mat[4, 4] = 1
    mat[5, 1] = 1
    mat[5, 2] = 1
    mat[5, 3] = 1
    mat[5, 4] = 1
    mat[5, 5] = 1
    mat[6, 3] = 1
    return mat


def gen_scalable_matrix():
    mat = np.zeros([6, 6], dtype=np.uint16)
    mat[0:2, 2:4] = 1
    mat[2:4, 0:2] = 1
    mat[0:2, 4:6] = 2
    mat[2:4, 2:4] = 2
    mat[4:6, 0:2] = 2
    mat[2:4, 4:6] = 3
    mat[4:6, 2:4] = 3
    mat[4:6, 4:6] = 4
    return mat


def gen_scaled_up_2_matrix():
    mat = np.zeros([12, 12], dtype=np.uint16)
    mat[0:4, 4:8] = 1
    mat[4:8, 0:4] = 1
    mat[0:4, 8:12] = 2
    mat[4:8, 4:8] = 2
    mat[8:12, 0:4] = 2
    mat[4:8, 8:12] = 3
    mat[8:12, 4:8] = 3
    mat[8:12, 8:12] = 4
    return mat


def gen_scaled_down_2_matrix():
    mat = np.zeros([3, 3], dtype=np.uint16)
    mat[0, 1] = 1
    mat[1, 0] = 1
    mat[0, 2] = 2
    mat[1, 1] = 2
    mat[2, 0] = 2
    mat[1, 2] = 3
    mat[2, 1] = 3
    mat[2, 2] = 4
    return mat
