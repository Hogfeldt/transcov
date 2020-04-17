import unittest
import numpy as np
from transcov import generator

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

class Test_calc_rel_start_and_end_Function(unittest.TestCase):

    def setUp(self):
        self.tss = 1000

    def test_total_lower_pos_strand(self):
        start = 550
        end = 770
        strand = '+'
        res_start, res_end = generator.calc_rel_start_and_end(start, end, strand, self.tss)
        self.assertEqual(res_start, -450)
        self.assertEqual(res_end, -230)

    def test_total_upper_pos_strand(self):
        start = 1300
        end = 1450
        strand = '+'
        res_start, res_end = generator.calc_rel_start_and_end(start, end, strand, self.tss)
        self.assertEqual(res_start, 300)
        self.assertEqual(res_end, 450)
        
    def test_total_upper_neg_strand(self):
        start = 1300
        end = 1450
        strand = '-'
        res_start, res_end = generator.calc_rel_start_and_end(start, end, strand, self.tss)
        self.assertEqual(res_start, -450)
        self.assertEqual(res_end, -300)

    def test_overlap_neg_strand(self):
        start = 600
        end = 1450
        strand = '-'
        res_start, res_end = generator.calc_rel_start_and_end(start, end, strand, self.tss)
        self.assertEqual(res_start, -450)
        self.assertEqual(res_end, 400)

class Test_add_read_ends_Function(unittest.TestCase):

    def setUp(self):
        self.A = np.zeros((3,101), dtype=np.uint16)
        self.k = 50

    def test_add_center_fragment(self):
        start = -30
        end = 30
        i = 1
        generator.add_read_ends(self.A, start, end, i, self.k)
        res = np.zeros(101, dtype=np.uint16)
        res[start + self.k] = 1
        res[end + self.k] = 1
        self.assertTrue((self.A[i]==res).all())


if __name__=='__main__':
    unittest.main()
