def compute_difference(lst_A, lst_B):
    """
    :param lst_A: raw set A
    :param lst_B: raw set B

    :output the set difference cardinality between set A and set B
    """

    cardinality_union = len(list(set(lst_A).union(set(lst_B))))
    cardinality_intersection = len(list(set(lst_A).intersection(set(lst_B))))
    cardinality_difference = cardinality_union - cardinality_intersection

    return cardinality_difference


def compute_rse(lst):
    rse = 0
    true_cardinality = lst[0][0]
    num_exp = len(lst)

    for exp in lst:
        rse += (exp[1] - true_cardinality) ** 2

    rse = (rse / num_exp) ** 0.5
    rse /= true_cardinality

    return rse


def compute_aare(lst):
    aare = 0
    num_exp = 0

    for exp in lst:
        if exp[0] > 0:
            aare += abs(exp[0] - exp[1]) / exp[0]
            num_exp += 1

    aare /= num_exp

    return aare
