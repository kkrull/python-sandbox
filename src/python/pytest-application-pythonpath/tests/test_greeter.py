import pytest
from greeter import Greeter


class TestGreeter:

    def test_make_greeting_greets_world(self):
        subject = Greeter()
        assert subject.make_greeting() == "Hello World!"

    def test_make_greeting_greets_by_name(self):
        subject = Greeter()
        assert subject.make_greeting("George") == "Hello George!"
