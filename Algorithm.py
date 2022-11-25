import ReadInputFromExcel
import Util
from Route import Route

routes = []
passed_paths = 0


class Algorithm:
    def __init__(self):
        ReadInputFromExcel.extract_number_of_stations()  # Read stations from input file
        ReadInputFromExcel.extract_station_demand_sheet()  # Read demands of stations from input file
        ReadInputFromExcel.extract_distance_sheet()  # Read distances between the stations from input file
        ReadInputFromExcel.extract_truck_sheet()  # Read available trucks from input file
        calculate_savings()  # Calculate savings for paths
        make_routes()  # Populate optimal routes


# Calculates the saving for round trip of a station and base station
# Formula for the saving is: saving = cost(0,x) + cost(0,y) - cost(x,y) where 0 is base station, x is start station for
# the path and y is end station for the path
def calculate_savings():
    for path in ReadInputFromExcel.paths:
        if path.start.stationNum != 0:
            saving = Util.get_cost_of_path_to_depot(path.start.stationNum) + \
                     Util.get_cost_of_path_to_depot(path.end.stationNum) - path.cost
            if saving < 0:
                path.saving = 0.0
            else:
                path.saving = saving
    ReadInputFromExcel.paths.sort(key=sort_saving, reverse=True)  # Sort paths by ordering savings


def sort_saving(path):
    return path.saving


def sort_earliest_time(station):
    return station.earliest_time


def sort_latest_time(station):
    return station.latest_time


def make_routes():
    global passed_paths
    paths_without_depot = [path for path in ReadInputFromExcel.paths if
                           path.start.stationNum != 0]  # Remove the base station since it is fixed location
    size_of_paths = len(paths_without_depot)
    while ReadInputFromExcel.NUM_OF_STATIONS_WITH_DEPOT > 1:
        for path in paths_without_depot:
            passed_paths += 1
            if len(routes) == 0:
                # If there is no route added before, initialize the very first route with the highest savings path
                make_new_route(path)
            elif not Util.routes_contain_station(path.start, routes) or not Util.routes_contain_station(path.end,
                                                                                                        routes):
                # If there is a route added before and there is a path that at least one of its stations
                # is not added into any route, first try to merge the routes, if merge is not successful,
                # make a new route from that station
                is_added, station = try_merge_or_add_new_route(path)
                if not is_added and passed_paths > size_of_paths and station is not None:
                    make_new_route_from_station(station)

    for route in routes:
        route.inner_stations.sort(key=sort_latest_time, reverse=True)
    for route in routes:
        route.inner_stations.sort(key=sort_earliest_time, reverse=False)
    print_result(routes)


# If a new path has not been added into a route before, if capacity of truck is not passed over yet,
# then add both stations of path into a same route. If the capacity of truck is not sufficient to satisfy total
# demand of the stations, make two separate routes using each station
def make_new_route(path):
    global passed_paths
    if (path.start.demand + path.end.demand) > ReadInputFromExcel.trucks[1].capacity:
        routes.append(Route([path.start]))
        routes.append(Route([path.end]))
    else:
        routes.append(Route([path.start, path.end]))
    ReadInputFromExcel.NUM_OF_STATIONS_WITH_DEPOT -= 2
    passed_paths = 0


# Make a new route by using a single station
def make_new_route_from_station(station):
    global passed_paths
    routes.append(Route([station]))
    ReadInputFromExcel.NUM_OF_STATIONS_WITH_DEPOT -= 1
    passed_paths = 0


# For the candidate path to be added into a route, first traverse through all previously created routes.
# First, check if there is a route that contains start station of path. If there is, see if truck's capacity is
# enough for adding end station to that route.
# Then, check if there is a route that contains end station of path. If there is, see if truck's capacity is
# enough for adding start station to that route.
# Keep all possible route options, then evaluate them to find the best fit.
# If there is no route that contains either of stations of the path, then create a new route using those stations.
def try_merge_or_add_new_route(path):
    global passed_paths
    size = len(routes)
    candidate_routes = {}
    for i in range(size):
        route = routes[i]
        if Util.route_contains_station(route, path.start) and (
                Util.total_demand_of_route(route) + path.end.demand <= ReadInputFromExcel.trucks[1].capacity):
            add_to_candidate_routes(candidate_routes, route, path.end)
        elif Util.route_contains_station(route, path.end) and (
                Util.total_demand_of_route(route) + path.start.demand <= ReadInputFromExcel.trucks[1].capacity):
            add_to_candidate_routes(candidate_routes, route, path.start)
        elif not Util.routes_contain_station(path.start, routes) and not Util.routes_contain_station(path.end, routes):
            make_new_route(path)
            return True, None
    if len(candidate_routes) > 0:
        is_added, station = evaluate_candidate_routes(candidate_routes)
        if is_added:
            ReadInputFromExcel.NUM_OF_STATIONS_WITH_DEPOT -= 1
            passed_paths = 0
            return True, None
        else:
            return False, station
    else:
        return False, None


def add_to_candidate_routes(candidate_routes, route_to_be_added, station):
    if candidate_routes.__contains__(station):
        candidate_routes[station].append(route_to_be_added)
    else:
        candidate_routes.__setitem__(station, route_to_be_added)


# If this snippet is being called, that means a station is candidate to be added in at least one route.
# Traverse through all routes, find the optimal route that maximizes demand without passing the truck's capacity
# minimizes the cost and satisfies the timeline of the stations.
def evaluate_candidate_routes(candidate_routes_dict):
    candidate_routes = list(candidate_routes_dict.values())
    stations = list(candidate_routes_dict.keys())
    route = candidate_routes[0]
    candidate_routes_size = len(candidate_routes_dict)
    index_of_selected_route = 0
    for i in range(candidate_routes_size):
        if ((i + 1 < candidate_routes_size) and (
                (Util.total_demand_of_route(candidate_routes[i]) + stations[i].demand) <
                (Util.total_demand_of_route(candidate_routes[i + 1] + stations[i + 1].demand)))):
            route = candidate_routes[i + 1]
            index_of_selected_route = i + 1
    time_passed_so_far = Util.calculate_total_time_passed(route, stations[index_of_selected_route])
    if time_passed_so_far < ReadInputFromExcel.stations[0].latest_time - ReadInputFromExcel.stations[0].earliest_time:
        temp = route.inner_stations.copy()
        temp.append(stations[index_of_selected_route])
        temp.sort(key=sort_latest_time, reverse=True)
        temp.sort(key=sort_earliest_time, reverse=False)
        if Util.calculate_final_time(Route(temp)) < ReadInputFromExcel.stations[0].latest_time - \
                ReadInputFromExcel.stations[0].earliest_time:
            route.inner_stations.append(stations[index_of_selected_route])
            return True, None
        else:
            return False, stations[index_of_selected_route]
    else:
        return False, stations[index_of_selected_route]


# Output the results
def print_result(results):
    for route in results:
        is_big_truck = True
        print("0 - ", end="")
        for station in route.inner_stations:
            print(str(station.stationNum) + " - ", end="")
        truck = "BIG"
        if Util.total_demand_of_route(route) <= ReadInputFromExcel.trucks[0].capacity:
            truck = "SMALL"
            is_big_truck = False
        print("0 ------> " + truck + " ------ total demand of route ------> " + str(
            Util.total_demand_of_route(route)) + " ------ total cost of route ------> " + str(
            Util.calculate_cost_of_route(route, is_big_truck)) + " ------ total time passed ------> " + str(
            Util.calculate_final_time(route)), end="")
        print("\n")
        ReadInputFromExcel.print_results_into_excel(results)
