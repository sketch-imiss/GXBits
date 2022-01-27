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