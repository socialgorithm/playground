import tkinter as tk
from threading import Thread

from model2.car import Car
from model2.environment import Environment
from model2.track import Track
from multiprocessing import Process, Queue
import multiprocessing as mp

from model2.updater import updateLoop


class SimUI:

    def __init__(self, populationSize, width=800, height=800, num_procs=5):
        self.width = width
        self.height = height
        self.populationSize = populationSize
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=width, width=height)
        self.canvas.configure(background='green')
        self.canvas.pack()
        ########################################################################################################################
        # creating updater processes
        ########################################################################################################################
        mp.set_start_method('spawn')
        self.processes = []
        self.in_queues = []
        self.out_queues = []
        self.cars = {}
        # generating initial population
        for i in range(populationSize):
            car = Car(tag=str(i), genGenome=True)
            self.cars[car.tag] = car
        # creating updater processes
        self.proc_car_lst = []
        for i in range(num_procs):
            self.proc_car_lst.append([])
        proc_car_lst_index = 0  # what updater process to assign the current car to
        for key in self.cars:
            if proc_car_lst_index == num_procs:
                proc_car_lst_index = 0
                self.proc_car_lst[proc_car_lst_index].append(self.cars[key])

            proc_car_lst_index += 1
        # creating processes
        for i in range(num_procs):
            in_queue = Queue(maxsize=1)
            out_queue = Queue(maxsize=len(self.proc_car_lst[i]))
            process = Process(target=updateLoop, args=([car.genome for car in self.proc_car_lst[i]],
                                                       in_queue, out_queue, i))
            self.processes.append(process)
            self.in_queues.append(in_queue)
            self.out_queues.append(out_queue)
            process.start()
        ########################################################################################################################
        # Creating simulation environment
        ########################################################################################################################
        self.population_genome = []
        self.track_raw_data = [
            {'outer': (20, 400), 'inner': (80, 400)},
            {'outer': (20, 20), 'inner': (80, 80)},
            {'outer': (780, 20), 'inner': (700, 80)},
            {'outer': (780, 780), 'inner': (700, 700)},
            {'outer': (20, 780), 'inner': (80, 700)},
            {'outer': (20, 780), 'inner': (80, 700)},
        ]
        self.track = Track(track_data=self.track_raw_data)

    def run(self):
        thread = Thread(target=self.sim)
        thread.start()
        self.root.mainloop()

    def sim(self):
        self.track.draw(self.canvas, draw_section_segments=True)
        while True:
            self.update()
            self.wait()

    def update(self):
        for in_queue in self.in_queues:
            in_queue.put(1)

    def wait(self):
        # wait for the update to finish on all processes and parse the output
        for out_queue in self.out_queues:
            return_dict = out_queue.get(block=True)
            for key in return_dict:
                pass



if __name__ == "__main__":
    sim = SimUI(20)
    sim.run()