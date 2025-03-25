import sys

from greeter import Greeter


def main():
    greeter = Greeter()
    print("{}".format(greeter.make_greeting()))
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
