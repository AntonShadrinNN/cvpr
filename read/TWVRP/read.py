from __future__ import annotations


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance(a: Point, b: Point) -> float:
        return ((b.x - a.x) ** 2 + (b.y - a.y) ** 2) ** 0.5


class Problem:
    def __init__(self):
        self.instance: str = ''
        self.dimension: int = 0
        self.demands: list = []
        self.depots: list = [0]
        self.weights: list = []
        self.ready_times: list = []
        self.due_dates: list = []
        self.service_times: list = []
        self.capacity: int = 0
        self.vehicles: int = 0

    def get_weight(self, src, dst):
        p1 = Point(self.weights[src-1][0], self.weights[src-1][1])
        p2 = Point(self.weights[dst-1][0], self.weights[dst-1][1])
        return Point.distance(p1, p2)


def parse(path: str) -> Problem:
    problem = Problem()
    with open(path, "r", encoding="utf-8") as instance:
        data = instance.readlines()

    problem.instance = data[0].strip()
    problem.vehicles, problem.capacity = list(map(int, data[4].strip().split()))

    for line in range(10, len(data)):
        c_params = list(map(int, data[line].strip().split()))
        problem.weights.append((c_params[1], c_params[2]))
        problem.demands.append(c_params[3])
        problem.ready_times.append(c_params[4])
        problem.due_dates.append(c_params[5])
        problem.service_times.append(c_params[6])
        problem.dimension += 1

    problem.demands = [0] + problem.demands
    return problem

