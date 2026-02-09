# Input is an inputString: "US:UK:UPS:4,US:UK:DHL:5,UK:CA:FedEx:10,AU:JP:DHL:20" Format: sourceCountry:targetCountry:method:cost
#
# Part 1:
# Write a method that takes (inputString, sourceCountry, targetCountry, method) as input and outputs the cost. Concatenate sourceCountry, targetCountry, method to use as a key. Handle edge cases: what to return if the country is not found, how to handle empty strings.
#
# Part 2:
# If one intermediate country is allowed, output a structure. For example, if the input is US and CA, output:
#
# {
# route: "US -> UK -> CA",
# method: "UPS -> FedEx",
# cost: 14
# }
# No need to calculate the lowest cost; any intermediate country and method are acceptable. The cost is the sum of the two methods' costs.
#
# Part 3:
# Calculate the lowest cost with at most one hop
#
# Part 4:
# Calculate the lowest cost.

from collections import defaultdict

def get_route_map(input_str):
    route_map = defaultdict(list)
    for line in input_str.split(","):
        source, target, curr_method, cost = line.split(":")
        cost = int(cost)
        route_map[source].append((target, curr_method, cost))
    return route_map

def get_cost(input_str, source_country, target_country, method):
    route_map = get_route_map(input_str)
    if source_country not in route_map:
        return "Source country not found"
    # Direct path
    for dest, curr_method, cost in route_map[source_country]:
        if dest == target_country and curr_method == method:
            return cost

    #Intermediate path:
    for dest, curr_method, cost in route_map[source_country]:
        for future_dest, future_method, future_cost in route_map[dest]:
            if target_country == future_dest:
                total_cost = cost + future_cost
                final_route = f"{source_country}->{dest}->{future_dest}"
                final_method = f"{curr_method}->{future_method}"
                return {
                    "route": final_route,
                    "method": final_method,
                    "cost": total_cost
                }

    return "Destination and corresponding method not found"

def lowest_cost_helper(source_country, destination_country, route_map, result, cost_so_far, past_path):
    for dest, method, cost in route_map[source_country]:
        if dest not in past_path or cost_so_far+cost < result[dest]:
            result[dest] = cost_so_far+cost
            lowest_cost_helper(dest, destination_country, route_map, result, cost_so_far + cost, past_path | {dest})

def get_lowest_cost(input_str, source_country, destination_country):
    route_map = get_route_map(input_str)
    result = {source_country: 0}
    lowest_cost_helper(source_country, destination_country, route_map, result, 0, {source_country})

    return result[destination_country] if destination_country in result else -1
