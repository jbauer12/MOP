import csv

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Daten werden von CSV Datei geladen.
with open('./../data/Wednesday.csv', 'r', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=";")
    distance_matrix = [row for row in rows]
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix[i])):
            # Einträge sind in KM
            distance_matrix[i][j] = abs(int(float(distance_matrix[i][j]) / 1000))

with open('./../data/Wednesdaybedarfe.csv', 'r', newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=",")
    bedarfe = [abs(int(demand)) for coordinates, demand in rows]
    print(f'Bedarfe ingesamt: {sum(bedarfe)}')


# TODO prüfen ob das stimmt -> grundlegend dieselbe Logik wie bei Overlay
def computeCosts(data, from_index, to_index, verbrauch):
    pakete = data['demands'][to_index]

    def getBenzinCosts(distance_in_km, consumption_per_100km):
        distance_in_hundred_km = distance_in_km / 100
        cost_per_100km = 2.1 * consumption_per_100km
        return distance_in_hundred_km * cost_per_100km

    def getCostsPerPaket(zeit_pro_paket_in_std):
        return stundensatz_mitarbeiter * zeit_pro_paket_in_std

    def getCostFromWorkerPerKM(distance_in_km):
        return getTimeConsumptionFromOneNodeToAnotherForCosts(distance_in_km) * stundensatz_mitarbeiter

    def getTimeConsumptionFromOneNodeToAnotherForCosts(distance_in_km):
        time_for_one_km = 1 / 30  # eine Dreißigstelstunde braucht man um km zu fahren.
        time = distance_in_km * time_for_one_km
        return time

    costs = int((getBenzinCosts(data['distance_matrix'][from_index][to_index], verbrauch) + getCostsPerPaket(
        zeit_pro_paket_in_std) * pakete + getCostFromWorkerPerKM(
        data['distance_matrix'][from_index][to_index])) * multiplier)
    return costs


def costs_for_cargoType1(from_index, to_index, data):
    """Gibt Kosten für Nutzen von Kante für Fahrzeugtyp 1 zurück"""
    # Convert from routing variable Index to distance matrix NodeIndex.
    # Anzahl Pakete
    return computeCosts(data, from_index, to_index, 10.3)


def computeDistanceMatrixCargo1():
    data = create_data_model()
    cargo1 = []
    for i in range(len(data['distance_matrix'])):
        innerlist = []
        for j in range(len(data['distance_matrix'])):
            innerlist.append(costs_for_cargoType1(i, j, data))
        cargo1.append(innerlist)
    return cargo1


def costs_for_cargoType2(from_index, to_index, data):
    """Gibt Kosten für Nutzen von Kante für Fahrzeugtyp 2 zurück"""
    # Convert from routing variable Index to distance matrix NodeIndex.
    return computeCosts(data, from_index, to_index, 11.1)


def computeDistanceMatrixCargo2():
    data = create_data_model()
    cargo1 = []
    for i in range(len(data['distance_matrix'])):
        innerlist = []
        for j in range(len(data['distance_matrix'])):
            innerlist.append(costs_for_cargoType2(i, j, data))
        cargo1.append(innerlist)
    return cargo1


def costs_for_cargoType3(from_index, to_index, data):
    """Gibt Kosten für Nutzen von Kante für Fahrzeugtyp 3 zurück"""
    # Convert from routing variable Index to distance matrix NodeIndex.
    return computeCosts(data, from_index, to_index, 14.2)


def computeDistanceMatrixCargo3():
    data = create_data_model()
    cargo3 = []
    for i in range(len(data['distance_matrix'])):
        innerlist = []
        for j in range(len(data['distance_matrix'])):
            innerlist.append(costs_for_cargoType3(i, j, data))
        cargo3.append(innerlist)
    return cargo3


def getTimeConsumptionFromOneNodeToAnother(distance_in_km):
    time_for_one_km = 1 / 30  # eine Dreißigstelstunde braucht man um km zu fahren.
    time = int(distance_in_km * time_for_one_km * multiplier)
    return time


# Constraint Programmierung --> Kann keine Fließkommazahlen -> Man multipliziert alle Kosten einfach mit 10000 -> Ganzzahlergebnis.
multiplier = 1000
# 23.612...
# Verbund
# TODO stimmen diese Werte für Verbund??
stundensatz_mitarbeiter = (40000 / 220) / 7.7
zeit_pro_paket_in_std = 0.0139
max_zeit_fahrer = 6.5 * multiplier


def create_data_model():
    data = {}

    data['distance_matrix'] = distance_matrix
    data['demands'] = bedarfe

    data['vehicle_capacities'] = 7 * [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
                                      30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
                                      30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
                                      60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60,
                                      60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60,
                                      60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60,
                                      200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                                      200, 200, 200, 200,
                                      200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                                      200, 200, 200, 200,
                                      200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200,
                                      200, 200, 200, 200
                                      ]  # Wenn hier Inhalt/Länge geändert --> unten auch ändern
    data['num_vehicles'] = len(data['vehicle_capacities'])
    data['startsends'] = 180 * [0, 1, 2, 3, 4, 5, 6]
    # Liste ist ein Depot -- jedes Depot soll drei Fahrzeuge haben unterschiedlichen Typs
    # Fixkosten pro Jahr und Tag gemeinsam --> wird an einem Tag genutzt -> Beides fällt an (Kann man sich auch was anderes überlegen)
    data['fixcostsyearAndDay'] = [int(3790 + 0.3 * stundensatz_mitarbeiter) * multiplier,
                                  int(4570 + 0.3 * stundensatz_mitarbeiter) * multiplier,
                                  int(9225 + 0.3 * stundensatz_mitarbeiter) * multiplier]
    return data


