import os
import matplotlib.pyplot as plt
import csv


def get_data(file_name: str):
    with open(file_name) as file:
        r = csv.DictReader(file)
        costs = {x: [] for x in r.fieldnames}

        for row in r:
            for key in costs:
                costs[key].append(float(row[key]))

    return costs


def plot_compare(file_name: str):
    costs = get_data(file_name)
    plt.figure(figsize=(10, 10))

    for key in costs:
        x = [i for i in range(len(costs[key]))]
        plt.plot(x, costs[key], label=key)
    plt.legend()
    plt.xlabel(" Test number")
    plt.ylabel("Min cost")
    plt.savefig(f"..\\data\\plots\\Fitness_selections_{os.path.splitext(os.path.split(file_name)[-1])[0]}.png")
