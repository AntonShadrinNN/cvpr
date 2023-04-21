from .cvrp import split_roads


def print_routes(ind: list[list], p):
    route = split_roads(ind, p)
    route_str = '0'
    sub_route_count = 0
    for sub_route in route:
        sub_route_count += 1
        sub_route_str = '0'
        for customer_id in sub_route:
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
        sub_route_str = f'{sub_route_str} - 0'
        print(f'  Vehicle {sub_route_count}\'s route: {sub_route_str}')
        route_str = f'{route_str} - 0'
    print(f'  Cost for the transportation is {calculate_distance_from_solution(route, p)}')


def calculate_distance_from_solution(solution: list[list], p):
    total = 0
    for line in solution:
        last = line[0]
        temp = p.get_weight(p.depots[0], last)
        for c in range(1, len(line)):
            s_distance = p.get_weight(last, int(line[c]))
            temp += s_distance
            total += s_distance
            last = c

    return total
