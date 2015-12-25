#!/usr/bin/env python
#
#  Unit tests for day6.py
#
import unittest
import day6

class TestLightArray(unittest.TestCase):
    def test_basic_methods(self):
        w, h = 5, 5
        maxx, maxy = w-1, h-1

        arr = day6.LightArray(w, h)
        self.assertEqual(arr.count_on(), 0)

        arr.set_region((0, 0), (maxx, maxy), True)
        self.assertEqual(arr.count_on(), w*h)

        arr.set_region((0, 0), (maxx, maxy), False)
        self.assertEqual(arr.count_on(), 0)

        arr.set_region((0,0), (0,maxy), True)
        self.assertEqual(arr.count_on(), h)

        arr.set_region((maxx,0), (maxx,maxy), True)
        self.assertEqual(arr.count_on(), 2*h)

        arr.set_region((0,0), (maxx,0), True)
        self.assertEqual(arr.count_on(), 2*h + w-2)

        arr.set_region((0,maxy), (maxx,maxy), True)
        self.assertEqual(arr.count_on(), 2*h + 2*w -4)

        arr.toggle_region((0,0), (maxx,maxy))
        self.assertEqual(arr.count_on(), (h-2)*(w-2))

if __name__ == '__main__':
    unittest.main()
