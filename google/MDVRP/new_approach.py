import csv
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

with open('./../data/Wednesday.csv', 'r', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=";")
    distance_matrix = [row for row in rows]
    # Spaßeswegen Umschreiben in list comprehension
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix[i])):
            distance_matrix[i][j] = int(float(distance_matrix[i][j]))
with open('./../data/Wednesdaybedarfe.csv', 'r', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=",")
    bedarfe = [int(demand) for coordinates, demand in rows]


def getBenzinCosts(distance_in_meters, consumption_per_100km):
    distance_in_km = distance_in_meters / 1000
    distance_in_hundred_km = distance_in_km / 100
    cost_per_100km = 2.1 * consumption_per_100km
    return int(distance_in_hundred_km * cost_per_100km * multiplier)


def getCostFromWorkerPerKM(distance_in_meters, stundensatz):
    return int(getTimeConsumptionFromOneNodeToAnother(distance_in_meters) * stundensatz)


def getTimeConsumptionFromOneNodeToAnother(distance_in_meters):
    time_for_one_km = 1 / 30  # eine Dreißigstelstunde braucht man um km zu fahren.
    distance_in_km = distance_in_meters / 1000
    return int(distance_in_km * time_for_one_km * multiplier)


def getCostsPerAbgabeStelle():
    return int(zeit_weg_vom_wagen_zum_haus_und_zurueck * stundensatz_mitarbeiter)


def getCostsPerPaket(stundensatz, zeit_pro_paket_in_std):
    return int(stundensatz * zeit_pro_paket_in_std)


# TODO alle Kostenfunktionen in einer Funktion schachteln und schauen dass nur einmal gerundet wird.
# Constraint Programmierung --> Kann keine Fließkommazahlen -> Man multipliziert alle Kosten einfach mit 10000 -> Ganzzahlergebnis.
multiplier = 10000
# 23.612...
# Overlay
stundensatz_mitarbeiter = (40000 / 220) / 7.7
zeit_pro_paket_in_std = (0.0131 + 0.0055 + 0.0005 + 0.0133) * multiplier
zeit_weg_vom_wagen_zum_haus_und_zurueck = 0.0133 * multiplier


def create_data_model():
    data = {}

    data['distance_matrix'] = distance_matrix
    data['demands'] = bedarfe
    data['vehicle_capacities'] = 7 * [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60,
                                      200, 200, 200, 200, 200, 200, 200, 200, 200,
                                      200, ]  # Wenn hier Inhalt/Länge geändert --> unten auch ändern
    data['num_vehicles'] = len(data['vehicle_capacities'])
    data['startsends'] = 30 * [0, 1, 2, 3, 4, 5, 6]
    # Liste ist ein Depot -- jedes Depot soll drei Fahrzeuge haben unterschiedlichen Typs
    # Fixkosten pro Jahr und Tag gemeinsam --> wird an einem Tag genutzt -> Beides fällt an (Kann man sich auch was anderes überlegen)
    data['fixcostsyearAndDay'] = [3790 * multiplier, 4570 * multiplier, 9225 * multiplier]







    return data


