import run
from cvrp_utils.twcvrp import get_fitness
from cvrp_utils.mutations.shuffle_mutation import mutate
from cvrp_utils.crossovers.ordered import crossover
from cvrp_utils.read.TWVRP import load
from cvrp_utils.twcvrp import split_roads
from cvrp_utils.selections import *
from visualizer.plot_comparation import plot_compare
from visualizer.plot_convergence import plot_conv
import os


def write_select_work(file_name):
    cost = {"tournament_selection": [], "stochastic_selection": [], "roulette_selection": []}
    selections = {"tournament_selection": tournament, "stochastic_selection": stochastic, "roulette_selection": roulette}
    instances = [f"instances\\{f}" for f in os.listdir("instances")]

    for select in selections:
        for instance in instances:
            problem, best, costs = run.run(mutation_prob=0.09,
                                           crossover_prob=1,
                                           instance_path=instance,
                                           population_size=300,
                                           epochs=2,
                                           fitness_func=get_fitness,
                                           mutation_func=mutate,
                                           crossover_func=crossover,
                                           loader=load,
                                           splitter=split_roads,
                                           selection_func=selections[select]
                                           )

            cost[select] += [min(costs)]

    with open(f"..\\data\\test_results\\{file_name}", "w", encoding="utf-8") as file:
        file.write(f'{",".join(cost.keys())}\n')
        s = list(cost.values())
        for v in zip(*s):
            file.write(f'{",".join(map(str, v))}\n')

    # temp: dict[str, list] = {key: [0] * 100 for key in selections}
    # iterations = 10
    # for i in range(iterations):
    #     for select in selections:
    #         problem, best, costs = run.run(mutation_prob=0.09,
    #                                        crossover_prob=1,
    #                                        instance_path="instances/R112.txt",
    #                                        population_size=300,
    #                                        epochs=50,
    #                                        fitness_func=get_fitness,
    #                                        mutation_func=mutate,
    #                                        crossover_func=crossover,
    #                                        loader=load,
    #                                        splitter=split_roads,
    #                                        selection_func=selections[select]
    #                                        )
    #         problems.append(problem)
    #         bests.append(best)
    #         temp[select] = [temp[select][x] + costs[x] for x in range(len(costs))]
    #         # print(temp)
    #
    # costs_per_select = {key: list(map(lambda x: x / iterations, temp[key])) for key in temp}
    # print(costs_per_select)
    # plot_compare("instancesR112_comp", costs_per_select, len(costs))
    # for s in selections:
    #     plot_conv(f"instancesR112_conv_{s}", costs_per_select[s])


def write_algo_work(test):
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
                                   selection_func=tournament
                                   )

    with open(f"..\\data\\test_results\\{os.path.splitext(os.path.split(test)[-1])[0]}.txt", "w") as file:
        file.write(" ".join(map(str, costs)))

    with open(f"..\\data\\test_results\\rout_{os.path.splitext(os.path.split(test)[-1])[0]}.txt", "w") as file:
        file.write(f"{str(len(problem.weights))}\n")
        for row in problem.weights:
            file.write(f'{" ".join(map(str, row))}\n')

        file.write(f"{str(len(best))}\n")
        for c in best:
            file.write(f'{" ".join(map(str, c))}\n')

        file.write(f"{' '.join(map(str, problem.weights[problem.depots[0]]))}")

# write_select_work("selections.txt")
# plot_compare("..\\data\\test_results\\selections.txt")
# write_algo_work("instances\\C101.txt")
# plot_conv("..\\data\\test_results\\C101.txt")