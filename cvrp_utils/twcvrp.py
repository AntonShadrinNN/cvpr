from .read.TWVRP import Problem


def split_roads(individual, data: Problem) -> list[list]:
    vehicle_capacity = data.capacity
    depart_due_time = data.due_dates[data.depots[0]]

    route = []
    sub_route = []
    vehicle_load = 0
    time_elapsed = 0
    previous_cust_id = 1
    for customer_id in individual:
        demand = data.demands[customer_id - 1]
        updated_vehicle_load = vehicle_load + demand
        service_time = data.service_times[customer_id - 1]
        return_time = data.get_weight(customer_id, 1)
        travel_time = data.get_weight(previous_cust_id, customer_id)
        provisional_time = time_elapsed + travel_time + service_time + return_time
        # Validate vehicle load and elapsed time
        if (updated_vehicle_load <= vehicle_capacity) and (provisional_time <= depart_due_time):
            # Add to current sub-route
            sub_route.append(customer_id)
            vehicle_load = updated_vehicle_load
            time_elapsed = provisional_time - return_time
        else:
            # Save current sub-route
            route.append(sub_route)
            # Initialize a new sub-route and add to it
            sub_route = [customer_id]
            vehicle_load = demand
            travel_time = data.get_weight(1, customer_id)
            time_elapsed = travel_time + service_time
        # Update last customer ID
        previous_cust_id = customer_id
    if sub_route:
        # Save current sub-route before return if not empty
        route.append(sub_route)
    return route


def get_fitness(individual, p: Problem):

    route = split_roads(individual, p)
    max_vehicles_count = p.vehicles
    total_cost = 9999999999

    if len(route) <= max_vehicles_count:
        total_cost = 0
        for sub_route in route:
            sub_route_time_cost = 0
            distance = 0
            elapsed_time = 0
            previous_cust_id = 0
            for cust_id in sub_route:
                # Calculate section distance
                delta = p.get_weight(previous_cust_id, cust_id)
                # Update sub-route distance
                distance = distance + delta

                # Calculate time cost
                arrival_time = elapsed_time + delta

                waiting_time = max(p.ready_times[cust_id - 1] - arrival_time, 0)
                delay_time = max(arrival_time - p.due_dates[cust_id - 1], 0) * 9999999999
                time_cost = waiting_time + delay_time

                # Update sub-route time cost
                sub_route_time_cost += time_cost

                # Update elapsed time
                service_time = p.service_times[cust_id - 1]
                elapsed_time = arrival_time + service_time

                # Update last customer ID
                previous_cust_id = cust_id

            distance += p.get_weight(previous_cust_id, 1)
            total_cost += sub_route_time_cost + distance

    return len(route), total_cost
