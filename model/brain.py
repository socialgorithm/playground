from model.genome import Genome
import tensorflow as tf
import numpy as np


class InsectBrain:

    def __init__(self, genome: Genome):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.session = tf.Session()
            self.inputs = tf.placeholder(tf.float32, shape=(1,5), name='inputs')
            # constructing input layer
            input_layer_weights = np.transpose(np.array(genome.genes['W_inputs'].values).reshape(5,5))
            input_weights = tf.constant(value=input_layer_weights, dtype=tf.float32)
            input_layer_bias = np.array(genome.genes['B_inputs'].values).reshape(1, 5)
            input_bias = tf.constant(value=input_layer_bias, dtype=tf.float32)
            input_weightedSum = tf.matmul(self.inputs, input_weights) + input_bias
            input_layer_out = tf.nn.relu(input_weightedSum)
            # constructing first layer
            first_layer_weights = np.transpose(np.array(genome.genes['W_one'].values).reshape(5, 5))
            layerone_weights = tf.constant(value=first_layer_weights, dtype=tf.float32)
            first_layer_bias = np.array(genome.genes['B_one'].values).reshape(1, 5)
            layerone_bias = tf.constant(value=first_layer_bias, dtype=tf.float32)
            layerone_weightedSum = tf.matmul(input_layer_out,layerone_weights) + layerone_bias
            layerone_out = tf.nn.relu(layerone_weightedSum)
            # constructing second layer
            second_layer_weights = np.transpose(np.array(genome.genes['W_two'].values).reshape(5,5))
            layertwo_weights = tf.constant(value=second_layer_weights,dtype=tf.float32)
            second_layer_bias = np.array(genome.genes['B_two'].values).reshape(1,5)
            layertwo_bias = tf.constant(value=second_layer_bias,dtype=tf.float32)
            layertwo_weightedSum = tf.matmul(layerone_out, layertwo_weights) + layertwo_bias
            layertwo_out = tf.nn.relu(layertwo_weightedSum)
            # constructing output layer
            output_layer_weights = np.transpose(np.array(genome.genes['W_out'].values).reshape(1,5))
            layerout_weights = tf.constant(value=output_layer_weights,dtype=tf.float32)
            output_layer_bias = np.array(genome.genes['B_out'].values).reshape(1,1)
            layerout_bias = tf.constant(value=output_layer_bias,dtype=tf.float32)
            layerout_weightedSum = tf.matmul(layerone_out,layerout_weights) + layerout_bias
            self.layerout_out = layerout_weightedSum


    def evaluate(self,inputs):
        value = None
        with self.graph.as_default():
            feed_dict = {self.inputs: inputs}
            value = self.session.run(fetches=self.layerout_out, feed_dict=feed_dict)[0, 0]
            if value < -1:
                value = -1
            elif value > 1:
                value = 1
        return value


if __name__ == "__main__":
    genome = Genome()
    genome.new_gene(size=25, value_bounds=(-1, 1), name="W_inputs")
    genome.new_gene(size=5, value_bounds=(-1, 1), name="B_inputs")
    genome.new_gene(size=25, value_bounds=(-1, 1), name="W_one")
    genome.new_gene(size=5, value_bounds=(-1, 1), name="B_one")
    genome.new_gene(size=25, value_bounds=(-1, 1), name="W_two")
    genome.new_gene(size=5, value_bounds=(-1, 1), name="B_two")
    genome.new_gene(size=5, value_bounds=(-1, 1), name="W_out")
    genome.new_gene(size=1, value_bounds=(-1, 1), name="B_out")
    brain = InsectBrain(genome)
    brain.evaluate(inputs=np.array([0, 0, 1, 0, 0]).reshape(1, 5))


# arr = np.array([0,0,0,1,1,1,2,2,2]).reshape(3,3)
# arr = np.transpose(arr)
# inp = np.array([1,1,1]).reshape(1,3)
# print(inp)
# print("\n")
# print(arr)
# print("\n")
# print(np.matmul(inp,arr))
