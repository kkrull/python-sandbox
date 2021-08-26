import pytest
from greeter import Greeter

class TestGreeter:
    def test_make_greeting(self):
        subject = Greeter()
        assert subject.make_greeting() == "Hello World!"