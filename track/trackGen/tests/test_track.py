import unittest
import sympy as sy
from track.trackGen.track import Track

class TestTrack(unittest.TestCase):

    def test_smooth(self):
        list_initial = [sy.Point2D(0, 0), sy.Point2D(0, 10), sy.Point2D(0, 20), sy.Point2D(0, 30)]
        expected = [sy.Point2D(0, 0), sy.Point2D(0, 5), sy.Point2D(0, 10),
                           sy.Point2D(0, 15), sy.Point2D(0, 20), sy.Point2D(0, 25),
                           sy.Point2D(0, 30)]
        self.assertEqual(Track._smooth(list_initial), expected)

    def test_smooth2(self):
        list_initial = [sy.Point2D(10, 10), sy.Point2D(20, 20), sy.Point2D(30, 30)]
        expected = [sy.Point2D(10, 10), sy.Point2D(15, 15),
                    sy.Point2D(20, 20), sy.Point2D(25, 25),
                    sy.Point2D(30, 30)]
        self.assertEqual(Track._smooth(list_initial), expected)

    def test_smooth3(self):
        list_initial = [sy.Point2D(30, 30), sy.Point2D(20, 20), sy.Point2D(10, 10)]
        expected = [sy.Point2D(30, 30), sy.Point2D(25, 25),
                    sy.Point2D(20, 20), sy.Point2D(15, 15),
                    sy.Point2D(10, 10)]
        self.assertEqual(Track._smooth(list_initial), expected)