import run

# TWCVRP
from cvrp_utils.twcvrp import get_fitness
from cvrp_utils.mutations.shuffle_mutation import mutate
from cvrp_utils.crossovers.ordered import crossover
from cvrp_utils.read.TWVRP.read import load

# CVRP
# from utils.cvrp import get_fitness
# from mutations.shuffle_mutation import mutate
# from crossover.orderedCrossOver import crossover
# from tsplib95 import load

if __name__ == "__main__":
    run.run(mutation_prob=0.02,
            crossover_prob=0.85,
            instance_path="instances/C101.txt",
            population_size=400,
            epochs=10,
            fitness_func=get_fitness,
            mutation_func=mutate,
            crossover_func=crossover,
            parser=load
            )
# run.run(mutation_prob=0.04,
#             crossover_prob=0.9,
#             instance_path="instances/DIMACS/A-n32-k5.vrp.txt",
#             population_size=200,
#             epochs=15,
#             fitness_func=get_fitness,
#             mutation_func=mutate,
#             crossover_func=crossover,
#             parser=load
#             )
