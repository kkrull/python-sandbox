#!/usr/bin/env python

from setuptoolsflat.greeting import make_greeting

def main():
    version = read_version()
    print(f"Marvin version {version}")
    print(make_greeting())

def read_version():
    return "Q.38"

if __name__ == '__main__':
    main()
