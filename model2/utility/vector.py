import math


class Vector:

    def __init__(self):
        self.x = None
        self.y = None
        self.deg = None
        self.mag = None
        self.rad = None

    def setXY(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.mag = (self.x**2 + self.y**2)**(1/2)
        self.rad = math.atan2(self.y, self.x)
        self.deg = self.rad * (180/math.pi)
        return self

    def setMagDeg(self, mag, deg):
        if mag <= 0:
            raise ValueError("magnitude cannot be <= 0")
        self.mag = float(mag)
        self.deg = float(deg)
        if self.deg > 0:
            _num = math.floor(self.deg / 360)
            self.deg -= _num*360
        elif self.deg < 0:
            self.deg += math.floor(math.fabs(self.deg)/360)*360
        self.rad = self.deg * (math.pi / 180)
        self.x = self.mag * math.cos(self.rad)
        self.y = self.mag * math.sin(self.rad)
        return self

    def addDeg(self, deg):
        self.deg += deg
        self.setMagDeg(self.mag, self.deg)

    def clockwiseAngleDeg(self, vec2: 'Vector'):
        dot = self.x * vec2.x + self.y * vec2.y  # dot product between [x1, y1] and [x2, y2]
        det = self.x * vec2.y - self.y * vec2.x  # determinant
        angle = math.atan2(det, dot) * (180/math.pi)
        return angle