def main():
    # Instanzieren des Problems
    data = create_data_model()

    # Den Indexmanager instanzieren --> data[startsends] sorgt dafür das die jeweiligen Fahrzeuge bei ihrem Depot anfangen und aufhören
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['startsends'], data['startsends'])

    # Erstellt auf Grundlage des Managers das Model.
    parameterss = pywrapcp.DefaultRoutingModelParameters()
    # Cachen von Zwischenergebnissen auf Solverseite.
    parameterss.max_callback_cache_size = 2000 * 2000 * 2
    routing = pywrapcp.RoutingModel(manager, parameterss)

    cargo1 = computeDistanceMatrixCargo1()
    cargo2 = computeDistanceMatrixCargo2()
    cargo3 = computeDistanceMatrixCargo3()

    # Gibt dem Solver bescheid das "Callback existiert" und übergibt die Funktion an den Solver --> macht sie nutzbar.
    transit_callback_index_c1 = routing.RegisterTransitMatrix(cargo1)
    transit_callback_index_c2 = routing.RegisterTransitMatrix(cargo2)
    transit_callback_index_c3 = routing.RegisterTransitMatrix(cargo3)

    # TODO Prüfen ob Time_Callbck richtig berechnet wird.
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return getTimeConsumptionFromOneNodeToAnother(data['distance_matrix'][from_node][to_node])

    time_worker_fn_index = routing.RegisterTransitCallback(time_callback)

    routing.AddDimension(
        time_worker_fn_index,  # total time function callback
        0,
        int(max_zeit_fahrer),
        True,
        'Time')

    # Setzt für die verschiedenen Fahrzeugtypen Kostenfunktionen und Fixkosten
    # Zugehörigkeit  eines Fahrzeugs zu Kostentyp anhand Stelle in der Liste.
    # Wann ist ein Fahrzeug Cargotyp 1? --> mod 3 =0
    # Wann ist ein Fahrzeug Cargotyp 2? --> mod 3 =1
    # Wann ist ein Fahrzeug Cargotyp 3? --> mod 3 =2
    # Es wird praktisch die Position im Array bestimmt. erstes Drittel im Array --> also erste 60 Fahrzeuge im Depot --> Kapazität 30
    # TODO prüfen ob Kostenfunktion richtig gesetzt wird und Fixkosten richtig gesetzt werden.
    for vehicle_id in range(data['num_vehicles']):
        if vehicle_id % 180 < 60:
            routing.SetArcCostEvaluatorOfVehicle(transit_callback_index_c1, vehicle_id)
            routing.SetFixedCostOfVehicle(data['fixcostsyearAndDay'][0], vehicle_id)
        elif vehicle_id % 180 < 120:
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
    #search_parameters.time_limit.seconds = 15 * 60
    search_parameters.solution_limit = 1

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        get_routes(data,solution, routing, manager)
    else:
        # 2 --> keine Lösung gefunden
        # 3 --> Zeit reichte nicht aus um Lösung zu finden.
        # SWEEP nur für C++ Version verfügbar scheinbar
        print(routing.status())


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if solution.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    print(dropped_nodes)
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n '.format(vehicle_id)
        if vehicle_id % 180 < 60:
            print("Typ 1 in Depot: " + str(data['num_vehicles'] // 180))
        elif vehicle_id % 180 < 120:
            print("Typ 2 in Depot " + str(data['num_vehicles'] // 180))
        else:
            print("Typ 3 in Depot " + str(data['num_vehicles'] // 180))
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


def get_routes(data, solution, routing, manager):
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    routes = []
    for vehicle_id in range(data['num_vehicles']):
        route = []
        innerroute = []
        index = routing.Start(vehicle_id)
        # erste Spalte vehicle_id
        route.append(vehicle_id)
        # Typ
        if vehicle_id % 180 < 60:
            route.append(1)
        elif vehicle_id % 180 < 120:
            route.append(2)
        else:
            route.append(3)
        # Depot
        route.append(data['num_vehicles'] // 180)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            # Tupel --> erstes Wo fahr ich hin zweites, aktuell ausgeliefert
            innerroute.append((node_index, route_load))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        # letzter angefahrene Kunde?
        innerroute.append((manager.IndexToNode(index), route_load))
        # Kosten der Route
        route.append(route_distance // multiplier)
        # Pakete je Route
        route.append(route_load)
        route.extend(innerroute)
        routes.append(route)
        total_distance += route_distance
        total_load += route_load


    # opening the csv file in 'w+' mode
    file = open('klein.csv', 'w+', newline='')

    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(routes)


if __name__ == '__main__':
    main()
