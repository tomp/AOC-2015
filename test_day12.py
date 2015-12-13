#!/usr/bin/env python
#
#  Unit tests for day5.py
#
import unittest
import day12

class TestDay12(unittest.TestCase):
    def test_extract_numbers(self):
        cases = [
            ('[1,2,3]', (3, 6)),
            ('{"a":2,"b":4}', (2, 6)),
            ('[[[3]]]', (1, 3)),
            ('{"a":{"b":4},"c":-1}', (2, 3)),
            ('{"a":[-1,1]}', (2, 0)),
            ('[-1,{"a":1}]', (2, 0)),
            ('[]', (0, 0)),
            ('{}', (0, 0)),
        ]

        for text, expected in cases:
            exp_count, exp_sum = expected
            numbers = day12.extract_numbers(text)
            self.assertEqual(len(numbers), exp_count,
                    "Count for '{}' was {}".format(text, len(numbers)))
            self.assertEqual(sum(numbers), exp_sum,
                    "Count for '{}' was {}".format(text, len(numbers)))

if __name__ == '__main__':
    unittest.main()
