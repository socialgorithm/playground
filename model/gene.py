import math
import random
import copy


class Gene:

    def __init__(self, val_type: type,
                 geneID: str,
                 initial_values: list,
                 static_values: bool=False,
                 value_bounds: tuple=(0, 1)):
        """
        Represents the gene for a single property of the model. For example, a gene could represent the the weights
        for a single layer in a neural network

        :param val_type: the type of the values in this gene, e.g for weights it would be float
        :type val_type: type
        :param geneID: identifier for the gene. Only genes with the same identifier can be combined
        :type geneID: str
        :param initial_values: initial values of gene
        :type initial_values: list
        :param static_values: Should the values in the gene be unique ? If the values represent position of something [1,4,5,2,3,0] then we need to consider this during mutation and crossover etc because it would be nonsensical to have [1,5,5,5,3,3]. Setting this to true means the gene will maintain the same number of each element
        :type static_values: bool
        :param value_bounds: (maximum value, minimum value) or (maximum value, minimum value, delta), where delta is the maximum amount this value changes during mutation. if not set then delta will be 10% of value range
        :type value_bounds: tuple
        """
        self.val_type = val_type
        self.geneID = geneID
        self.unique_values = static_values
        self.values = initial_values
        self.value_bounds = value_bounds
        self.delta_max = None
        if static_values and value_bounds != (0, 1):
            raise ValueError("Setting value bounds when the gene contains unique values does not makes sense since the values will not change during mutation")
        elif not 2 <= len(value_bounds) <= 3:
            raise ValueError("value_bounds parameter should be a tuple of size 2 or 3, provided tuple {}".format(str(value_bounds)))
        elif len(value_bounds) == 2:
            self.delta_max = math.fabs(value_bounds[1] - value_bounds[0])*0.05 # val change due to mutation should be maximum 5% of val range
        elif len(value_bounds) == 3:
            self.delta_max = value_bounds[2]




    def mutate(self, mutation_rate: float):
        """
        method for mutating the gene. If values are static, then items in the list are switched with each other, if not
        then

        :param mutation_rate:
        :return:
        """

        if not 0 <= mutation_rate < 1:
            raise ValueError("Mutation chance should be in range 0 <= x < 1")
        # determine how many mutations to carry out
        num_mutations: int = 0
        while random.random() < mutation_rate and num_mutations < len(self.values):
            num_mutations += 1
        # unique values list, swap values around for mutation
        if self.unique_values:
            for mutation_num in range(0, num_mutations):
                # selecting two values to swap
                index_1 = random.randrange(0, len(self.values))
                index_2 = random.randrange(0, len(self.values))
                # swapping
                val_buffer = self.values[index_1]
                self.values[index_1] = self.values[index_2]
                self.values[index_2] = val_buffer
        else:
            for mutation_num in range(0, num_mutations):
                # selecting index to which to add or substract
                index = random.randrange(0, len(self.values))
                # choosing if to add or substract
                sign = 1 if random.random() >= 0.5 else -1
                # determining magnitude of change
                mag = self.delta_max*random.random()
                # updating value
                self.values[index] += sign*mag
                # enforce max and min bounds
                if self.values[index] < self.value_bounds[0]:
                    self.values[index] = self.value_bounds[0]
                elif self.values[index] > self.value_bounds[1]:
                    self.values[index] = self.value_bounds[1]

    def crossover_singlepoint(self, otherGene) -> tuple:
        """
        Generates two child genes by performing single point crossover with the parents genes (this instance and otherGene)

        :param otherGene: the second parent
        :type otherGene: Gene
        :return: returns a list with 2 items, each of them a result of the crossover
        """
        # checking that crossover can be performed with these two genes
        if otherGene.geneID != self.geneID:
            raise Exception("cannot perform crossover, geneIDs do not match!")
        child1_values = [None for i in range(len(self.values))]
        child2_values = [None for i in range(len(self.values))]
        crossover_index = random.randrange(0,len(self.values))
        child1_values[0:crossover_index] = self.values[0:crossover_index]
        child1_values[crossover_index:] = otherGene.values[crossover_index:]
        child2_values[0:crossover_index] = otherGene.values[0:crossover_index]
        child2_values[crossover_index:] = self.values[crossover_index:]
        gene_child1 = copy.deepcopy(self)
        gene_child1.values = child1_values
        gene_child2 = copy.deepcopy(self)
        gene_child2.values = child2_values
        return gene_child1, gene_child2
