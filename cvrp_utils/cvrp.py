# from .utils import split_roads
from typing import Any


def split_roads(chromosome, p) -> list[list]:
    route: list[list] = []
    sub_route = []
    load = 0
    # last_customer = 0

    for c in chromosome:
        demand = p.demands[c]

        new_load = load + demand

        if new_load <= p.capacity:
            sub_route.append(c)
            load = new_load
        else:
            route.append(sub_route)
            sub_route = [c]
            load = demand

    if sub_route:
        route.append(sub_route)

    return route


def get_fitness(chromosome: list, cost: float, p: Any) -> tuple[int, float]:
    total_cost = 0
    routes = split_roads(chromosome, p)
    trucks = len(routes)
    for s_route in routes:
        distance = 0
        last_customer = p.depots[0]

        for c in s_route:
            d = p.get_weight(last_customer, c)

            distance += d
            last_customer = c

        distance += p.get_weight(last_customer, p.depots[0])
        # distance -= p.get_weight(1, s_route[0])
        total_cost += cost * distance

    return trucks, total_cost
