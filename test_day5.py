#!/usr/bin/env python
#
#  Unit tests for day5.py
#
import unittest
import day5

class TestIsNice(unittest.TestCase):
    def test_is_nice(self):
        cases = [
            ('ugknbfddgicrmopn', True),
            ('aaa', True),
            ('jchzalrnumimnmhp', False),
            ('haegwjzuvuyypxyu', False),
            ('dvszwmarrgswjxmb', False),
            ('aeioou', True),
            ('bbiouu', True)
        ]

        for word, expected in cases:
            result = day5.is_nice(word)
            print result, word
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
