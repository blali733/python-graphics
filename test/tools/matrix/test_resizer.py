import test.data_generators as dg
import numpy as np
from src.tools.matrix import resizer


class TestResizer:
    def test_imresize_downscale(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_down_2xy_matrix()
        assert np.array_equal(expected, resizer.imresize(base, (3, 3)))

    def test_imresize_upscale(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_up_2xy_matrix()
        assert np.array_equal(expected, resizer.imresize(base, (12, 12)))

    def test_resize_1_to_1(self):
        base = dg.gen_matrix(dtype=np.uint16)
        assert np.array_equal(base, resizer.resize(base, 7, 7))

    def test_resize_up_xy_fill(self):
        base = dg.gen_matrix(dtype=np.uint16)
        result = np.pad(base, ((4, 4), (4, 4)), mode="constant")
        assert np.array_equal(result, resizer.resize(base, 15, 15))

    def test_resize_up_x_fill(self):
        base = dg.gen_matrix(dtype=np.uint16)
        result = np.pad(base, ((0, 0), (4, 4)), mode="constant")
        assert np.array_equal(result, resizer.resize(base, 7, 15))

    def test_resize_up_y_fill(self):
        base = dg.gen_matrix(dtype=np.uint16)
        result = np.pad(base, ((4, 4), (0, 0)), mode="constant")
        assert np.array_equal(result, resizer.resize(base, 15, 7))

    def test_imresize_up_xy_stretch(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_up_2xy_matrix()
        assert np.array_equal(expected, resizer.resize(base, 12, upscale=True))

    def test_imresize_up_x_stretch(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_up_2x_matrix()
        assert np.array_equal(expected, resizer.resize(base, 12, 6, upscale=True))

    def test_imresize_up_y_stretch(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_up_2y_matrix()
        assert np.array_equal(expected, resizer.resize(base, 6, 12, upscale=True))

    def test_resize_down_xy(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_down_2xy_matrix()
        assert np.array_equal(expected, resizer.resize(base, 3))

    def test_resize_down_x(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_down_2x_matrix()
        assert np.array_equal(expected, resizer.resize(base, 3, 6))

    def test_resize_down_y(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_down_2y_matrix()
        assert np.array_equal(expected, resizer.resize(base, 6, 3))

    # def test_shrink(self):
    #     assert False
    #
    # def test_expand(self):
    #     assert False
