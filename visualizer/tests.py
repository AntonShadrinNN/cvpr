import run
from cvrp_utils.twcvrp import get_fitness
from cvrp_utils.mutations.swap_mutation import mutate
from cvrp_utils.crossovers.ordered import crossover
from cvrp_utils.read.TWVRP import load
from cvrp_utils.twcvrp import split_roads
from cvrp_utils.selections import *
from visualizer.plot_comparation import plot_compare
from visualizer.plot_convergence import plot_conv
from visualizer.plot_vehicle_routes import plot_routes
import os


def write_select_work(output_file: str) -> None:
    cost = {"tournament_selection": [], "stochastic_selection": [], "roulette_selection": []}
    selections = {"tournament_selection": tournament, "stochastic_selection": stochastic,
                  "roulette_selection": roulette}
    instances = [f"instances\\{f}" for f in os.listdir("instances")]

    for select in selections:
        for instance in instances:
            problem, best, costs = run.run(mutation_prob=0.09,
                                           crossover_prob=1,
                                           instance_path=instance,
                                           population_size=300,
                                           epochs=50,
                                           fitness_func=get_fitness,
                                           mutation_func=mutate,
                                           crossover_func=crossover,
                                           loader=load,
                                           splitter=split_roads,
                                           selection_func=selections[select]
                                           )

            cost[select] += [min(costs)]

    with open(f"..\\data\\test_results\\{output_file}", "w", encoding="utf-8") as file:
        file.write(f'{",".join(cost.keys())}\n')
        s = list(cost.values())
        for v in zip(*s):
            file.write(f'{",".join(map(str, v))}\n')


def write_algo_work(test: str, ) -> None:
    problem, best, costs = run.run(mutation_prob=0.09,
                                   crossover_prob=1,
                                   instance_path=test,
                                   population_size=300,
                                   epochs=40,
                                   fitness_func=get_fitness,
                                   mutation_func=mutate,
                                   crossover_func=crossover,
                                   loader=load,
                                   splitter=split_roads,
                                   selection_func=stochastic
                                   )

    with open(f"..\\data\\test_results\\sto{os.path.splitext(os.path.split(test)[-1])[0]}.txt", "w", encoding="utf-8")\
            as file:
        file.write(" ".join(map(str, costs)))

    with open(f"..\\data\\test_results\\rout_sto{os.path.splitext(os.path.split(test)[-1])[0]}.txt", "w", encoding="utf-8")\
            as file:
        file.write(f"{str(len(problem.weights))}\n")
        for row in problem.weights:
            file.write(f'{" ".join(map(str, row))}\n')

        file.write(f"{str(len(best))}\n")
        for c in best:
            file.write(f'{" ".join(map(str, c))}\n')


# write_select_work("selections_2.txt")
# plot_compare("..\\data\\test_results\\selections_2.txt")
# plot_compare("..\\data\\test_results\\selections.txt")

write_algo_work("instances\\R101.txt")
# plot_route("..\\data\\test_results\\rout_tournR101.txt")
plot_conv("..\\data\\test_results\\stoR101.txt")
# plot_conv("..\\data\\test_results\\C101.txt")