import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import os


def get_data(file_name: str):
    with open(file_name) as file:
        costs = list(map(float, file.readline().split()))

    return costs


def plot_conv(file_name: str):
    costs = get_data(file_name)
    plt.figure(figsize=(10, 10))
    iterations = list(range(1, len(costs) + 1))
    x_y_spline = make_interp_spline(iterations, costs)
    x_ = np.linspace(min(iterations), max(iterations), 500)
    y_ = x_y_spline(x_)

    plt.plot(x_, y_)
    plt.xlabel("Generations")
    plt.ylabel("Min distance")
    plt.savefig(f"..\\data\\plots\\{os.path.splitext(os.path.split(file_name)[-1])[0]}.png")
