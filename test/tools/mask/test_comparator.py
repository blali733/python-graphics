import test.data_generators as dg
import numpy as np
from src.tools.mask import comparator
import pytest


class TestComparator:
    def test_raw_compare(self):
        mask1 = dg.gen_bin_matrix_1()
        mask2 = dg.gen_bin_matrix_2()
        expected = (16, 9, 27)
        assert expected == comparator.raw_compare(mask1, mask2)
