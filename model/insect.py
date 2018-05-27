from sympy import *


class Insect:

    def __init__(self, starting_position: Point2D):
        self.position = starting_position
        self.sensorInput = []  # should be fixed size

    def update(self,environment):
        pass

    def draw(self):
        pass


