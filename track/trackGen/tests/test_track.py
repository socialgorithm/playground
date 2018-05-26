import unittest
import sympy as sy
from track.trackGen.track import Track

class TestTrack(unittest.TestCase):

    def test_smooth(self):
        list = [sy.Point2D(0, 0), sy.Point2D(0, 1), sy.Point2D(0, 2), sy.Point2D(0, 3)]
        print(Track._smooth(list))