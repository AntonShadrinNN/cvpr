import run

# TWCVRP
from cvrp_utils.twcvrp import get_fitness
from cvrp_utils.mutations.shuffle_mutation import mutate
from cvrp_utils.crossovers.ordered import crossover
from cvrp_utils.read.TWVRP import load
from cvrp_utils.twcvrp import split_roads
from cvrp_utils.selections import tournament_selection
from visualizer.plot_vehicle_routes import plot_route
from visualizer.plot_convergence import plot_conv


if __name__ == "__main__":
    problem, best, costs = run.run(mutation_prob=0.09,
                                   crossover_prob=1,
                                   instance_path="instances/R112.txt",
                                   population_size=300,
                                   epochs=10,
                                   fitness_func=get_fitness,
                                   mutation_func=mutate,
                                   crossover_func=crossover,
                                   loader=load,
                                   splitter=split_roads,
                                   selection_func=tournament_selection
                                   )

    plot_conv("R112", costs)
    plot_route("R112", best, problem.weights, problem.weights[problem.depots[0]])