import Path
import ReadInputFromExcel


# How much does it cost to trip from base station(0) to given station
def get_cost_of_path_to_depot(station_num: int) -> float:
    for path in ReadInputFromExcel.paths:
        if ((path.start.stationNum == 0 and path.end.stationNum == station_num) or
                (path.start.stationNum == station_num and path.end.stationNum == 0)):
            return path.cost


# Traverse all routes to check if any of them contains a specific station in it
def routes_contain_station(station, routes) -> bool:
    for route in routes:
        if station in route.inner_stations:
            return True
    return False


# Check if a route contains a specific station in it
def route_contains_station(route, station) -> bool:
    return station in route.inner_stations


# Calculate total demand needed by the stations in a route
def total_demand_of_route(route) -> float:
    demand = 0.0
    for station in route.inner_stations:
        demand += station.demand
    return demand


# Calculate the total cost of the route for the given truck type
def calculate_cost_of_route(route, is_big_truck) -> float:
    total_cost = 0.0
    inner_stations = route.inner_stations
    num_of_inner_stations = len(inner_stations)
    total_cost += calculate_cost_to_depot(inner_stations[0], is_big_truck)
    total_cost += calculate_cost_to_depot(route.inner_stations[num_of_inner_stations - 1], is_big_truck)
    for index in range(0, num_of_inner_stations - 1):
        total_cost += calculate_cost_between_two_stations(inner_stations[index], inner_stations[index + 1],
                                                          is_big_truck)
    if is_big_truck:
        total_cost += ReadInputFromExcel.trucks[1].rent
    else:
        total_cost += ReadInputFromExcel.trucks[0].rent
    return total_cost


# Calculate the cost between two stations for given truck type. The calculation is
# basically (distance between two stations) * (fuel per km) for the truck
def calculate_cost_between_two_stations(station1, station2, is_big_truck) -> float:
    distance = find_proper_path(station1.stationNum, station2.stationNum).cost
    if is_big_truck:
        return distance * ReadInputFromExcel.trucks[1].fuelPerKm
    else:
        return distance * ReadInputFromExcel.trucks[0].fuelPerKm


# Calculate the cost between the base station and the given station for given truck type
def calculate_cost_to_depot(station, is_big_truck) -> float:
    distance = find_proper_path(0, station.stationNum).cost
    if is_big_truck:
        return distance * ReadInputFromExcel.trucks[1].fuelPerKm
    else:
        return distance * ReadInputFromExcel.trucks[0].fuelPerKm


# Find a path between two stations
def find_proper_path(start, end) -> Path:
    paths = ReadInputFromExcel.paths
    path = [path for path in paths if compare_path(path, start, end)]
    return path[0]


# Check if a path is correct for given two stations
def compare_path(path, start, end) -> bool:
    return (path.start.stationNum == start and path.end.stationNum == end) or \
           (path.end.stationNum == start and path.start.stationNum == end)


# Calculate how much time would pass if given station is added to the route
def calculate_total_time_passed(route, station_to_add) -> float:
    time_passed = find_proper_path(0,
                                   route.inner_stations[0].stationNum).timeSpentBetween  # Time spent for base station
    inner_stations = route.inner_stations  # Get all inner stations in that route
    num_of_inner_stations = len(inner_stations)
    for index in range(0, num_of_inner_stations - 1):
        # Add time spent between stations(in path) and time spent in the station
        time_passed += find_proper_path(inner_stations[index].stationNum,
                                        inner_stations[index + 1].stationNum).timeSpentBetween
        time_passed += inner_stations[index].time_to_spend
    time_passed += find_proper_path(0, station_to_add.stationNum).timeSpentBetween
    time_passed += find_proper_path(route.inner_stations[len(route.inner_stations) - 1].stationNum,
                                    station_to_add.stationNum).timeSpentBetween
    time_passed += station_to_add.time_to_spend
    return time_passed


# Calculate total time passed for the given route
def calculate_final_time(route) -> float:
    temp_stations = route.inner_stations.copy()
    temp_stations.insert(0, ReadInputFromExcel.stations[0])
    temp_stations.append(ReadInputFromExcel.stations[0])
    num_of_inner_stations = len(temp_stations)
    time_passed = 0
    for index in range(0, num_of_inner_stations - 1):
        time_passed += find_proper_path(temp_stations[index].stationNum,
                                        temp_stations[index + 1].stationNum).timeSpentBetween
        time_passed += temp_stations[index].time_to_spend
    return time_passed
