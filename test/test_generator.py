import unittest
import numpy as np
import tempfile
import filecmp
from os.path import join, dirname

from transcov import generator


class Test_calc_rel_start_and_end_Function(unittest.TestCase):
    def setUp(self):
        self.tss = 1000

    def test_total_lower_pos_strand(self):
        start = 550
        end = 770
        strand = "+"
        res_start, res_end = generator.calc_rel_start_and_end(
            start, end, strand, self.tss
        )
        self.assertEqual(res_start, -450)
        self.assertEqual(res_end, -230)

    def test_total_upper_pos_strand(self):
        start = 1300
        end = 1450
        strand = "+"
        res_start, res_end = generator.calc_rel_start_and_end(
            start, end, strand, self.tss
        )
        self.assertEqual(res_start, 300)
        self.assertEqual(res_end, 450)

    def test_total_upper_neg_strand(self):
        start = 1300
        end = 1450
        strand = "-"
        res_start, res_end = generator.calc_rel_start_and_end(
            start, end, strand, self.tss
        )
        self.assertEqual(res_start, -450)
        self.assertEqual(res_end, -300)

    def test_overlap_neg_strand(self):
        start = 600
        end = 1450
        strand = "-"
        res_start, res_end = generator.calc_rel_start_and_end(
            start, end, strand, self.tss
        )
        self.assertEqual(res_start, -450)
        self.assertEqual(res_end, 400)


class Test_add_read_ends_Function(unittest.TestCase):
    def setUp(self):
        self.A = np.zeros((3, 101), dtype=np.uint16)
        self.k = 50

    def test_add_center_fragment(self):
        start = -30
        end = 30
        i = 1
        generator.add_read_ends(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[start + self.k] = 1
        res[end + self.k] = 1
        self.assertTrue((self.A[i] == res).all())

    def test_left_out_of_bounds_fragment(self):
        start = -300
        end = 30
        i = 0
        generator.add_read_ends(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[end + self.k] = 1
        self.assertTrue((self.A[i] == res).all())

    def test_addtion_side_effect_fragment(self):
        start = -300
        end = 30
        i = 1
        generator.add_read_ends(self.A, start, end, i, self.k)
        generator.add_read_ends(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[end + self.k] = 2
        self.assertTrue((self.A[i] == res).all())

    def test_edges_fragment(self):
        start = -50
        end = 50
        i = 2
        generator.add_read_ends(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[start + self.k] = 1
        res[end + self.k] = 1
        self.assertTrue((self.A[i] == res).all())


class Test_add_fragment_Function(unittest.TestCase):
    def setUp(self):
        self.A = np.zeros((3, 101), dtype=np.uint16)
        self.k = 50

    def test_add_center_fragment(self):
        start = -30
        end = 30
        i = 1
        generator.add_fragment(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[start + self.k : end + self.k] = 1
        self.assertTrue((self.A[i] == res).all())

    def test_left_out_of_bounds_fragment(self):
        start = -300
        end = 30
        i = 0
        generator.add_fragment(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[start + self.k : end + self.k] = 1
        self.assertTrue((self.A[i] == res).all())

    def test_addtion_side_effect_fragment(self):
        start = -300
        end = 30
        i = 1
        generator.add_fragment(self.A, start, end, i, self.k)
        generator.add_fragment(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[start + self.k : end + self.k] = 2
        self.assertTrue((self.A[i] == res).all())

    def test_edges_fragment(self):
        start = -50
        end = 51
        i = 2
        generator.add_fragment(self.A, start, end, i, self.k)
        res = np.ones(101, dtype=np.uint16)
        self.assertTrue((self.A[i] == res).all())


class Test_module_with_file_io(unittest.TestCase):
    def setUp(self):
        self.output_matrix = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.output_matrix.close()

    def test_read_ends_matrix_generation(self):
        bam_file = join(dirname(__file__), "data/test.bam")
        bed_file = join(dirname(__file__), "data/gencode.v19.annotation.tss.bed")
        res_matrix = join(dirname(__file__), "data/read_ends_matrix.npy")
        generator.generate_read_ends_matrix(bam_file, bed_file, self.output_matrix.name)
        res = filecmp.cmp(res_matrix, self.output_matrix.name + ".npy", shallow=False)
        self.assertTrue(res)

    def test_coverage_matrix_generation(self):
        bam_file = join(dirname(__file__), "data/test.bam")
        bed_file = join(dirname(__file__), "data/gencode.v19.annotation.tss.bed")
        res_matrix = join(dirname(__file__), "data/coverage_matrix.npy")
        generator.generate_coverage_matrix(bam_file, bed_file, self.output_matrix.name)
        res = filecmp.cmp(res_matrix, self.output_matrix.name + ".npy", shallow=False)
        self.assertTrue(res)

    def test_length_matrix_generation(self):
        bam_file = join(dirname(__file__), "data/test.bam")
        bed_file = join(dirname(__file__), "data/gencode.v19.annotation.tss.bed")
        res_matrix = join(dirname(__file__), "data/length_matrix.npy")
        generator.generate_length_matrix(bam_file, bed_file, self.output_matrix.name)
        res = filecmp.cmp(res_matrix, self.output_matrix.name + ".npy", shallow=False)
        self.assertTrue(res)


if __name__ == "__main__":
    unittest.main()
