import random
import tkinter
import math
from sympy import *
import numpy as np
from model.utility.vector import Vector
from model2.genome import Genome
from model2.brain import CarBrain


class Car:

    def __init__(self, tag, genGenome = False):
        self.position = None
        self.prevPosition = None
        self.sensorInput = []  # should be fixed size
        self.movement_vector = None
        self.sensor_vectors = []
        self.brain: CarBrain = None
        self.fitness = 0
        self.canvas_sphere = None
        self.canvas_line = None
        self.track = None
        self.tag = tag  # used to identify the car
        # create random genome
        if genGenome:
            self.genome = Genome(tag)
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

    def update(self):
        SENSOR_RANGE = 100
        # update the cars sensor vectors based on the movement vector
        sens_neg90 = self.movement_vector.clone()
        sens_neg90.addDeg(-90)
        sens_neg90.setMag(SENSOR_RANGE)
        sens_neg45 = self.movement_vector.clone()
        sens_neg45.addDeg(-45)
        sens_neg45.setMag(SENSOR_RANGE)
        sens_pos0 = self.movement_vector.clone()
        sens_pos0.setMag(SENSOR_RANGE)
        sens_pos45 = self.movement_vector.clone()
        sens_pos45.addDeg(+45)
        sens_pos45.setMag(SENSOR_RANGE)
        sens_pos90 = self.movement_vector.clone()
        sens_pos90.addDeg(+90)
        sens_pos90.setMag(SENSOR_RANGE)
        self.sensor_vectors = [sens_neg90, sens_neg45, sens_pos0, sens_pos45, sens_pos90]
        # TODO convert sensor vectors to segments
        # TODO check where sensor segments intersect with track and get shortest distance as sensor input
        # TODO send sensor distances back with return data.
        




