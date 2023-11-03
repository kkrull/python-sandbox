import unittest
from math import add

class AddTest(unittest.TestCase):
    def test_add_two_numbers(self):
        self.assertEqual(3, add(1, 2))
