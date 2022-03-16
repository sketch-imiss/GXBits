import mmh3
import math
import random
import os
import pickle

from utils import *


class GXBits:

    """
        :param dict_dataset: raw dataset represented as a map user->list of items
        :param size: the number of bits in each gxbits sketch
        :param probability: parameter of the geometric distribution
        :param block_truncated: whether gxbits sketch is block_truncated or not
        :param num_bits: the number of bits in each segment
        :param num_iterations: maximum number of iterations for newton-raphson method
        :param error: stopping condition of newton-raphson method
        :param output: output directory, the default is 'result/'
        :param seed: the round number of experiments, which is also used as the random seed in each round

        :func build_sketch(): initialize a gxbits sketch for each user and update the sketch based on all its items
        :func estimate_difference(): estimate the set difference cardinality
        :func newton_raphson(): iteratively optimize the estimated set difference cardinality
        :func compute_probability(): compute the mapping probability for each bit
        :func compute_function_derivative(): compute the raw function, first derivative, and second derivative with
                                             respect to the estimated set difference cardinality

        :output format: [actual set difference, estimated set difference]
    """

    def __init__(self, dict_dataset, size, probability, block_truncated, num_bits, error, rate, output, seed):
        self.dict_dataset = dict_dataset
        self.size = size
        self.probability = probability
        self.block_truncated = block_truncated
        self.num_bits = num_bits
        self.num_segments = math.ceil(size / num_bits)
        self.error = error
        self.rate = rate
        self.output = output
        self.seed = seed

    def build_sketch(self):
        self.dict_gxbits_sketch = dict()

        for user in self.dict_dataset:
            gxbits_sketch = [0] * self.size

            if not self.block_truncated:
                for item in self.dict_dataset[user]:
                    random_num = mmh3.hash(str(item), signed=False, seed=self.seed) / (2 ** 32 - 1)
                    index = math.floor(math.log(1 - random_num) / math.log(1 - self.probability))
                    if index >= self.size:
                        index = self.size - 1
                    gxbits_sketch[index] ^= 1

                self.dict_gxbits_sketch[user] = gxbits_sketch
            else:
                for item in self.dict_dataset[user]:
                    random_num = mmh3.hash(str(item), signed=False, seed=self.seed) / (2 ** 32 - 1)
                    segment_index = math.floor(math.log(1 - random_num) / math.log(1 - self.probability))
                    if segment_index >= self.num_segments:
                        segment_index = self.num_segments - 1

                    if segment_index == self.num_segments - 1:
                        index = random.randint(segment_index * self.num_bits, self.size-1)
                        gxbits_sketch[index] ^= 1
                    else:
                        index = random.randint(segment_index * self.num_bits, (segment_index + 1) * self.num_bits - 1)
                        gxbits_sketch[index] ^= 1

                self.dict_gxbits_sketch[user] = gxbits_sketch

    def estimate_difference(self):
        random.seed(self.seed)

        lst_user = list(self.dict_dataset.keys())
        num_user = len(lst_user)
        random.shuffle(lst_user)

        lst_result = list()
        for i in range(num_user - 1):
            user_A = lst_user[i]
            user_B = lst_user[i + 1]

            lst_A = self.dict_dataset[user_A]
            lst_B = self.dict_dataset[user_B]

            gxbits_sketch_A = self.dict_gxbits_sketch[user_A]
            gxbits_sketch_B = self.dict_gxbits_sketch[user_B]

            zero_ratio = 0
            one_bits = 0
            for j in range(self.size):
                zero_ratio += (1 - gxbits_sketch_A[j] ^ gxbits_sketch_B[j])
                one_bits += gxbits_sketch_A[j] ^ gxbits_sketch_B[j]
            zero_ratio /= self.size

            if one_bits >= self.size / 2:
                one_bits = self.size / 2 - 1

            initial_difference = math.log(1 - 2 * one_bits / self.size) / math.log(1 - 2 / self.size)
            estimated_difference = self.newton_raphson(initial_difference, zero_ratio)
            actual_difference = compute_difference(lst_A, lst_B)

            lst_result.append([actual_difference, estimated_difference])

        foutput = open(os.path.join(self.output, 'gxbits_' + str(self.seed) + '.out'), 'wb')
        pickle.dump(lst_result, foutput)
        foutput.close()

        return lst_result

    def newton_raphson(self, initial_difference, zero_ratio):
        estimated_difference = initial_difference
        raw_function, first_derivative = self.compute_function_derivative(estimated_difference, zero_ratio)

        while abs(first_derivative) > self.error:
            estimated_difference -= self.rate * raw_function / first_derivative
            raw_function, first_derivative = self.compute_function_derivative(estimated_difference, zero_ratio)

        return estimated_difference

    def compute_probability(self, index):
        if not self.block_truncated:
            if 0 <= index <= self.size - 2:
                return self.probability * (1 - self.probability) ** index
            elif index == self.size - 1:
                return (1 - self.probability) ** (self.size - 1)
        else:
            if 0 <= index < self.num_bits * (self.num_segments - 1):
                return self.probability * (1 - self.probability) ** math.floor(index / self.num_bits) / self.num_bits
            elif self.num_bits * (self.num_segments - 1) <= index <= self.size - 1:
                return (1 - self.probability) ** (self.num_segments - 1) / self.num_bits

    def compute_function_derivative(self, estimated_difference, zero_ratio):
        raw_function = 0
        first_derivative = 0
        second_derivative = 0

        for i in range(self.size):
            probability = self.compute_probability(i)
            raw_function += 1 + (1 - 2 * probability) ** estimated_difference
            first_derivative += math.log(1 - 2 * probability) * (1 - 2 * probability) ** estimated_difference
            # second_derivative += (math.log(1 - 2 * probability) ** 2) * (1 - 2 * probability) ** estimated_difference

        raw_function = raw_function / (2 * self.size) - zero_ratio
        first_derivative /= (2 * self.size)
        # second_derivative /= (2 * self.size)

        # return raw_function, first_derivative, second_derivative
        return raw_function, first_derivative

