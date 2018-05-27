import math


class Vector:

    def __init__(self):
        self.x = None
        self.y = None
        self.deg = None
        self.mag = None
        self.rad = None

    def setXY(self, x, y):
        raise Exception("Not implemented")

    def setMagDeg(self, mag, deg):
        if mag <= 0:
            raise ValueError("magnitude cannot be <= 0")
        self.mag = mag
        self.deg = deg
        if self.deg > 0:
            _num = math.floor(deg / 360)
            self.deg -= _num*360
        elif self.deg < 0:
            self.deg += math.floor(math.fabs(deg)/360)*360
        self.rad = self.deg * (math.pi / 180)
        self.x = mag * math.cos(deg)
        self.y = mag * math.sin(deg)
        return self

    def addDeg(self):
        raise Exception("Not implemented")