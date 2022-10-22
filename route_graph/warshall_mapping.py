import pandas as pd
import networkx as nx

import os


def _get_node(route) -> tuple:
    travel_time = ((route.distance / 1000) / 30) * 60
    return tuple([route.source_point_id, route.target_point_id, {'weight': travel_time}])


def get_warshall_mapping():
    path = 'data/Distance.xlsx'
    if os.path.exists(path):
        routes = pd.read_excel('data/Distance.xlsx', sheet_name='Roads', index_col='road_id')
    else:
        raise IOError(f'Exception in {__file__}: No such file or directory: {path}')

    all_points = list(set(routes.source_point_id) | set(routes.target_point_id))

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
