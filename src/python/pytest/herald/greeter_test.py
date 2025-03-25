import os
import re

from . import greeter


class TestGreeter:
    def test_greet_with_no_name(self):
        subject = greeter.Greeter()
        assert subject.greet() == 'Hello world!'

    def test_greet_with_a_static_name(self):
        subject = greeter.Greeter()
        assert subject.greet('George') == 'Hello George!'

    def test_greet_with_a_secret_name(self):
        assert 'GREETER_NAME' in os.environ, "Missing environment variable: GREETER_NAME"
        name = os.environ['GREETER_NAME']

        subject = greeter.Greeter()
        assert re.match('Hello .+!', subject.greet(name))
