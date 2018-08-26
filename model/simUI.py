import random
import tkinter as tk
from threading import Thread

from environment import Environment
from insect import Insect


class SimUI:

    def __init__(self, populationSize, width=800, height=800):
        self.width = width
        self.height = height
        self.populationSize = populationSize
        self.environment: Environment = Environment(width, height, populationSize*10)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=width, width=height)
        self.canvas.configure(background='black')
        self.canvas.pack()
        self.population_genome = []
        self.insects = []
        self.drawn = False

    def run(self):
        thread = Thread(target=self.sim)
        thread.start()
        self.root.mainloop()

    def sim(self):
        STEPS_PER_GENERATION = 250
        # generating initial population
        for i in range(self.populationSize):
            self.insects.append(Insect(genGenome=True))
        self.population_genome = [insec.genome for insec in self.insects]
        while True:
            self.canvas.delete("all")
            current_step = 0
            self.environment: Environment = Environment(self.width, self.height, self.populationSize*10)
            self.environment.setInsects(self.insects)
            while current_step < STEPS_PER_GENERATION:
                current_step = self.environment.simSteps(self.canvas)
            ########################################################################################################################
            # selection
            ########################################################################################################################
            # normalise insect fitness
            max_fitness = None
            min_fitness = None
            average_fitness = 0
            for insect in self.insects:
                fitness = insect.fitness
                average_fitness += fitness
                if max_fitness is None or max_fitness < fitness:
                    max_fitness = fitness
                if min_fitness is None or min_fitness > fitness:
                    min_fitness = fitness
            average_fitness /= len(self.insects)
            print("Average fitness: {}, Max fitness: {}, Min fitness: {}".format(average_fitness, max_fitness, min_fitness))
            max_fitness -= min_fitness
            # select parents based on fitness until enough children have been generated
            fitness_list = []
            cumu_val = 0
            for insect in self.insects:
                insect.fitness = float(insect.fitness - min_fitness)/max_fitness
                fitness_list.append((cumu_val, insect.genome))
                cumu_val += insect.fitness
            self.population_genome.clear()
            while len(self.population_genome) < self.populationSize:
                val1 = random.random() * cumu_val
                val2 = random.random() * cumu_val
                parent1 = None
                parent2 = None
                for index, fitness_genome_tuple in enumerate(fitness_list):
                    if index + 1 < len(fitness_list):
                        next_tuple = fitness_list[index+1]
                    else:
                        next_tuple = (cumu_val+10, fitness_genome_tuple[1])
                    if fitness_genome_tuple[0] <= val1 < next_tuple[0]:
                        parent1 = fitness_genome_tuple[1]
                    if fitness_genome_tuple[0] <= val2 < next_tuple[0]:
                        parent2 = fitness_genome_tuple[1]
                children = parent1.reproduce(parent2)
                # select one of the children
                child = children[random.randint(0, 1)]
                self.population_genome.append(child)
            ########################################################################################################################
            # generate new insects
            ########################################################################################################################
            self.insects.clear()
            for genome in self.population_genome:
                new_insect = Insect(genGenome=False)
                new_insect.setGenome(genome)
                self.insects.append(new_insect)






if __name__ == "__main__":
    sim = SimUI(15)
    sim.run()
