import random
import tkinter
from threading import Thread

import sympy as sy
from model.utility.vector import Vector
from model.insect import Insect
from sympy.core.cache import *

from model2.track import Track


class Environment:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.track_raw_data = [
            {'outer': (20, 400), 'inner': (80, 400)},
            {'outer': (20, 20), 'inner': (80, 80)},
            {'outer': (780, 20), 'inner': (700, 80)},
            {'outer': (780, 780), 'inner': (700, 700)},
            {'outer': (20, 780), 'inner': (80, 700)},
            {'outer': (20, 780), 'inner': (80, 700)},
        ]
        self.track = Track(self.track_raw_data)
        self.cars = []
        self.isFirstDrawCall = True
        self.simStep = 0

    def simSteps(self, canvas: tkinter.Canvas, num_steps=1, num_threads=4):
        print("Step: {}".format(self.simStep))
        self.simStep += 1
        # updating the canvas with the new car positions
        self.draw(canvas)

    def setCars(self, cars):
        pass

    def updateCars(self, insects: list, num_steps):
        pass

    def draw(self, canvas: tkinter.Canvas):
        # drawing the track
        self.track.draw(canvas, redraw=False, draw_section_segments=True)
