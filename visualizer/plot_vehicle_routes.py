import matplotlib.pyplot as plt
import numpy as np


def plot_sub_route(sub_route, coordinates, depot):
    color = np.random.rand(1, 3)
    temp_route = sub_route[:]

    plt.plot([depot[0], coordinates[temp_route[0]-1][0]],
             [depot[1], coordinates[temp_route[0]-1][1]], c=color)

    for i in range(1, len(sub_route)):
        first_cust = temp_route[0] - 1
        second_cust = temp_route[1] - 1
        plt.plot([coordinates[first_cust][0], coordinates[second_cust][0]],
                 [coordinates[first_cust][1], coordinates[second_cust][1]], c=color)
        temp_route.pop(0)

    plt.plot([depot[0], coordinates[sub_route[-1] - 1][0]],
                 [depot[1], coordinates[sub_route[-1] - 1][1]], c=color)


def plot_route(test_name: str, routes: list[list[int]], coordinates: list[tuple[int, int]], depot: tuple[int, int]):
    plt.figure(figsize=(10, 10))
    plt.scatter(depot[0], depot[1], c='green', s=100)
    plt.text(depot[0], depot[1], "depot", fontsize=12)

    for i in range(1, len(coordinates)):
        plt.scatter(coordinates[i][0], coordinates[i][1], c='orange', s=100)
        plt.text(coordinates[i][0], coordinates[i][1], f'{i}', fontsize=12)

    for route in routes:
        plot_sub_route(route, coordinates, depot)

    plt.xlabel("X - Coordinate")
    plt.ylabel("Y - Coordinate")
    plt.title(test_name)
    plt.savefig(f"Route_{test_name}.png")

# plot_route("test", [[1, 3, 2], [4, 5, 6]], [ (3, 0), (1, 3), (3, 2), (3, 3), (5, 2), (6, 3), (7, 1)], (3, 0))
# plt.show()

