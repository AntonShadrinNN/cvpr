import os

import matplotlib.pyplot as plt
import numpy as np


def get_data(file_name: str):
    routes = []
    coordinates = []
    depot = ()
    with open(file_name, encoding="utf-8") as file:
        cnt_coord = int(file.readline())

        depot = tuple(map(int, file.readline().split()))
        coordinates.append(depot)

        for _ in range(cnt_coord - 1):
            coord = tuple(map(int, file.readline().split()))
            coordinates.append(coord)

        cnt_rout = int(file.readline())

        for _ in range(cnt_rout):
            rout = list(map(int, file.readline().split()))
            routes.append(rout)

    return depot, coordinates, routes


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


def plot_routes(file_name: str):
    depot, coordinates, routes = get_data(file_name)

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
    title = f"{os.path.splitext(os.path.split(file_name)[-1])[0]}"
    plt.title(title)
    plt.savefig(f"..\\data\\plots\\{os.path.splitext(os.path.split(file_name)[-1])[0]}.png")
