import random

from deap import creator, base, tools
from mutations.shuffle_mutation import mutate
from crossover.random_crossover import crossover

MUTATION_PROB = 0.85


class Vrp:

    def __init__(self, num_customers: int, population_size: int, epochs: int):
        self.population = None
        self.tools = base.Toolbox()
        self.num_customers = num_customers
        self.population_size = population_size
        self.epochs = epochs
        
    def get_fitness(self, cost: float):
        pass

    def define_model(self):
        # Create fitness and individual classes
        creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
        creator.create("Individual", list, fitness=creator.fitness)

        # create list of customers numbered from 1 to number of customers given
        self.tools.register('customers', random.sample, range(1, self.num_customers + 1),  self.num_customers)

        # create an individual
        self.tools.register('individual', tools.initIterate, creator.Individual, self.tools.customers)
        # create population based on individual
        self.tools.register('population', tools.initRepeat, list, self.tools.individual)

        # get individual fitness for chromosome
        self.tools.register('get_fitness', self.get_fitness, cost=1.0)

        # select ancestor for evolution
        self.tools.register('select', tools.selNSGA2)

        # mutation func with constant probability
        self.tools.register('mutate', mutate, prob=MUTATION_PROB)

        # crossover func
        self.tools.register('crossover', crossover)

    def init_population(self):
        self.population = self.tools.population(n=self.population_size)
        self.not_weighted = [ind for ind in self.population if not ind.fitness.valid]
        self.fitnesses = list(map(self.tools.fitness, self.not_weighted))

        for chromosome, fit in zip(self.not_weighted, self.fitnesses):
            chromosome.fitness.values = fit

        self.population = self.tools.select(self.population, len(self.population))

    def compile(self):
        for epoch in range(self.epochs):
            # select next generation
            self.descendants = [tools. tools.selRoulette(self.population, len(self.population))]


