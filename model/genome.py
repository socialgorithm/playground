import math

from gene import Gene
import random

class Genome:

    def __init__(self):
        self.genes: dict['Gene'] = {}
        self.fitness = None
        self.mutation_rate = 0.05

    def new_gene(self, size: int, value_bounds: tuple, name: str):
        if name in self.genes:
            raise Exception("gene with this name already present in genome !")
        val_plusminus = math.fabs(value_bounds[0] - value_bounds[1])/2
        val_midpoint = value_bounds[0] + val_plusminus
        new_values = []
        for i in range(size):
            sign = 1 if random.random() >= 0.5 else -1
            val = val_midpoint + sign*val_plusminus*random.random()
            new_values.append(val)
        new_gene = Gene(val_type=float,geneID=name,initial_values=new_values,value_bounds=(value_bounds[0],value_bounds[1]))
        self.genes[name] = new_gene

    def add_gene(self, gene: Gene, name: str):
        if name in self.genes:
            raise Exception("gene with this name already present in genome !")
        self.genes[name] = gene

    def mutate(self):
        for gene_name in self.genes:
            self.genes[gene_name].mutate(self.mutation_rate)

    def reproduce(self, otherGenome: 'Genome'):
        genome_child1 = Genome()
        genome_child2 = Genome()
        for gene_name in self.genes:
            # crossover and add genes to children
            new_gene1, new_gene2 = self.genes[gene_name].crossover_singlepoint(otherGenome.genes[gene_name])
            genome_child1.add_gene(new_gene1, gene_name)
            genome_child2.add_gene(new_gene2, gene_name)
        # mutate child genome
        genome_child1.mutate()
        genome_child2.mutate()
        return genome_child1,genome_child2
