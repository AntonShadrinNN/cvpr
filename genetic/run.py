from typing import Callable
import random

from deap import creator, base, tools
from mutations.shuffle_mutation import mutate
from crossover.orderedCrossOver import crossover
# from tsplib95 import load as tsp_load
from read.TWVRP.read import parse as tsp_load

MUTATION_PROB = 0.04
CROSSOVER_PROB = 0.7
PROBLEM = tsp_load(r"../instances/C101.txt")
CAPACITY = PROBLEM.capacity
DEPOT = PROBLEM.depots[0]


def get_fitness(chr: list, cost: float):
    return trucks_required(chr), get_cost(chr, cost)


def get_cost(chr: list, cost: float) -> float:
    total_cost = 0
    routes = split_roads(chr)

    for s_route in routes:
        distance = 0
        last_customer = DEPOT

        for c in s_route:
            d = PROBLEM.get_weight(last_customer, c)

            distance += d
            last_customer = c

        # distance += PROBLEM.get_weight(last_customer, DEPOT)
        distance -= PROBLEM.get_weight(1, s_route[0])
        total_cost += cost * distance

    return total_cost


def split_roads(chr):
    route: list[list] = []
    sub_route = []
    load = 0
    # last_customer = 0

    for c in chr:
        demand = PROBLEM.demands[c]

        new_load = load + demand

        if new_load <= CAPACITY:
            sub_route.append(c)
            load = new_load
        else:
            route.append(sub_route)
            sub_route = [c]
            load = demand

        # last_customer = c

    if sub_route:
        route.append(sub_route)

    return route


def trucks_required(chr):
    return len(split_roads(chr))


def printRoute(route, merge=False):
    route_str = '0'
    sub_route_count = 0
    for sub_route in route:
        sub_route_count += 1
        sub_route_str = '0'
        for customer_id in sub_route:
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
        sub_route_str = f'{sub_route_str} - 0'
        if not merge:
            print(f'  Vehicle {sub_route_count}\'s route: {sub_route_str}')
        route_str = f'{route_str} - 0'
    if merge:
        print(route_str)


class Vrp:

    def __init__(self, num_customers: int, population_size: int, epochs: int):
        self.population = None
        self.tools = base.Toolbox()
        self.num_customers = num_customers
        self.population_size = population_size
        self.epochs = epochs

    def define_model(self):
        # Create fitness and individual classes
        creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
        creator.create("Individual", list, fitness=creator.Fitness)

        # create list of customers numbered from 1 to number of customers given
        self.tools.register('customers', random.sample, range(1, self.num_customers + 1), self.num_customers)

        # create an individual
        self.tools.register('individual', tools.initIterate, creator.Individual, self.tools.customers)
        # create population based on individual
        self.tools.register('population', tools.initRepeat, list, self.tools.individual)

        # get individual fitness for chromosome
        self.tools.register('get_fitness', get_fitness, cost=1.0)

        # select ancestor for evolution
        self.tools.register('select', tools.selNSGA2)

        # mutation func with constant probability
        self.tools.register('mutate', mutate, prob=MUTATION_PROB)

        # crossover func
        self.tools.register('crossover', crossover)

    def init_population(self):
        self.population = self.tools.population(n=self.population_size)
        self.not_weighted = [ind for ind in self.population if not ind.fitness.valid]
        self.fitnesses = list(map(self.tools.get_fitness, self.not_weighted))

        for chromosome, fit in zip(self.not_weighted, self.fitnesses):
            chromosome.fitness.values = fit

        self.population = self.tools.select(self.population, len(self.population))

    def compile(self):
        for epoch in range(self.epochs):
            # select next generation
            self.descendants = [self.tools.clone(ind) for ind in
                                tools.selTournamentDCD(self.population, len(self.population))]
            # loop for crossover and mutation operations
            for chr1, chr2 in zip(self.descendants[::2], self.descendants[1::2]):
                if random.random() < CROSSOVER_PROB:
                    self.tools.crossover(chr1, chr2)

                    del chr1.fitness.values, chr2.fitness.values

                self.tools.mutate(chr1)
                self.tools.mutate(chr2)

            self.not_weighted = [ind for ind in self.descendants if not ind.fitness.valid]
            self.fitnesses = self.tools.map(self.tools.get_fitness, self.not_weighted)
            for chromosome, fit in zip(self.not_weighted, self.fitnesses):
                chromosome.fitness.values = fit

            self.population = self.tools.select(self.population + self.descendants, self.population_size)

    def find_best(self):
        self.best = tools.selBest(self.population, 1)[0]
        print(f'Unique individuals: {len(set(self.best))}')
        print(f"Best individual is {self.best}")
        print(f"Number of vechicles required are "
              f"{self.best.fitness.values[0]}")
        print(f"Cost required for the transportation is "
              f"{self.best.fitness.values[1]}")
        printRoute(split_roads(self.best))


def run(mutation_prob: float, crossover_prob: float, instance_path: str, fitness_func: Callable[[str, float], float],
        mutation_func: Callable[[list, float], list], crossover_func: Callable[[list, list], tuple[list, list]]):
    pass

