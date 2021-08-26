import pytest

class Greeter:
    def make_greeting(self):
        return "Hello World!"

class TestGreeter:
    def test_make_greeting(self):
        subject = Greeter()
        assert subject.make_greeting() == "Hello World!"