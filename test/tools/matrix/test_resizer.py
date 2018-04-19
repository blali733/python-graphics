import test.data_generators as dg
import numpy as np
from src.tools.matrix import resizer
import pytest


class TestResizer:
    # region imresize
    def test_imresize_downscale(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_down_2xy_matrix()
        assert np.array_equal(expected, resizer.imresize(base, (3, 3)))

    def test_imresize_upscale(self):
        base = dg.gen_scalable_matrix()
        expected = dg.gen_scaled_up_2xy_matrix()
        assert np.array_equal(expected, resizer.imresize(base, (12, 12)))
    # endregion

    # region resize
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

    def test_resize_exception_negative_x(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.resize(base, -5)
        assert "Parameters can not be negative!" in str(e_info.value)

    def test_resize_exception_negative_y(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.resize(base, 7, -5)
        assert "Parameters can not be negative!" in str(e_info.value)
    # endregion

    # region shrink
    def test_shrink_exception_negative_origin(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.shrink(base, (-5, 4), (3, 5))
        assert "Parameters can not be negative!" in str(e_info.value)

    def test_shrink_exception_negative_size(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.shrink(base, (5, 4), (-3, 5))
        assert "Parameters can not be negative!" in str(e_info.value)
    # endregion

    # region expand
    def test_expand_exception_negative_origin(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.expand(base, (5, -4), (3, 5), (20, 20))
        assert "Parameters can not be negative!" in str(e_info.value)

    def test_expand_exception_negative_size(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.expand(base, (5, 4), (-3, 5), (20, 20))
        assert "Parameters can not be negative!" in str(e_info.value)

    def test_expand_exception_negative_desired_size(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.expand(base, (5, 4), (3, 5), (20, -20))
        assert "Parameters can not be negative!" in str(e_info.value)

    def test_expand_exception_too_small_desired_size(self):
        base = dg.gen_scalable_matrix()
        with pytest.raises(IndexError) as e_info:
            resizer.expand(base, (5, 4), (3, 5), (1, 1))
        assert "Cannot expand to smaller container!" in str(e_info.value)
    # endregion
