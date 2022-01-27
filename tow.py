import mmh3
import random
import os
import pickle

from utils import *


class TOW:

    """
        :param dict_dataset: raw dataset represented as a map user->list of items
        :param size: the number of counters in each tug-of-war sketch
        :param output: output directory, the default is 'result/'
        :param seed: the round number of experiments, which is also used as the random seed in each round

        :func build_sketch(): initialize a tug-of-war sketch for each user and update the sketch based on all its items
        :func estimate_difference(): estimate the set difference cardinality

        :output format: [actual set difference, estimated set difference]
    """

    def __init__(self, dict_dataset, size, output, seed):
        self.dict_dataset = dict_dataset
        self.size = size
        self.output = output
        self.seed = seed

    def build_sketch(self):
        self.dict_tow_sketch = dict()

        for user in self.dict_dataset:
            tow_sketch = [0] * self.size

            for item in self.dict_dataset[user]:
                for i in range(self.size):
                    random_num = mmh3.hash(str(item), signed=False, seed=i+self.seed) / (2 ** 32 - 1)
                    if random_num <= 0.5:
                        tow_sketch[i] += 1
                    else:
                        tow_sketch[i] -= 1

            self.dict_tow_sketch[user] = tow_sketch

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

            tow_sketch_A = self.dict_tow_sketch[user_A]
            tow_sketch_B = self.dict_tow_sketch[user_B]

            estimated_difference = 0
            for j in range(self.size):
                estimated_difference += (tow_sketch_A[j] - tow_sketch_B[j]) ** 2
            estimated_difference /= self.size
            actual_difference = compute_difference(lst_A, lst_B)

            lst_result.append([actual_difference, estimated_difference])

            print(actual_difference, estimated_difference)

        foutput = open(os.path.join(self.output, 'tow_' + str(self.seed) + '.out'), 'wb')
        pickle.dump(lst_result, foutput)
        foutput.close()