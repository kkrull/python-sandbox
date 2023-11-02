import unittest

def greet(name="World"):
    return "Hello %s" % (name)

class GreeterGreetTest(unittest.TestCase):
    def test_no_args(self):
        """greets the world, given no arguments"""
        self.assertEqual(greet(), "Hello World")

    def test_name(self):
        """greets a person, given a name"""
        self.assertEqual(greet("George"), "Hello George")
