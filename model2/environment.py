import random
import tkinter
from threading import Thread

import sympy as sy
from model.utility.vector import Vector
from model.insect import Insect
from sympy.core.cache import *


class Environment:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.track = [
            {'outer': (20, 400), 'inner': (80, 400)},
            {'outer': (20, 20), 'inner': (80, 80)},
            {'outer': (780, 20), 'inner': (700, 80)},
            {'outer': (780, 780), 'inner': (700, 700)},
            {'outer': (20, 780), 'inner': (80, 700)},
            {'outer': (20, 780), 'inner': (80, 700)},
        ]
        self.cars = []
        self.isFirstDrawCall = True
        self.simStep = 0

    def simSteps(self, canvas: tkinter.Canvas, num_steps=1, num_threads=4):
        thread_car_lists = []
        threads = []
        # creating the specified number of threads that will be used for updating the cars
        for num in range(num_threads):
            car_list = []
            thread_car_lists.append(car_list)
            threads.append(Thread(target=self.updateCars, args=(car_list, num_steps,)))
        thread_index = 0
        counter = len(self.cars)
        # assigning cars to threads
        while counter > 0:
            counter -= 1
            thread_car_lists[thread_index].append(self.cars[counter])
            thread_index += 1
            if thread_index >= num_threads:
                thread_index = 0
        # starting update
        for thread in threads:
            thread.start()
        # waiting for all car updates to complete
        for thread in threads:
            thread.join()
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
        if self.isFirstDrawCall:
            for index in range(len(self.track)):
                # making sure the track is closed
                coord_pairs = self.track[index]
                if index < len(self.track) - 1:
                    next_pair = self.track[index + 1]
                else:
                    next_pair = self.track[0]
                canvas.create_line(coord_pairs['outer'][0], coord_pairs['outer'][1],
                                   next_pair['outer'][0], next_pair['outer'][1],
                                   fill="Black")
                canvas.create_line(coord_pairs['inner'][0], coord_pairs['inner'][1],
                                   next_pair['inner'][0], next_pair['inner'][1],
                                   fill="Black")
                x1, y1 = (coord_pairs['inner'][0] - 5), (coord_pairs['inner'][1] - 5)
                x2, y2 = (coord_pairs['inner'][0] + 5), (coord_pairs['inner'][1] + 5)
                canvas.create_oval(x1, y1, x2, y2, fill='red')
                x1, y1 = (coord_pairs['outer'][0] - 5), (coord_pairs['outer'][1] - 5)
                x2, y2 = (coord_pairs['outer'][0] + 5), (coord_pairs['outer'][1] + 5)
                canvas.create_oval(x1, y1, x2, y2, fill='red')
            self.isFirstDrawCall = False
