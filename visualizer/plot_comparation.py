import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import csv
def get_data(file_name: str):
    with open(file_name) as file:
        r = csv.DictReader(file)
        costs = {x: [] for x in r.fieldnames}

        for row in r:
            for key in costs:
                costs[key].append(float(row[key]))

    return costs


def plot_compare(file_name):
    costs = get_data(file_name)
    plt.figure(figsize=(10, 10))

    for key in costs:
        x = [i for i in range(len(costs[key]))]
        plt.plot(x, costs[key], label=key)
    plt.legend()
    plt.xlabel("test_number")
    plt.ylabel("Min distance")
    plt.savefig("..\\data\\plots\\Fitness_selections.png")
