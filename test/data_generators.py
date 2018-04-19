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
    mat[0:2, 4:6] = 2
    mat[2:4, 0:2] = 3
    mat[2:4, 2:4] = 4
    mat[2:4, 4:6] = 5
    mat[4:6, 0:2] = 6
    mat[4:6, 2:4] = 7
    mat[4:6, 4:6] = 8
    return mat


def gen_scaled_down_2y_matrix():
    mat = np.zeros([3, 6], dtype=np.uint16)
    mat[0, 2:4] = 1
    mat[0, 4:6] = 2
    mat[1, 0:2] = 3
    mat[1, 2:4] = 4
    mat[1, 4:6] = 5
    mat[2, 0:2] = 6
    mat[2, 2:4] = 7
    mat[2, 4:6] = 8
    return mat


def gen_scaled_down_2x_matrix():
    mat = np.zeros([6, 3], dtype=np.uint16)
    mat[0:2, 1] = 1
    mat[0:2, 2] = 2
    mat[2:4, 0] = 3
    mat[2:4, 1] = 4
    mat[2:4, 2] = 5
    mat[4:6, 0] = 6
    mat[4:6, 1] = 7
    mat[4:6, 2] = 8
    return mat


def gen_scaled_down_2xy_matrix():
    mat = np.zeros([3, 3], dtype=np.uint16)
    mat[0, 1] = 1
    mat[0, 2] = 2
    mat[1, 0] = 3
    mat[1, 1] = 4
    mat[1, 2] = 5
    mat[2, 0] = 6
    mat[2, 1] = 7
    mat[2, 2] = 8
    return mat


def gen_scaled_up_2xy_matrix():
    mat = np.zeros([12, 12], dtype=np.uint16)
    mat[0:4, 4:8] = 1
    mat[0:4, 8:12] = 2
    mat[4:8, 0:4] = 3
    mat[4:8, 4:8] = 4
    mat[4:8, 8:12] = 5
    mat[8:12, 0:4] = 6
    mat[8:12, 4:8] = 7
    mat[8:12, 8:12] = 8
    return mat


def gen_scaled_up_2x_matrix():
    mat = np.zeros([6, 12], dtype=np.uint16)
    mat[0:2, 4:8] = 1
    mat[0:2, 8:12] = 2
    mat[2:4, 0:4] = 3
    mat[2:4, 4:8] = 4
    mat[2:4, 8:12] = 5
    mat[4:6, 0:4] = 6
    mat[4:6, 4:8] = 7
    mat[4:6, 8:12] = 8
    return mat


def gen_scaled_up_2y_matrix():
    mat = np.zeros([12, 6], dtype=np.uint16)
    mat[0:4, 2:4] = 1
    mat[0:4, 4:6] = 2
    mat[4:8, 0:2] = 3
    mat[4:8, 2:4] = 4
    mat[4:8, 4:6] = 5
    mat[8:12, 0:2] = 6
    mat[8:12, 2:4] = 7
    mat[8:12, 4:6] = 8
    return mat
