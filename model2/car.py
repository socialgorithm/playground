import random
import tkinter
import math
from sympy import *
import numpy as np
from model.utility.vector import Vector
from model.genome import Genome
from model2.brain import CarBrain


class Car:

    def __init__(self, genGenome = False):
        self.position = None
        self.prevPosition = None
        self.sensorInput = []  # should be fixed size
        self.vector = None
        self.brain: CarBrain = None
        self.fitness = 0
        self.canvas_sphere = None
        self.canvas_line = None
        self.track = None
        # create random genome
        if genGenome:
            self.genome = Genome()
            self.genome.new_gene(size=25, value_bounds=(-1, 1), name="W_inputs")
            self.genome.new_gene(size=5, value_bounds=(-1, 1), name="B_inputs")
            self.genome.new_gene(size=25, value_bounds=(-1, 1), name="W_one")
            self.genome.new_gene(size=5, value_bounds=(-1, 1), name="B_one")
            self.genome.new_gene(size=25, value_bounds=(-1, 1), name="W_two")
            self.genome.new_gene(size=5, value_bounds=(-1, 1), name="B_two")
            self.genome.new_gene(size=5, value_bounds=(-1, 1), name="W_out")
            self.genome.new_gene(size=1, value_bounds=(-1, 1), name="B_out")
            self.brain: CarBrain = CarBrain(self.genome)
        else:
            self.genome = None

    def setGenome(self, genome):
        self.genome = genome
        self.brain: CarBrain = CarBrain(genome)

    def update(self, track_coords: list ):
        # check if car has collided with track
        if self.track is None:
            pass
        # sensors
        sensor_input = [0, 0, 0, 0, 0]
        SENSOR_RANGE = 50

        # normalize sensor output
        max_sensor_val = None
        min_sensor_val = None
        for val in sensor_input:
            if max_sensor_val is None or val > max_sensor_val:
                max_sensor_val = float(val)
            if min_sensor_val is None or val < min_sensor_val:
                min_sensor_val = float(val)
        max_sensor_val -= min_sensor_val
        for index, val in enumerate(sensor_input):
            if max_sensor_val == 0:
                continue
            sensor_input[index] = (val-min_sensor_val)/max_sensor_val
        steering = self.brain.evaluate(np.array(sensor_input).reshape(1, 5))
        delta_angle = 10*steering
        #print("Sensor: {} deltaDeg: {}".format([round(val, 1) for val in sensor_input], delta_angle))
        self.vector.addDeg(delta_angle)
        # updating position
        self.prevPosition = self.position
        self.position = Point(int(self.position.x) + int(self.vector.x), int(self.position.y) + int(self.vector.y))


    # def undraw(self, canvas: tkinter.Canvas):
    #     if self.prevPosition is None:
    #         return
    #     x0, y0 = int(self.prevPosition.x) - 5, int(self.prevPosition.y) - 5
    #     x1, y1 = int(self.prevPosition.x) + 5, int(self.prevPosition.y) + 5
    #     canvas.create_oval(x0, y0, x1, y1, fill='black', width=0)

    def draw(self, canvas: tkinter.Canvas):
        if self.position is None:
            return
        x0, y0 = int(self.position.x) - 5, int(self.position.y) - 5
        x1, y1 = int(self.position.x) + 5, int(self.position.y) + 5
        if self.canvas_sphere is None:
            self.canvas_sphere = canvas.create_oval(x0, y0, x1, y1, fill='blue', width=0)
        if self.canvas_line is not None:
            canvas.delete(self.canvas_line)
        self.canvas_line = canvas.create_line(int(self.position.x), int(self.position.y),
                               int(self.position.x) + int(self.vector.x),
                               int(self.position.y) + int(self.vector.y), fill="yellow")
        canvas.coords(self.canvas_sphere, x0, y0, x1, y1)



