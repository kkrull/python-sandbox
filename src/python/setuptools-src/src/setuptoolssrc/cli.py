#!/usr/bin/env python

from setuptoolssrc.greeting import make_greeting
from setuptoolssrc.marvin import suite_version


def main():
    print(f"Version: {suite_version()}")
    print(make_greeting())

if __name__ == '__main__':
    main()
