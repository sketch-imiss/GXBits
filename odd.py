import mmh3
import random
import math
import pickle
import os

from utils import *


class Odd:

    """
        :param dict_dataset: raw dataset represented as a map user->list of items
        :param size: the number of bits in each odd sketch
        :param output: output directory, the default is 'result/'
        :param seed: the round number of experiments, which is also used as the random seed in each round

        :func build_sketch(): initialize an odd sketch for each user and update the sketch based on all its items
        :func estimate_difference(): estimate the set difference cardinality

        :output format: [actual set difference, estimated set difference]
    """

    def __init__(self, dict_dataset, size, output, seed):
        self.dict_dataset = dict_dataset
        self.size = size
        self.output = output
        self.seed = seed

    def build_sketch(self):
        self.dict_odd_sketch = dict()

        for user in self.dict_dataset:
            odd_sketch = [0] * self.size

            for item in self.dict_dataset[user]:
                index = mmh3.hash(str(item), signed=False, seed=self.seed) % self.size
                odd_sketch[index] ^= 1

            self.dict_odd_sketch[user] = odd_sketch

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

            odd_sketch_A = self.dict_odd_sketch[user_A]
            odd_sketch_B = self.dict_odd_sketch[user_B]

            one_bits = 0
            for j in range(self.size):
                one_bits += (odd_sketch_A[j] ^ odd_sketch_B[j])

            estimated_difference = math.log(1 - 2 * one_bits / self.size) / math.log(1 - 2 / self.size)
            actual_difference = compute_difference(lst_A, lst_B)
            lst_result.append([actual_difference, estimated_difference])

            print(actual_difference, estimated_difference)

        foutput = open(os.path.join(self.output, 'odd_' + str(self.seed) + '.out'), 'wb')
        pickle.dump(lst_result, foutput)
        foutput.close()
