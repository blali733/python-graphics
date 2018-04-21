import numpy as np


def gen_data_layer_mask_result():
    data = np.arange(2500).reshape(50, 50).astype(np.int16)
    # region mask
    mask = np.zeros([50, 50], dtype=np.int16)
    mask[10, 7:15] = 1
    mask[11, 5:20] = 1
    mask[12, 7:15] = 1

    mask[2, 22] = 1
    mask[3, 20:25] = 1
    mask[3, 26] = 1
    mask[4, 22:27] = 1
    mask[5, 25:28] = 1

    mask[40:44, 40] = 1
    # endregion
    # region expected_stains
    stains = data * mask
    expected_stains = [(stains[2:6, 20:28], mask[2:6, 20:28], 2, 20), (stains[10:13, 5:20], mask[10:13, 5:20], 10, 5)]
    # endregion
    return data, mask, expected_stains


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


def gen_scaled_down_2xy_matrix_binearized_at_5():
    mat = np.zeros([3, 3], dtype=np.uint16)
    mat[2, 0] = 1
    mat[2, 1] = 1
    mat[2, 2] = 1
    return mat

def gen_scaled_down_2xy_matrix_binearized_at_0():
    mat = np.ones([3, 3], dtype=np.uint16)
    mat[0, 0] = 0
    return mat


def gen_scaled_down_2xy_matrix_float():
    mat = np.zeros([3, 3], dtype=np.float)
    mat[0, 1] = 0.125
    mat[0, 2] = 0.25
    mat[1, 0] = 0.375
    mat[1, 1] = 0.5
    mat[1, 2] = 0.625
    mat[2, 0] = 0.75
    mat[2, 1] = 0.875
    mat[2, 2] = 1.0
    return mat


def gen_scaled_down_2xy_matrix_float_absolute():
    mat = np.zeros([3, 3], dtype=np.float)
    mat[0, 1] = 3.051850947599719e-05
    mat[0, 2] = 6.103701895199438e-05
    mat[1, 0] = 9.155552842799158e-05
    mat[1, 1] = 0.00012207403790398877
    mat[1, 2] = 0.00015259254737998596
    mat[2, 0] = 0.00018311105685598315
    mat[2, 1] = 0.00021362956633198035
    mat[2, 2] = 0.00024414807580797754
    return mat


def gen_scaled_down_2xy_matrix_uint8_stretch():
    mat = np.zeros([3, 3], dtype=np.uint8)
    mat[0, 1] = 31
    mat[0, 2] = 63
    mat[1, 0] = 95
    mat[1, 1] = 127
    mat[1, 2] = 159
    mat[2, 0] = 191
    mat[2, 1] = 223
    mat[2, 2] = 255
    return mat


def gen_scaled_down_2xy_matrix_uint8_stretch_absolute():
    mat = np.zeros([3, 3], dtype=np.uint8)
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


def gen_bin_matrix_1():
    mat = np.zeros([8, 8], dtype=np.uint16)
    mat[0:5, 0:5] = 1
    return mat


def gen_bin_matrix_2():
    mat = np.zeros([8, 8], dtype=np.uint16)
    mat[2:8, 2:8] = 1
    return mat
