from typing import Callable, Any
import random

from deap import creator, base, tools
from cvrp_utils.utils import print_routes

MUTATION_PROB = None
CROSSOVER_PROB = None
PROBLEM = None
CAPACITY = None
DEPOT = None


class Vrp:

    def __init__(self, num_customers: int, population_size: int, epochs: int,
                 fitness_func: Callable, mutation_func: Callable, crossover_func: Callable):
        self.population = None
        self.tools = base.Toolbox()
        self.num_customers = num_customers
        self.population_size = population_size
        self.epochs = epochs
        self.get_fitness = fitness_func
        self.mutation_func = mutation_func
        self.crossover_func = crossover_func

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
        self.tools.register('get_fitness', self.get_fitness,
                            cost=1.0, p=PROBLEM)

        # select ancestor for evolution
        self.tools.register('select', tools.selNSGA2)

        # mutation func with constant probability
        self.tools.register('mutate', self.mutation_func, prob=MUTATION_PROB)

        # crossover func
        self.tools.register('crossover', self.crossover_func)

    def init_population(self):
        self.population = self.tools.population(n=self.population_size)
        not_weighted = [ind for ind in self.population if not ind.fitness.valid]
        fitnesses = list(map(self.tools.get_fitness, not_weighted))

        for chromosome, fit in zip(not_weighted, fitnesses):
            chromosome.fitness.values = fit

        self.population = self.tools.select(self.population, len(self.population))
        print(f'Population successfully initialized with length {len(self.population)}!')

    def compile(self):
        for epoch in range(self.epochs):
            if epoch % 10 == 0:
                print(f'Evaluating generation {epoch}')
            # select next generation
            descendants = [self.tools.clone(ind) for ind in
                                tools.selTournamentDCD(self.population, len(self.population))]
            # loop for crossover and mutation operations
            for chr1, chr2 in zip(descendants[::2], descendants[1::2]):
                if random.random() < CROSSOVER_PROB:
                    self.tools.crossover(chr1, chr2)

                    del chr1.fitness.values, chr2.fitness.values

                self.tools.mutate(chr1)
                self.tools.mutate(chr2)

            not_weighted = [ind for ind in descendants if not ind.fitness.valid]
            fitnesses = self.tools.map(self.tools.get_fitness, not_weighted)
            for chromosome, fit in zip(not_weighted, fitnesses):
                chromosome.fitness.values = fit

            self.population = self.tools.select(self.population + descendants, self.population_size)

    def find_best(self):
        self.best = tools.selBest(self.population, 1)[0]
        print(f'Unique individuals: {len(set(self.best))}')
        print(f"Best individual is {self.best}")
        print(f"Number of vechicles required are "
              f"{self.best.fitness.values[0]}")
        # print(f"Cost required for the transportation is "
        #       f"{self.best.fitness.values[1]}")
        print_routes(self.best, PROBLEM)


def run(mutation_prob: float, crossover_prob: float, instance_path: str, population_size: int, epochs: int,
        fitness_func: Callable[[list, float, Any, int, int], tuple[int, float]],
        mutation_func: Callable[[list, float], list],
        crossover_func: Callable[[list, list], tuple[list, list]], parser: Callable[[str], Any]):
    global PROBLEM, MUTATION_PROB, CROSSOVER_PROB, CAPACITY, DEPOT
    PROBLEM = parser(instance_path)
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
        crossover_func=crossover_func
    )
    p.define_model()
    p.init_population()
    p.compile()
    p.find_best()