def main():
    # Instanzieren des Problems
    data = create_data_model()

    # Den Indexmanager instanzieren --> data[startsends] sorgt dafür das die jeweiligen Fahrzeuge bei ihrem Depot anfangen und aufhören
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['startsends'], data['startsends'])

    # Erstellt auf Grundlage des Managers das Model.

    parameterss = pywrapcp.DefaultRoutingModelParameters()
    parameterss.max_callback_cache_size = 2000 * 2000 * 2
    routing = pywrapcp.RoutingModel(manager, parameterss)


    # Erstelle jeweilige Kostenfunktionen für jeweiligen Fahrzeugtyp
    def costs_for_cargoType1(from_index, to_index):
        """Gibt Kosten für Nutzen von Kante für Fahrzeugtyp 1 zurück"""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # Anzahl Pakete
        pakete = data['demands'][to_node]
        return getBenzinCosts(data['distance_matrix'][from_node][to_node], 10.3) + getCostsPerPaket(
            stundensatz_mitarbeiter,
            zeit_pro_paket_in_std) * pakete + getCostsPerAbgabeStelle() + getCostFromWorkerPerKM(
            data['distance_matrix'][from_node][to_node], stundensatz_mitarbeiter)

    # Erstelle jeweilige Kostenfunktionen für jeweiligen Fahrzeugtyp
    def costs_for_cargoType2(from_index, to_index):
        """Gibt Kosten für Nutzen von Kante für Fahrzeugtyp 2 zurück"""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        pakete = data['demands'][to_node]
        return getBenzinCosts(data['distance_matrix'][from_node][to_node], 11.1) + getCostsPerPaket(
            stundensatz_mitarbeiter,
            zeit_pro_paket_in_std) * pakete + getCostsPerAbgabeStelle() + getCostFromWorkerPerKM(
            data['distance_matrix'][from_node][to_node], stundensatz_mitarbeiter)

    # Erstelle jeweilige Kostenfunktionen für jeweiligen Fahrzeugtyp
    def costs_for_cargoType3(from_index, to_index):
        """Gibt Kosten für Nutzen von Kante für Fahrzeugtyp 3 zurück"""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        pakete = data['demands'][to_node]
        return getBenzinCosts(data['distance_matrix'][from_node][to_node], 14.2) + getCostsPerPaket(
            stundensatz_mitarbeiter,
            zeit_pro_paket_in_std) * pakete + getCostsPerAbgabeStelle() + getCostFromWorkerPerKM(
            data['distance_matrix'][from_node][to_node], stundensatz_mitarbeiter)

    # Gibt dem Solver bescheid das "Callback existiert" und übergibt die Funktion an den Solver --> macht sie nutzbar.
    transit_callback_index_c1 = routing.RegisterTransitCallback(costs_for_cargoType1)
    transit_callback_index_c2 = routing.RegisterTransitCallback(costs_for_cargoType2)
    transit_callback_index_c3 = routing.RegisterTransitCallback(costs_for_cargoType3)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return getTimeConsumptionFromOneNodeToAnother(data['distance_matrix'][from_node][to_node])

    time_worker_fn_index = routing.RegisterTransitCallback(time_callback)

    routing.AddDimension(
        time_worker_fn_index,  # total time function callback
        0,
        int(6.5 * multiplier),
        True,
        'Time')

    # Setzt für die verschiedenen Fahrzeugtypen Kostenfunktionen und Fixkosten
    # Zugehörigkeit  eines Fahrzeugs zu Kostentyp anhand Stelle in der Liste.
    # Wann ist ein Fahrzeug Cargotyp 1? --> mod 3 =0
    # Wann ist ein Fahrzeug Cargotyp 2? --> mod 3 =1
    # Wann ist ein Fahrzeug Cargotyp 3? --> mod 3 =2
    for vehicle_id in range(data['num_vehicles']):
        if vehicle_id % 3 == 0:
            routing.SetArcCostEvaluatorOfVehicle(transit_callback_index_c1, vehicle_id)
            routing.SetFixedCostOfVehicle(data['fixcostsyearAndDay'][0], vehicle_id)
        elif vehicle_id % 3 == 1:
            routing.SetArcCostEvaluatorOfVehicle(transit_callback_index_c2, vehicle_id)
            routing.SetFixedCostOfVehicle(data['fixcostsyearAndDay'][1], vehicle_id)
        else:
            routing.SetArcCostEvaluatorOfVehicle(transit_callback_index_c3, vehicle_id)
            routing.SetFixedCostOfVehicle(data['fixcostsyearAndDay'][2], vehicle_id)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(100)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        # 2 --> keine Lösung gefunden
        # 3 --> Zeit reichte nicht aus um Lösung zu finden.
        #SWEEP nur für C++ Version verfügbar scheinbar
        print(routing.status())


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Kosten der Route: {}€\n'.format(route_distance // multiplier)
        plan_output += 'Anzahl Pakete Route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Gesamtkosten aller Routen: {}€'.format(total_distance // multiplier))
    print('ausgetragene Pakete aller Routen: {}'.format(total_load))


if __name__ == '__main__':
    main()
