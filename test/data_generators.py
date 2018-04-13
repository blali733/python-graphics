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
