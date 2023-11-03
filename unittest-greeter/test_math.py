import unittest
from math import add

class AddTest(unittest.TestCase):
    def test_add_two_integers(self):
        """should return the sum of two integers"""
        self.assertEqual(3, add(1, 2))
        self.assertEqual(6, add(2, 4))

    def test_add_strings(self):
        """should raise TypeError for strings that are not numbers"""
        with self.assertRaises(TypeError):
            add("1", "2")
