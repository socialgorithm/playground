import random
import tkinter
from threading import Thread

import sympy as sy
from model.utility.vector import Vector
from model.insect import Insect
from sympy.core.cache import *

from model2.car import Car
from model2.track import Track


class Environment:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.track = Track(self.track_raw_data)
        self.cars = []
        self.simStep = 0


    def simSteps(self, canvas: tkinter.Canvas, num_steps=1):
        print("Step: {}".format(self.simStep))
        self.simStep += 1



    def draw(self, canvas: tkinter.Canvas):
        # drawing the track
        self.track.draw(canvas, redraw=False, draw_section_segments=True)
