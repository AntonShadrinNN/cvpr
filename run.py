import copy
import math
from typing import Callable, Any
import random
from deap import creator, base, tools

MUTATION_PROB = None
CROSSOVER_PROB = None
PROBLEM = None
CAPACITY = None
DEPOT = None


class Vrp:

    def __init__(self, num_customers: int, population_size: int, epochs: int,
                 fitness_func: Callable, mutation_func: Callable, crossover_func: Callable,
                 split_func: Callable, selection_func: Callable):
        self._population = None
        self.__tools = base.Toolbox()
        self._num_customers = num_customers
        self._population_size = population_size
        self._epochs = epochs
        self._get_fitness = fitness_func
        self._mutation_func = mutation_func
        self._crossover_func = crossover_func
        self._splitter = split_func
        self._selection_func = selection_func

    def define_model(self):
        # Create fitness and individual classes
        creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
        creator.create("Individual", list, fitness=creator.Fitness)
        # create list of customers numbered from 1 to number of customers given
        self.__tools.register('customers', random.sample, range(1, self._num_customers + 1), self._num_customers)

        # create an individual
        self.__tools.register('individual', tools.initIterate, creator.Individual, self.__tools.customers)
        # create population based on individual
        self.__tools.register('population', tools.initRepeat, list, self.__tools.individual)

        # get individual fitness for chromosome
        self.__tools.register('get_fitness', self._get_fitness, p=PROBLEM)

        # selection func
        self.__tools.register('select', self._selection_func)

        # mutation func with constant probability
        self.__tools.register('mutate', self._mutation_func, prob=MUTATION_PROB)

        # crossover func
        self.__tools.register('crossover', self._crossover_func)

    def init_population(self):
        self._population = self.__tools.population(n=self._population_size)
        not_weighted = [ind for ind in self._population if not ind.fitness.valid]
        fitnesses = list(map(self.__tools.get_fitness, not_weighted))

        # weight the population using fitness function
        for chromosome, fit in zip(not_weighted, fitnesses):
            chromosome.fitness.values = fit

    def compile(self):
        f = open('res.txt', 'a', encoding='utf-8')
        best_cost = math.inf
        best_route = None
        cur_best = []
        costs = []
        for epoch in range(self._epochs):
            # select the best individual's fitness
            ind = tools.selBest(self._population, 1)[0]
            # calculate distance cost
            cost = self._calculate_distance(self._splitter(ind, PROBLEM))
            cur_best.append((ind, cost))
            if cost < best_cost:
                best_cost, best_route = cost, ind

            # calculate min cost on every 10 generation
            min_cost = min(cur_best, key=lambda x: x[1])[1]
            costs.append(min_cost)
            f.write(f'gen: {epoch}\tcost: {min_cost}\n')
            if epoch % 10 == 0:
                print(f'Evaluating generation {epoch}')
                print(f'Now the best individual is {cur_best[0]}\n'
                      f'Cost: {min_cost}\n')
                cur_best = []

            # select and clone offspring using selection func given
            descendants = list(map(self.__tools.clone, self.__tools.select(self._population, self._population_size)))
            off = []
            # loop for crossover and mutation operations
            for chr1, chr2 in zip(descendants[::2], descendants[1::2]):
                if random.random() < CROSSOVER_PROB:
                    chr1, chr2 = self.__tools.crossover(chr1, chr2)
                    del chr1.fitness.values, chr2.fitness.values
                chr1 = self.__tools.mutate(chr1)
                chr2 = self.__tools.mutate(chr2)
                # update offspring
                off.append(chr1)
                off.append(chr2)

            not_weighted = [ind for ind in off if not ind.fitness.valid]
            fitnesses = self.__tools.map(self.__tools.get_fitness, not_weighted)
            # weight new offspring
            for chromosome, fit in zip(not_weighted, fitnesses):
                chromosome.fitness.values = fit

            # select best routes from old and new population
            self._population = self.__tools.select(self._population + off, self._population_size)

        f.close()
        self._print_routes(best_route)
        return best_route, costs

    @staticmethod
    def _calculate_distance(solution: list[list]) -> float:
        total = 0
        for line in solution:
            last = line[0]
            total += PROBLEM.get_weight(PROBLEM.depots[0], last) + PROBLEM.get_weight(line[-1], PROBLEM.depots[0])
            for c in range(1, len(line)):
                s_distance = PROBLEM.get_weight(last, int(line[c]))
                total += s_distance
                last = c

        return total

    def _print_routes(self, ind: list[list]):
        route = self._splitter(ind, PROBLEM)
        route_str = '0'
        sub_route_count = 0
        for sub_route in route:
            sub_route_count += 1
            sub_route_str = '0'
            for customer_id in sub_route:
                sub_route_str = f'{sub_route_str} - {customer_id}'
                route_str = f'{route_str} - {customer_id}'
            sub_route_str = f'{sub_route_str} - 0'
            print(f'  Vehicle {sub_route_count}\'s route: {sub_route_str}')
            route_str = f'{route_str} - 0'
        print(f'  Cost for the transportation is {self._calculate_distance(route)}')


def run(mutation_prob: float, crossover_prob: float, instance_path: str, population_size: int, epochs: int,
        fitness_func: Callable[[list, Any, int, int], tuple[int, float]],
        mutation_func: Callable[[list, float], list],
        crossover_func: Callable[[list, list], tuple[list, list]], selection_func: Callable,
        loader: Callable[[str], Any], splitter: Callable):
    global PROBLEM, MUTATION_PROB, CROSSOVER_PROB, CAPACITY, DEPOT
    PROBLEM = loader(instance_path)
    MUTATION_PROB = mutation_prob
    CROSSOVER_PROB = crossover_prob
    CAPACITY = PROBLEM.capacity
    DEPOT = PROBLEM.depots[0]
    p = Vrp(
        num_customers=PROBLEM.dimension,
        population_size=population_size,
        epochs=epochs,
        fitness_func=fitness_func,
        mutation_func=mutation_func,
        crossover_func=crossover_func,
        split_func=splitter,
        selection_func=selection_func,
    )
    p.define_model()
    p.init_population()
    best, costs = p.compile()
    return PROBLEM, splitter(best, PROBLEM), costs