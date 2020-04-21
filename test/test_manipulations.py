import unittest
import numpy as np
import tempfile
import filecmp
from os.path import join, dirname

import transcov.manipulations as mut


class Test_pick_subset_by_row_index(unittest.TestCase):
    def setUp(self):
        self.X = np.arange(12, dtype=np.uint16).reshape(4, 3)

    def test_pick_two_rows(self):
        index_pairs = ((0, 1), (1, 2))
        n = len(index_pairs)
        res = mut.pick_subset_by_row_index(self.X, index_pairs, n)
        exp_res = np.array([[3, 4, 5], [6, 7, 8]], dtype=np.uint16)
        self.assertTrue((res == exp_res).all())


class Test_pick_subset_integration(unittest.TestCase):
    def setUp(self):
        # create input matrix
        self.input_matrix = tempfile.NamedTemporaryFile()
        A = np.arange(12, dtype=np.uint16).reshape(4, 3)
        np.save(self.input_matrix.name, A)
        # create input index
        self.input_index = tempfile.NamedTemporaryFile()
        with open(self.input_index.name, "w") as fp:
            fp.write("#index\tid\n0\ta\n1\tb\n2\tc\n3\td")
        # instantiate output file
        self.output_matrix = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.input_matrix.close()
        self.input_index.close()
        self.output_matrix.close()

    def test_pick_subset(self):
        ids = ["b", "c"]
        mut.pick_subset(
            self.input_matrix.name + ".npy",
            self.input_index.name,
            self.output_matrix.name,
            ids,
        )
        exp_res = np.array([[3, 4, 5], [6, 7, 8]], dtype=np.uint16)
        res = np.load(self.output_matrix.name + ".npy")
        self.assertTrue((res == exp_res).all())

class Test_collapse_integration(unittest.TestCase):
    def setUp(self):
        self.output_matrix = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.output_matrix.close()

    def test_coverage_collapse(self):
        matrix = join(dirname(__file__), "data/coverage_matrix.npy")
        index = join(dirname(__file__), "data/coverage_matrix.index")
        matrix_index_pairs = [(matrix, index), (matrix, index)]
        mut.collapse(matrix_index_pairs, self.output_matrix.name)
        A = np.load(matrix)
        B = np.load(self.output_matrix.name + ".npy")
        self.assertTrue(((A+A)==B).all())

class Test_cut_tails_both_integration(unittest.TestCase):
    def setUp(self):
        self.output_matrix = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.output_matrix.close()

    def test_cut_tails_both(self):
        matrix = join(dirname(__file__), "data/coverage_matrix.npy")
        index = join(dirname(__file__), "data/coverage_matrix.index")
        mut.cut_tails_both(matrix, index, self.output_matrix.name)
        An, Am = np.load(matrix).shape
        Bn, Bm = np.load(self.output_matrix.name + ".npy").shape
        self.assertTrue(An>Bn)
        self.assertTrue(Am==Bm)

if __name__ == "__main__":
    unittest.main()
