import random
import tkinter
from threading import Thread

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
        self.firstDrawCall = True
        self.food_to_remove = []

    def generateFood(self, num_food, width, height):
        self.food.clear()
        seenCoords = []
        for i in range(num_food):
            coords = (None, None)
            point = None
            while True:
                coords = (random.randrange(0, width), random.randrange(0, height))
                point = sy.Point(coords[0], coords[1])
                if coords not in seenCoords:
                    seenCoords.append(coords)
                    self.food.append(point)
                    break

    def setInsects(self, insects: list):
        self.insects.clear()
        self.insects.extend(insects)
        # setting starting point and vector
        startingPoint = sy.Point(int(self.width/2),int(self.height/2))
        for insect in self.insects:
            insect.position = startingPoint
            insect.vector = Vector().setMagDeg(5, random.randrange(0, 360))

    def simSteps(self, num_steps=1, num_threads=4):
        print("starting updates")
        thread_insect_lists = []
        threads = []
        for num in range(num_threads):
            insect_list = []
            thread_insect_lists.append(insect_list)
            threads.append(Thread(target=self.updateInsects, args=(insect_list, num_steps,)))
        thread_index = 0
        counter = len(self.insects)
        while counter > 0:
            counter -= 1
            thread_insect_lists[thread_index].append(self.insects[counter])
            thread_index += 1
            if thread_index >= num_threads:
                thread_index = 0
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("food remaining: {}".format(len(self.food)))
        print("all ended")


    def updateInsects(self, insects: list, num_steps):
        for step in range(num_steps):
            for index, insect in enumerate(insects):
                insect.update(self.food)

    def draw(self, canvas: tkinter.Canvas):
        if self.firstDrawCall:
            canvas.create_rectangle(0, 0, self.width, self.height, fill='black', width=0)
            self.firstDrawCall = False
            for food in self.food:
                x0, y0 = food.x - 1, food.y - 1
                x1, y1 = food.x + 1, food.y + 1
                canvas.create_oval(x0, y0, x1, y1, fill='green', width=0)
        for insect in self.insects:
            insect.undraw(canvas)
        for insect in self.insects:
            insect.draw(canvas)

