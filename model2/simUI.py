import tkinter as tk
from threading import Thread

from model2.car import Car
from model2.environment import Environment
from model2.track import Track
from multiprocessing import Process, Queue
import multiprocessing as mp

from model2.updater import updateLoop


class SimUI:

    def __init__(self, populationSize, updaters, in_queues, out_queues, width=800, height=800, num_procs=4):
        self.width = width
        self.height = height
        self.populationSize = populationSize
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=width, width=height)
        self.canvas.configure(background='green')
        self.canvas.pack()
        self.in_queues = in_queues
        self.out_queues = out_queues
        ########################################################################################################################
        # Creating simulation environment
        ########################################################################################################################
        self.population_genome = []
        self.cars = []
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

    def __reduce__(self):
        return (self.__class__)

    def sim(self):
        while True:
            for v in range(4):
                print("MAIN: put to proc {}".format(v))
                self.in_queues[v].put(1, block=True)
            for ind, q in enumerate(self.out_queues):
                print("MAIN: get from proc {}".format(ind))
                print(q.get(block=True))


if __name__ == "__main__":
    ########################################################################################################################
    # creating updater processes
    ########################################################################################################################
    mp.set_start_method('spawn')
    num_procs = 4
    processes = []
    in_queues = []
    out_queues = []
    populationSize = 20
    cars = []
    # generating initial population
    for i in range(populationSize):
        cars.append(Car(tag=str(i), genGenome=True))
    # creating updater processes
    proc_car_lst = []
    for i in range(num_procs):
        proc_car_lst.append([])
    proc_car_lst_index = 0  # what updater process to assign the current car to
    for i in range(populationSize):
        if proc_car_lst_index == num_procs:
            proc_car_lst_index = 0
        proc_car_lst[proc_car_lst_index].append(cars[i])
        proc_car_lst_index += 1
    # creating processes
    for i in range(num_procs):
        in_queue = Queue(maxsize=1)
        out_queue = Queue(maxsize=len(proc_car_lst[i]))
        process = Process(target=updateLoop, args=([car.genome for car in cars], in_queue, out_queue, i))
        processes.append(process)
        in_queues.append(in_queue)
        out_queues.append(out_queue)
        process.start()
    # starting simulation controller
    sim = SimUI(25, processes, in_queues, out_queues)
    sim.run()