import random
import tkinter

import sympy as sy
from model.utility.vector import Vector
from model.insect import Insect


class Environment:

    def __init__(self, width: int, height: int, num_food=500):
        self.width = width
        self.height = height
        self.num_food = num_food
        self.food = []
        self.insects = []
        self.generateFood(num_food, width, height)

    def generateFood(self, num_food, width, height):
        self.food.clear()
        seenCoords = []
        for i in range(num_food):
            coords = (None, None)
            point = None
            while True:
                coords = (random.randrange(0, width), random.randrange(0, height))
                point = sy.Point2D(coords[0], coords[1])
                if coords not in seenCoords:
                    seenCoords.append(coords)
                    self.food.append(point)
                    break

    def setInsects(self, insects: list):
        self.insects.clear()
        self.insects.extend(insects)
        # setting starting point and vector
        startingPoint = sy.Point2D(int(self.width/2),int(self.height/2))
        for insect in self.insects:
            insect.position = startingPoint
            insect.vector = Vector().setMagDeg(25, random.randrange(0, 360))

    def simSteps(self,num=1):
        for step in range(num):
            for index,insect in enumerate(self.insects):
                insect.update(self.food)

    def draw(self, canvas: tkinter.Canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill='black', width=0)
        for food in self.food:
            x0, y0 = food.x - 1, food.y - 1
            x1, y1 = food.x + 1, food.y + 1
            canvas.create_oval(x0, y0, x1, y1, fill='green', width=0)
        for insect in self.insects:
            insect.draw(canvas)

