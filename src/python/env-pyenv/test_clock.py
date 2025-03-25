#!/usr/bin/env python3

import unittest

import clock


class TestClock(unittest.TestCase):
    def test_current_time(self):
        self.assertIsNotNone(clock.current_time())

if __name__ == '__main__':
    unittest.main()
