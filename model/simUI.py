import tkinter as tk

from model.environment import Environment
from model.insect import Insect


class SimUI:

    def __init__(self, populationSize, width=800, height=800):
        self.width = width
        self.height = height
        self.populationSize = populationSize
        self.environment: Environment = Environment(width, height, 100)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=width, width=height)
        self.canvas.pack()
        self.population_genome = []
        self.insects = []
        self.drawn = False

    def run(self):
        # generating initial population
        for i in range(self.populationSize):
            self.insects.append(Insect(genGenome=True))
        self.population_genome = [insec.genome for insec in self.insects]
        self.environment.setInsects(self.insects)
        self.nextStep()
        self.root.mainloop()

    def nextStep(self):
        self.environment.simSteps()
        self.environment.draw(self.canvas)
        self.root.after(1000, self.nextStep)


if __name__ == "__main__":
    sim = SimUI(100)
    sim.run()