import random


def mutate(individual: list, prob: float) -> list:
    """
    Inputs : Individual route
             Probability of mutation betwen (0,1)
    Outputs : Mutated individual according to the probability
    """
    size = len(individual)
    for i in range(size):
        if random.random() < prob:
            swap_indx = random.randint(0, size - 2)
            if swap_indx >= i:
                swap_indx += 1
            individual[i], individual[swap_indx] = \
                individual[swap_indx], individual[i]

    return individual
