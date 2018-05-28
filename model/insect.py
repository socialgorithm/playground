import random
import tkinter
import math
from sympy import *
import numpy as np
from model.brain import InsectBrain
from model.utility.vector import Vector
from model.genome import Genome
from random import random as fran

class Insect:

    def __init__(self, genGenome = False):
        self.position = None
        self.prevPosition = None
        self.sensorInput = []  # should be fixed size
        self.vector = None
        self.brain: InsectBrain = None
        self.fitness = 0
        self.canvas_sphere = None
        self.canvas_line = None
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
            self.brain: InsectBrain = InsectBrain(self.genome)
        else:
            self.genome = None

    def setGenome(self, genome):
        self.genome = genome
        self.brain: InsectBrain = InsectBrain(genome)

    def update(self, food_coords: list ):
        # check if intersecting food coordinates
        food_to_remove = []
        for food in food_coords:
            # approximating insect body as a square, cannot use sympy due to bug
            intersects = False
            if (int(self.position.x) - 5) <= food.x <= (int(self.position.x) + 5):
                if (int(self.position.y) - 5) <= food.y <= (int(self.position.y) + 5):
                    intersects = True
            if intersects:
                self.fitness += 1
                print("nam nam nam")
                food_to_remove.append(food)
        for to_remove in food_to_remove:
            food_coords.remove(to_remove)
        # sensors
        sensor_input = [0, 0, 0, 0, 0]
        SENSOR_RANGE = 50
        for food in food_coords:
            delta_x = food.x - int(self.position.x)
            delta_y = food.y - int(self.position.y)
            vec_to_food = Vector().setXY(delta_x, delta_y)
            if vec_to_food is None:
                continue
            if vec_to_food.mag > SENSOR_RANGE:
                continue
            angle = self.vector.clockwiseAngleDeg(vec_to_food)
            #print("ANGLE: {}".format(angle))
            sensor_val = SENSOR_RANGE - float(vec_to_food.mag)/SENSOR_RANGE
            if -90 >= angle < -45.5:
                sensor_input[0] += sensor_val
            elif -45.5 >= angle < -22.5:
                sensor_input[1] += sensor_val
            elif -22.5 >= angle < 0 or 0 >= angle < 22.5:
                sensor_input[2] += sensor_val
            elif 22.5 >= angle < 45:
                sensor_input[3] += sensor_val
            elif 45 >= angle < 90:
                sensor_input[4] += sensor_val
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



