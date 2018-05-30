import tkinter as tk
from threading import Thread

from model2.car import Car
from model2.environment import Environment


class SimUI:

    def __init__(self, populationSize, width=800, height=800):
        self.width = width
        self.height = height
        self.populationSize = populationSize
        self.environment: Environment = Environment(width, height)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=width, width=height)
        self.canvas.configure(background='green')
        self.canvas.pack()
        self.population_genome = []
        self.insects = []
        self.drawn = False

    def run(self):
        # generating initial population
        for i in range(self.populationSize):
            self.insects.append(Car(genGenome=True))
        self.population_genome = [insec.genome for insec in self.insects]
        self.environment.setCars(self.insects)
        thread = Thread(target=self.sim)
        thread.start()
        self.root.mainloop()

    def sim(self):
        while True:
            self.environment.simSteps(self.canvas)

if __name__ == "__main__":
    sim = SimUI(25)
    sim.run()