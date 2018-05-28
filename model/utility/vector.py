import math


class Vector:

    def __init__(self):
        self.x = None
        self.y = None
        self.deg = None
        self.mag = None
        self.rad = None

    def setXY(self, x, y):
        self.x = x
        self.y = y
        self.mag = math.sqrt(x**2 + y**2)
        self.rad = math.atan2(y, x)
        self.deg = self.rad * (180/math.pi)
        return self

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
        self.x = mag * math.cos(self.rad)
        self.y = mag * math.sin(self.rad)
        return self

    def addDeg(self, deg):
        self.deg += deg
        self.setMagDeg(self.mag, self.deg)

    def clockwiseAngleDeg(self, vec2: 'Vector'):
        dot = self.x * vec2.x + self.y * vec2.y  # dot product between [x1, y1] and [x2, y2]
        det = self.x * vec2.y - self.y * vec2.x  # determinant
        angle = math.atan2(det, dot) * (180/math.pi)
        return angle