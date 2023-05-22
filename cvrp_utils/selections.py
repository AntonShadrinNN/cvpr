import copy
import random
from operator import attrgetter


def roulette(population: list, size: int, fit_attr="fitness") -> list:
    pop_copy = copy.deepcopy(population)
    max_fit = getattr(max(pop_copy, key=lambda x: x.fitness.values[1]), fit_attr).values[1] * 1.1
    for p in pop_copy:
        p.fitness.values = (p.fitness.values[0],  max_fit - p.fitness.values[1])
    # pop_copy = map(lambda x: setattr(x, fit_attr, max_fit - getattr(x, fit_attr)), pop_copy)
    sorted_population = sorted(pop_copy, key=attrgetter(fit_attr), reverse=True)
    sum_fit = sum(getattr(ind, fit_attr).values[1] for ind in population)
    chosen_ind = []

    for i in range(size):
        rand_fit = random.random() * sum_fit
        temp_fit_sum = 0

        for ind in sorted_population:
            temp_fit_sum += getattr(ind, fit_attr).values[1]

            if temp_fit_sum > rand_fit:
                ind.fitness.values = (ind.fitness.values[0], max_fit - ind.fitness.values[1])
                chosen_ind.append(ind)
                break

    return chosen_ind


def stochastic(population: list, size: int, fit_attr="fitness") -> list:
    pop_copy = copy.deepcopy(population)
    max_fit = getattr(max(pop_copy, key=lambda x: x.fitness.values[1]), fit_attr).values[1] * 1.1
    for p in pop_copy:
        p.fitness.values = (p.fitness.values[0], max_fit - p.fitness.values[1])
    sorted_population = sorted(pop_copy, key=attrgetter(fit_attr), reverse=True)
    sum_fit = sum(getattr(ind, fit_attr).values[1] for ind in pop_copy)

    distance = sum_fit / float(size)
    begin = random.uniform(0, distance)
    points = [begin + i * distance for i in range(size)]
    chosen_ind = []

    for p in points:
        i = 0
        temp_fit_sum = getattr(sorted_population[i], fit_attr).values[1]

        while temp_fit_sum < p:
            i += 1
            temp_fit_sum += getattr(sorted_population[i], fit_attr).values[1]
        ind = copy.deepcopy(sorted_population[i])
        ind.fitness.values = (ind.fitness.values[0], max_fit - ind.fitness.values[1])
        chosen_ind.append(ind)

    return chosen_ind


def tournament(population: list, size: int, tourn_size=100, fit_attr="fitness") -> list:
    chosen_ind = []

    for i in range(size):
        potential_ind = [random.choice(population) for _ in range(tourn_size)]
        chosen_ind.append(max(potential_ind, key=attrgetter(fit_attr)))

    return chosen_ind
