import test.data_generators as dg
import numpy as np
from src.tools.mha import mhaMath


class TestMhaMath:
    def test_med_2_float_relative(self):
        matrix = dg.gen_scaled_down_2xy_matrix()
        expected = dg.gen_scaled_down_2xy_matrix_float()
        assert np.array_equal(expected, mhaMath.med_2_float(matrix))

    def test_med_2_float_absolute(self):
        matrix = dg.gen_scaled_down_2xy_matrix()
        expected = dg.gen_scaled_down_2xy_matrix_float_absolute()
        assert np.array_equal(expected, mhaMath.med_2_float(matrix, relative=False))
        
    def test_med_2_uint8_relative(self):
        matrix = dg.gen_scaled_down_2xy_matrix()
        expected = dg.gen_scaled_down_2xy_matrix_uint8_stretch()
        assert np.array_equal(expected, mhaMath.med_2_uint8(matrix))

    def test_med_2_uint8_absolute(self):
        matrix = dg.gen_scaled_down_2xy_matrix()
        expected = dg.gen_scaled_down_2xy_matrix_uint8_stretch_absolute()
        assert np.array_equal(expected, mhaMath.med_2_uint8(matrix, relative=False))

    def test_med_image_binearize_level_0(self):
        matrix = dg.gen_scaled_down_2xy_matrix()
        expected = dg.gen_scaled_down_2xy_matrix_binearized_at_0()
        assert np.array_equal(expected, mhaMath.med_image_binearize(matrix))

    def test_med_image_binearize_level_5(self):
        matrix = dg.gen_scaled_down_2xy_matrix()
        expected = dg.gen_scaled_down_2xy_matrix_binearized_at_5()
        assert np.array_equal(expected, mhaMath.med_image_binearize(matrix, level=5))
