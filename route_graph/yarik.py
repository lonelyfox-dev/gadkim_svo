import pandas as pd
import networkx as nx

import os

import module_time.moduleTemplate as mt


###################
# WARSHALL MAPPING
###################


def _get_node(route) -> tuple:
    travel_time = ((route.distance / 1000) / 30) * 60
    return tuple([route.source_point_id, route.target_point_id, {'weight': travel_time}])


def _get_routes_points(path='route_graph/data/Distance.xlsx'):
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        routes = pd.read_excel(abs_path, sheet_name='Roads', index_col='road_id')
    else:
        raise IOError(f'Exception in {__file__}: No such file or directory: {abs_path}')

    all_points = list(set(routes.source_point_id) | set(routes.target_point_id))
    return routes, all_points


def get_warshall_mapping():
    routes, all_points = _get_routes_points()

    edges = list(routes.apply(_get_node, axis=1).values)
    graph = nx.DiGraph(edges)

    predecessors, distances = nx.floyd_warshall_predecessor_and_distance(graph)

    warshall_map = {}
    for source_point in all_points:
        warshall_map[source_point] = {}
        warshall_map[source_point]['distance'] = {}
        warshall_map[source_point]['route'] = {}

        for destination_point in all_points:
            warshall_map[source_point]['distance'][destination_point] = distances[source_point][destination_point]
            warshall_map[source_point]['route'][destination_point] = nx.reconstruct_path(
                source_point,
                destination_point,
                predecessors
            )

    return warshall_map


######################
# YARIK CONTROL LOGIC
######################

def wake_yarik():
    default_spawnpoint_id = 4
    bus_capacities = [100] * 30 + [50] * 10

    drivers = []
    for driver_id, bus_capacity in enumerate(bus_capacities):
        drivers.append({
            'id': driver_id,
            'location': default_spawnpoint_id,
            'destination': None,
            'task_id': None,
            'capacity': bus_capacity,
            'free_time': None
        })

    future_events_chain = None

    return drivers, future_events_chain


__warshall_map = get_warshall_mapping()
__drivers, __future_events_chain = wake_yarik()
__global_model_time = 0


def yarik_driver_manager(drivers: list, future_events_chain, global_model_time, warshall_map: dict):
    __global_model_time = global_model_time

    if future_events_chain is None:
        future_events_chain = [0] * 40
        for driver in drivers:
            driver_id = driver['id']
            if driver['task_id'] is None:
                future_events_chain[driver_id] = (driver_id, 0)
    else:
        # Update drivers position according to the time passed
        for driver_id, event_model_time in future_events_chain:
            if drivers[driver_id]['task_id'] is None:
                continue
            # If the model time moved enough to trigger a driver's event
            if global_model_time >= event_model_time:
                # Get destination, old_location and new location
                destination = drivers[driver_id]['destination']
                old_location = drivers[driver_id]['location']
                location = warshall_map[old_location]['route'][destination][1]

                # Get time travelled to the new point
                travel_time = warshall_map[location]['distance'][old_location]

                # If the driver reached his destination
                if location == destination:
                    drivers[driver_id]['location'] = destination
                    drivers[driver_id]['task_id'] = None
                    drivers[driver_id]['destination'] = None
                    drivers[driver_id]['free_time'] = None
                    continue

                drivers[driver_id]['location'] = location
                drivers[driver_id]['free_time'] -= travel_time

    __future_events_chain = _update_future_events_chain(future_events_chain, global_model_time, drivers, warshall_map)


def _update_future_events_chain(future_events_chain: list, global_model_time, drivers: list, warshall_map: dict):
    for driver in drivers:
        if driver['task_id'] is None:
            continue

        # Get current driver location, destination and the next route point
        location = driver['location']
        destination = driver['destination']
        next_point = warshall_map[location]['route'][destination][1]

        # Get time until the next point, update future events chain
        event_model_time = warshall_map[location]['distance'][next_point] + global_model_time
        future_events_chain[driver['id']] = (driver['id'], event_model_time)

    return sorted(future_events_chain, key=lambda tup: tup[1])


def get_time_move_drivers(synch_params):
    print(synch_params['model-time'])
    yarik_driver_manager(__drivers, __future_events_chain, synch_params, __warshall_map)


def assign_task(synch_params):
    driver_id = synch_params['driver_id']
    task_id = synch_params['task_id']
    location = __drivers[driver_id]['location']
    destination = synch_params['destination']

    __drivers[driver_id]['destination'] = destination
    __drivers[driver_id]['task_id'] = task_id
    __drivers[driver_id]['free_time'] = __warshall_map[location]['distance'][destination]

    yarik_driver_manager(__drivers, __future_events_chain, __global_model_time, __warshall_map)


params = [
    ['get', '/model-time', get_time_move_drivers],
    ['put', '/put', assign_task],
    ['post', '/post', assign_task]
]
mt.init(5000, 'yarik', params)
