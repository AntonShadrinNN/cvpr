import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

def plot_conv(test_name: str, costs: list[float]):
    plt.figure(figsize=(10, 10))
    iterations = list(range(1, len(costs) + 1))
    X_Y_Spline = make_interp_spline(iterations, costs)
    X_ = np.linspace(min(iterations), max(iterations), 500)
    Y_ = X_Y_Spline(X_)

    plt.plot(X_, Y_)
    plt.xlabel("Generations")
    plt.ylabel("Min distance")
    plt.title(test_name)
    plt.savefig(f"Fitness_{test_name}.png")


# plot_conv("test", [3222, 3567, 2976])
