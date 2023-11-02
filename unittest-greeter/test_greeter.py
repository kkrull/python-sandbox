import unittest

class GreeterGreetTest(unittest.TestCase):
    def test_no_args(self):
        self.assertEquals(greet(), "Hello World")
