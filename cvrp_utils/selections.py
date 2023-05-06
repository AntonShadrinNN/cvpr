# TODO: implement our own roulette wheel selection

from deap.tools import selRoulette, selTournament, selStochasticUniversalSampling


def roulette(population, size):
    return selRoulette(population, size)


def stochastic(population, size):
    return selStochasticUniversalSampling(population, size)


def tournament(population, population_size):
    return selTournament(population, population_size, tournsize=100)
