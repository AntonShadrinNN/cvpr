from typing import Callable, Any
import random

from deap import creator, base, tools
# from cvrp_utils.utils import print_routes, split_roads, calculate_distance_from_solution
# from cvrp_utils.twcvrp import split_roads
MUTATION_PROB = None
CROSSOVER_PROB = None
PROBLEM = None
CAPACITY = None
DEPOT = None


class Vrp:

    def __init__(self, num_customers: int, population_size: int, epochs: int,
                 fitness_func: Callable, mutation_func: Callable, crossover_func: Callable,
                 split_func: Callable):
        self._population = None
        self.__tools = base.Toolbox()
        self._num_customers = num_customers
        self._population_size = population_size
        self._epochs = epochs
        self._get_fitness = fitness_func
        self._mutation_func = mutation_func
        self._crossover_func = crossover_func
        self._splitter = split_func

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
        self.__tools.register('get_fitness', self._get_fitness,
                              cost=1.0, p=PROBLEM)

        # select ancestor for evolution
        self.__tools.register('select', tools.selNSGA2)

        # mutation func with constant probability
        self.__tools.register('mutate', self._mutation_func, prob=MUTATION_PROB)

        # crossover func
        self.__tools.register('crossover', self._crossover_func)

    def init_population(self):
        self._population = self.__tools.population(n=self._population_size)
        not_weighted = [ind for ind in self._population if not ind.fitness.valid]
        fitnesses = list(map(self.__tools.get_fitness, not_weighted))

        for chromosome, fit in zip(not_weighted, fitnesses):
            chromosome.fitness.values = fit

        self._population = self.__tools.select(self._population, len(self._population))
        print(f'Population successfully initialized with length {len(self._population)}!')

    def compile(self):
        for epoch in range(self._epochs):
            cur_best = tools.selBest(self._population, 1)[0]
            if epoch % 10 == 0:
                print(f'Evaluating generation {epoch}')
                print(f'Now the best individual is {cur_best}\n'
                      f'Cost: {self._calculate_distance(self._splitter(cur_best, PROBLEM))}')
            # select next generation
            descendants = [self.__tools.clone(ind) for ind in
                           tools.selTournamentDCD(self._population, len(self._population))]
            # loop for crossover and mutation operations
            for chr1, chr2 in zip(descendants[::2], descendants[1::2]):
                if random.random() < CROSSOVER_PROB:
                    self.__tools.crossover(chr1, chr2)

                    del chr1.fitness.values, chr2.fitness.values

                self.__tools.mutate(chr1)
                self.__tools.mutate(chr2)

            not_weighted = [ind for ind in descendants if not ind.fitness.valid]
            fitnesses = self.__tools.map(self.__tools.get_fitness, not_weighted)
            for chromosome, fit in zip(not_weighted, fitnesses):
                chromosome.fitness.values = fit

            self._population = self.__tools.select(self._population + descendants, self._population_size)

    @staticmethod
    def _calculate_distance(solution: list[list]) -> float:
        total = 0
        for line in solution:
            last = line[0]
            temp = PROBLEM.get_weight(PROBLEM.depots[0], last)
            for c in range(1, len(line)):
                s_distance = PROBLEM.get_weight(last, int(line[c]))
                temp += s_distance
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

    def find_best(self):
        best = tools.selBest(self._population, 1)[0]
        print(f'Unique individuals: {len(set(best))}')
        print(f"Best individual is {best}")
        print(f"Number of vechicles required are "
              f"{best.fitness.values[0]}")
        self._print_routes(best)


def run(mutation_prob: float, crossover_prob: float, instance_path: str, population_size: int, epochs: int,
        fitness_func: Callable[[list, float, Any, int, int], tuple[int, float]],
        mutation_func: Callable[[list, float], list],
        crossover_func: Callable[[list, list], tuple[list, list]], loader: Callable[[str], Any],
        splitter: Callable):
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
    )
    p.define_model()
    p.init_population()
    p.compile()
    p.find_best()

