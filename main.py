import copy
import random

from classes.customer import *
import math


CUSTOMERS = []
DEPOT = City(-1, -1)
VEHICLE = 0
POPULATION_FITNESS = 0
CAPACITY = 0
POPULATION_SIZE = 20
POPULATION = []


def read_data(path: str):
    global DEPOT, VEHICLE, CAPACITY
    with open(path, 'r', encoding='utf-8') as file:
        data = file.readlines()

    VEHICLE, CAPACITY = map(int, data[0].split())
    DEPOT = City(*map(int, data[1].split()))

    for i in range(2, len(data)):
        c = data[i].split()
        x_coord = float(c[0])
        y_coord = float(c[1])
        demand = int(c[2])
        if demand > CAPACITY:
            raise ValueError("Demand is greater than capacity")
        CUSTOMERS.append(Customer(i-2, x_coord, y_coord, demand))


def calculate_distance(c1: City, c2: City) -> float:
    return ((c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2) ** 0.5


def get_fitness(chromosome: list[Customer]):
    fitness = 0
    for i in range(len(chromosome) - 1):
        fitness += calculate_distance(chromosome[i].city, chromosome[i + 1].city)

    cur_demand = 0
    for c in chromosome:
        if c.city == DEPOT and cur_demand > CAPACITY:
            fitness = math.inf
            return fitness
        elif c.city == DEPOT:
            cur_demand = 0
        else:
            cur_demand += c.demand

    return fitness


# def get_population_fitness(population: list[list[Customer]]) -> list[tuple]:
#     calculated_fitness = []
#     for individual in population:
#         calculated_fitness.append((individual, get_fitness(individual)))
#
#     return calculated_fitness


def create_chromosome():
    c = copy.deepcopy(CUSTOMERS)
    random.shuffle(c)
    return c


def initialize():
    global POPULATION_FITNESS
    retries = len(CUSTOMERS) * POPULATION_SIZE
    for i in range(retries):
        chromosome = create_chromosome()
        fitness = get_fitness(chromosome)
        if fitness != math.inf:
            cell = (chromosome, fitness)
            POPULATION.append(cell)
            POPULATION_FITNESS += fitness

    if len(POPULATION) == 0:
        raise TimeoutError("impossible to create population")

