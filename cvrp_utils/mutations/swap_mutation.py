import random


def mutate(individual: list, prob: float) -> list:
    size = len(individual)

    for i in range(size):
        if random.random() < prob:
            swap_index = random.randint(0, size - 2)

            if swap_index >= i:
                swap_index += 1
            individual[i], individual[swap_index] = \
                individual[swap_index], individual[i]

    return individual
