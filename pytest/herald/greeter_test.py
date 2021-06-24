from . import greeter

class TestGreeter:
    def test_greet_with_no_name(self):
        subject = greeter.Greeter()
        assert subject.greet() == 'Hello world!'

    def test_greet_with_a_name(self):
        subject = greeter.Greeter()
        assert subject.greet('George') == 'Hello George!'
