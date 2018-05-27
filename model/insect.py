import random
import tkinter

from sympy import *
from model.utility.vector import Vector
from model.genome import Genome


class Insect:

    def __init__(self,genGenome = False):
        self.position = None
        self.sensorInput = []  # should be fixed size
        self.vector = None
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
        else:
            self.genome = None

    def setGenome(self, genome):
        self.genome = genome

    def update(self, food_coords: list ):
        # check if intersecting food coordinates
        insect_body = Ellipse(centre=self.position, hradius=10, vradius=10)
        food_to_remove = []
        for food in food_coords:
            intersec = intersection(food, insect_body)
            if len(intersec) > 0:
                self.fitness += 1
                food_to_remove.append(food)
        for to_remove in food_to_remove:
            food_coords.remove(to_remove)
        # vector
        # TODO implement
        # updating position
        self.position = Point2D(self.position.x + self.vector.x, self.position.y + self.vector.y)

    def draw(self, canvas: tkinter.Canvas):
        x0, y0 = int(self.position.x) - 5, int(self.position.y) - 5
        x1, y1 = int(self.position.x) + 5, int(self.position.y) + 5
        canvas.create_oval(x0, y0, x1, y1, fill='red', width=0)


