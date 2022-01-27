import logging
import random


class Dataloader:
    '''
        :param dataset: dataset path or synthetic dataset
        :param intersection: set intersection cardinality
        :param difference: set difference cardinality
        :param seed: random seed used to generate items in each set

        :func generate_synthetic_dataset(): generate synthetic dataset
        :func load_public_dataset(): load public-available dataset

        :output: dict_dataset: dataset represented as a map user->list of items
    '''
    def __init__(self, dataset, intersection, difference, seed):
        self.dataset = dataset
        self.intersection = intersection
        self.difference = difference
        self.seed = seed

    def generate_synthetic_dataset(self):
        dict_dataset = dict()
        lst_union = list()
        lst_A = list()
        lst_B = list()
        random.seed(self.seed)

        while len(lst_union) < self.intersection + self.difference:
            random_num = random.randint(0, 2 ** 32 - 1)
            if random_num not in lst_union:
                lst_union.append(random_num)

        lst_A.extend(lst_union[0:self.intersection])
        lst_A.extend(lst_union[self.intersection:self.intersection + int(self.difference/2)])
        lst_B.extend(lst_union[0:self.intersection])
        lst_B.extend(lst_union[self.intersection + int(self.difference/2):])

        dict_dataset['A'] = lst_A
        dict_dataset['B'] = lst_B

        return dict_dataset

    def load_public_dataset(self):
        dict_dataset = dict()

        with open(self.dataset) as freader:
            for line in freader:
                [user, item] = list(map(int, line.strip().split()))
                if user not in dict_dataset:
                    dict_dataset[user] = []
                if item not in dict_dataset[user]:
                    dict_dataset[user].append(item)

        return dict_dataset

    def load_dataset(self):
        if self.dataset == 'synthetic':
            dict_dataset = self.generate_synthetic_dataset()
        else:
            dict_dataset = self.load_public_dataset()

        return dict_dataset