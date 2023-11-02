import unittest

def greet():
    return "Hello World"

class GreeterGreetTest(unittest.TestCase):
    def test_no_args(self):
        """greets the world, given no arguments"""
        self.assertEquals(greet(), "Hello World")
