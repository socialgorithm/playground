import random
import tkinter

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
        #insect_body = Ellipse(Point(self.position.x, self.position.y), hradius=10, vradius=10)
        food_to_remove = []
        for food in food_coords:
            #intersects = insect_body.encloses_point(food) #TODO buggy, issues with thread lock
            intersects = False
            if (self.position.x - 5) <= food.x <= (self.position.x + 5):
                if (self.position.y - 5) <= food.y <= (self.position.y + 5):
                    intersects = True
            if intersects:
                self.fitness += 1
                print("nam nam nam")
                food_to_remove.append(food)
        for to_remove in food_to_remove:
            food_coords.remove(to_remove)
        # vector
        steering = self.brain.evaluate(np.array([fran(), fran(), fran(), fran(), fran()]).reshape(1, 5))
        delta_angle = 10*steering
        self.vector.addDeg(delta_angle)
        # updating position
        self.prevPosition = self.position
        try:
            self.position = Point(self.position.x + self.vector.x, self.position.y + self.vector.y)
        except:
            print("error during update")

    def undraw(self, canvas: tkinter.Canvas):
        if self.prevPosition is None:
            return
        x0, y0 = int(self.prevPosition.x) - 5, int(self.prevPosition.y) - 5
        x1, y1 = int(self.prevPosition.x) + 5, int(self.prevPosition.y) + 5
        canvas.create_oval(x0, y0, x1, y1, fill='black', width=0)

    def draw(self, canvas: tkinter.Canvas):
        if self.position is None:
            return
        x0, y0 = int(self.position.x) - 5, int(self.position.y) - 5
        x1, y1 = int(self.position.x) + 5, int(self.position.y) + 5
        canvas.create_oval(x0, y0, x1, y1, fill='blue', width=0)
        canvas.create_line(int(self.position.x), int(self.position.y),
                           int(self.position.x) + int(self.vector.x),
                           int(self.position.y) + int(self.vector.y), fill="yellow")


