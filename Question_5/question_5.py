# Question 5: Graph Algorithm
# Esmanur Yorulmaz - 210201008
# Canan Kılıç - 220201037

import time
from collections import deque, defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Breadth-First Search (BFS) to find an augmenting path with available residual capacity in the matrix representation
def bfs_capacity_path_matrix(graph, source, sink, parent):
    visited = [False] * len(graph)  # track visited nodes
    queue = deque([source])  # initialize queue with the source node
    visited[source] = True

    while queue:
        node = queue.popleft()
        for neigh, capacity in enumerate(graph[node]):
            # check for unvisited neighbors with available capacity
            if not visited[neigh] and capacity > 0:
                queue.append(neigh)
                visited[neigh] = True
                parent[neigh] = node  # track the path
                if neigh == sink:
                    return True  # found path to sink
    return False  # No path 

# BFS for the list representation of the graph
def bfs_capacity_path_list(graph, source, sink, parent):
    visited = set()  # track visited nodes
    queue = deque([source])
    visited.add(source)

    while queue:
        node = queue.popleft()
        for neigh, capacity in graph[node]:
            # check for unvisited neighbors with available capacity
            if neigh not in visited and capacity > 0:
                queue.append(neigh)
                visited.add(neigh)
                parent[neigh] = node  # track the path
                if neigh == sink:
                    return True  # found path to sink
    return False  # No path 

# trace back the path from sink to source using the parent array
def get_path(parent, source, sink):
    path = []
    current = sink
    while current != source:
        path.append(current)
        current = parent[current]
    path.append(source)
    return path[::-1]  # return reverse path

# Ford-Fulkerson Algorithm implementation using adjacency matrix representation
def ford_fulkerson_matrix(graph, source, sink):
    parent = [-1] * len(graph)  # store the path
    max_flow = 0  # initialize max flow
    paths = []  # store paths contributing (max flow) 

    # find augmenting paths while they exist (continue)
    while bfs_capacity_path_matrix(graph, source, sink, parent):
        flow_path = float('Inf')
        s = sink
        while s != source:
            flow_path = min(flow_path, graph[parent[s]][s])  # minimum capacity in path way
            s = parent[s]
        
        max_flow += flow_path  # add path flow to overall flow
        paths.append((get_path(parent, source, sink), flow_path))
        
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= flow_path  # update residual capacities
            graph[v][u] += flow_path  # update reverse flow
            v = parent[v]
    
    return max_flow, paths  # return the maximum flow and paths

# Ford-Fulkerson Algorithm implementation using adjacency list representation
def ford_fulkerson_list(graph, source, sink):
    parent = {}
    max_flow = 0  # initialize max flow
    paths = []  # storing paths contributing to the max flow

    # find augmenting paths while they exist (continue)
    while bfs_capacity_path_list(graph, source, sink, parent):
        flow_path = float('Inf')
        s = sink
        while s != source:
            for neigh, capacity in graph[parent[s]]:
                if neigh == s:
                    flow_path = min(flow_path, capacity)  # minimum capacity in the path
                    break
            s = parent[s]
        
        max_flow += flow_path  # add path flow to overall flow
        paths.append((get_path(parent, source, sink), flow_path))
        
        v = sink
        while v != source:
            u = parent[v]
            for index, (neigh, capacity) in enumerate(graph[u]):
                if neigh == v:
                    graph[u][index] = (neigh, capacity - flow_path)  # update residual capacities
            for index, (neigh, capacity) in enumerate(graph[v]):
                if neigh == u:
                    graph[v][index] = (neigh, capacity + flow_path)  # update reverse flow
            v = parent[v]
    
    return max_flow, paths  # return the maximum flow and paths

# visualize the graph using NetworkX and Matplotlib
def visualize_graph(graph, is_matrix=True, is_second_output=False):
    G = nx.DiGraph()
    if is_matrix:
        for i, row in enumerate(graph):
            for j, capacity in enumerate(row):
                if capacity > 0:
                    G.add_edge(i, j, capacity=capacity)
    else:
        for u in graph:
            for v, capacity in graph[u]:
                if capacity > 0:
                    G.add_edge(u, v, capacity=capacity)

    pos = nx.spring_layout(G)
    node_color = 'lightblue' if not is_second_output else 'lightgreen'
    nx.draw(G, pos, with_labels=True, node_color=node_color, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Network Graph with Capacities")
    plt.show()

# example data Input for Matrix Representation
graph_matrix = [
    [0, 16, 13, 0, 0, 0],
    [0, 0, 10, 12, 0, 0],
    [0, 4, 0, 0, 14, 0],
    [0, 0, 9, 0, 0, 20],
    [0, 0, 0, 7, 0, 4],
    [0, 0, 0, 0, 0, 0]
]

# example data Input for List Representation
graph_list = defaultdict(list)
graph_list[0].extend([(1, 16), (2, 13)])
graph_list[1].extend([(2, 10), (3, 12)])
graph_list[2].extend([(1, 4), (4, 14)])
graph_list[3].extend([(2, 9), (5, 20)])
graph_list[4].extend([(3, 7), (5, 4)])

source = 0
sink = 5

# running and visualize the matrix-based implementation
print("Visualizing the initial graph (Matrix):")
visualize_graph(graph_matrix)
starting_time = time.time()
max_flow_matrix, paths_matrix = ford_fulkerson_matrix(graph_matrix, source, sink)
ending_time = time.time()
print("\nMaximum Flow (Matrix Representation):", max_flow_matrix)
print("Paths Contributing to Maximum Flow:")
for path, flow in paths_matrix:
    print(f"Path: {' -> '.join(map(str, path))}, Flow: {flow}")
print("Execution Time (Matrix):", ending_time - starting_time, "seconds")

# runnign and visualize the list-based implementation with green nodes
print("\nVisualizing the initial graph (List):")
visualize_graph(graph_list, is_matrix=False, is_second_output=True)
starting_time = time.time()
max_flow_list, paths_list = ford_fulkerson_list(graph_list, source, sink)
ending_time = time.time()
print("\nMaximum Flow (List Representation):", max_flow_list)
print("Paths Contributing to Maximum Flow:")
for path, flow in paths_list:
    print(f"Path: {' -> '.join(map(str, path))}, Flow: {flow}")
print("Execution Time (List):", ending_time - starting_time, "seconds")
