import unittest
from model.gene import Gene
from unittest.mock import patch


class TestGene(unittest.TestCase):

    def setUp(self):
        geneA_vals = ['A', 'B', 'C', 'D', 'E', 'F']
        self.geneA_u = Gene(val_type=str, geneID="test_gene", initial_values=geneA_vals, static_values=True)
        geneB_vals = ['B', 'F', 'C', 'A', 'D', 'E']
        self.geneB_u = Gene(val_type=str, geneID="test_gene", initial_values=geneB_vals, static_values=True)
        geneC_vals = [0, 1, 2, 3, 4, 5]
        self.geneC_u = Gene(val_type=str, geneID="test_gene2", initial_values=geneC_vals, static_values=True)
        geneD_vals = [0.3, 0.5, 0.2, 0.8, 0.98, 0.05]
        self.geneD = Gene(val_type=str, geneID="test_gene3", initial_values=geneD_vals)
        geneE_vals = [0.13, 0.1, 0.52, 0.98, 0.25, 0.65]
        self.geneE = Gene(val_type=str, geneID="test_gene3", initial_values=geneE_vals)

    @patch('model.gene.random.randrange')
    @patch('model.gene.random.random')
    def test_staticValues_mutation_1(self, mf_random, mf_randrange):
        # setup
        mf_randrange.side_effect = [0, 1, 1, 4]  # specifying swap indicies
        mf_random.side_effect = [0, 0, 1]  # determines how many swaps are done (2)
        expected_result = ['B', 'E', 'C', 'D', 'A', 'F']
        # test
        self.geneA_u.mutate(0.5)
        self.assertEqual(expected_result, self.geneA_u.values)

    @patch('model.gene.random.randrange')
    @patch('model.gene.random.random')
    def test_values_mutation_1(self, mf_random, mf_randrange):
        # setup
        mf_randrange.side_effect = [0, 2, 4]  # indices
        mf_random.side_effect = [0, 0, 0, 1,  # setting number of mutations
                                 0, 0.5,  # sign and magnitude of change to value
                                 0, 1,
                                 1, 1]
        expected_result = [0.275, 0.5, 0.15, 0.8, 1, 0.05]
        # test
        self.geneD.mutate(0.5)
        self.assertEqual(expected_result, [round(x, 3) for x in self.geneD.values])

    @patch('model.gene.random.randrange')
    @patch('model.gene.random.random')
    def test_values_mutation_2(self, mf_random, mf_randrange):
        # setup
        mf_randrange.side_effect = [0, 2, 4]  # indices
        expected_result_1_A = [0.13, 0.1, 0.52, 0.98, 0.25, 0.65]
        expected_result_1_B = [0.3, 0.5, 0.2, 0.8, 0.98, 0.05]
        expected_result_2_A = [0.3, 0.5,  0.52, 0.98, 0.25, 0.65]
        expected_result_2_B = [0.13, 0.1, 0.2, 0.8, 0.98, 0.05]
        expected_result_3_A = [0.3, 0.5, 0.2, 0.8, 0.25, 0.65]
        expected_result_3_B = [0.13, 0.1, 0.52, 0.98, 0.98, 0.05]
        # test
        genes = self.geneD.crossover_singlepoint(self.geneE)
        self.assertEqual(expected_result_1_A, genes[0].values)
        self.assertEqual(expected_result_1_B, genes[1].values)
        genes = self.geneD.crossover_singlepoint(self.geneE)
        self.assertEqual(expected_result_2_A, genes[0].values)
        self.assertEqual(expected_result_2_B, genes[1].values)
        genes = self.geneD.crossover_singlepoint(self.geneE)
        self.assertEqual(expected_result_3_A, genes[0].values)
        self.assertEqual(expected_result_3_B, genes[1].values)