import mmh3
import math
import random
import os
import pickle

from utils import *


class HyperLogLog:

    """
        :param dict_dataset: raw dataset represented as a map user->list of items
        :param size: the number of counters in each hyperloglog sketch
        :param output: output directory, the default is 'result/'
        :param seed: the round number of experiments, which is also used as the random seed in each round

        :func build_sketch(): initialize a hyperloglog sketch for each user and update the sketch based on all its items
        :func estimate_difference(): estimate the set difference cardinality
        :func compute_index_value(): compute the index and counter value for each item before inserting it into the sketch
        :func estimate_cardinality(): estimate the cardinality for each hyperloglog sketch

        :output format: [actual set difference, estimated set difference]
    """

    def __init__(self, dict_dataset, size, output, seed):
        self.dict_dataset = dict_dataset
        self.size = size
        self.output = output
        self.seed = seed

    def build_sketch(self):
        self.dict_hll_sketch = dict()

        for user in self.dict_dataset:
            hll_sketch = [0] * self.size
            flag = math.ceil(math.log2(self.size))

            for item in self.dict_dataset[user]:
                item_trans = mmh3.hash(str(item), signed=False, seed=self.seed)
                index, value = self.compute_index_value(item_trans, flag)
                if value > hll_sketch[index]:
                    hll_sketch[index] = value

            self.dict_hll_sketch[user] = hll_sketch

    def compute_index_value(self, item, flag):
        binary_item = '0' * (32 - len(bin(item)[2:])) + bin(item)[2:]
        index = int(binary_item[0:flag], 2) % self.size
        value = 0
        for bit in binary_item[flag:]:
            if bit == '0':
                value += 1
            else:
                break
        value += 1

        return index, value

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

            hll_sketch_A = self.dict_hll_sketch[user_A]
            hll_sketch_B = self.dict_hll_sketch[user_B]

            hll_sketch_merge = [0] * self.size
            for j in range(self.size):
                hll_sketch_merge[j] = max(hll_sketch_A[j], hll_sketch_B[j])

            cardinality_A = self.estimate_cardinality(hll_sketch_A)
            cardinality_B = self.estimate_cardinality(hll_sketch_B)
            cardinality_union = self.estimate_cardinality(hll_sketch_merge)

            estimated_difference = abs(2 * cardinality_union - cardinality_A - cardinality_B)
            actual_difference = compute_difference(lst_A, lst_B)
            lst_result.append([actual_difference, estimated_difference])

        foutput = open(os.path.join(self.output, 'hll_' + str(self.seed) + '.out'), 'wb')
        pickle.dump(lst_result, foutput)
        foutput.close()

        return lst_result

    def estimate_cardinality(self, hll_sketch):
        zero_bits = 0
        alpha = 0.7213 / (1 + 1.079 / self.size)
        tmp = 0

        for i in range(self.size):
            tmp += (2 ** (-hll_sketch[i]))
            if hll_sketch[i] == 0:
                zero_bits += 1
        cardinality = alpha * (self.size ** 2) / tmp

        if zero_bits == 0:
            zero_bits = 1

        if cardinality < 2.5 * self.size:
            cardinality = -self.size * math.log(zero_bits / self.size)

        return cardinality
