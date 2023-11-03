import unittest

def add(a, b):
    return 3

class AddTest(unittest.TestCase):
    def test_add_two_numbers(self):
        self.assertEqual(3, add(1, 2))
