from src.tools.mask import separator
from test import data_generators as dg
import numpy as np


class TestSeparator:
    separator_class = separator.Separator(5)

    # def test_check_neighbourhood(self):
    #     pass

    def test_get_list_of_stains(self):
        data, mask, expected_stains = dg.gen_data_layer_mask_result()
        stains = self.separator_class.get_list_of_stains((data, mask))
        for i in range(expected_stains.__len__()):
            assert np.array_equal(expected_stains[i][0], stains[i][0])
            assert np.array_equal(expected_stains[i][1], stains[i][1])
            assert expected_stains[i][2] == stains[i][2]
            assert expected_stains[i][3] == stains[i][3]
