from greeter import Greeter


class TestGreeter:
    def test_greet_with_no_name(self):
        subject = Greeter()
        assert subject.greet() == 'Hello world!'

    def test_greet_with_a_static_name(self):
        subject = Greeter()
        assert subject.greet('George') == 'Hello George!'
