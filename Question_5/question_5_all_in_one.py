# Question 5: Graph Algorithm
# Esmanur Yorulmaz - 210201008
# Canan Kılıç - 220201037
#output time and space to data size

import time
import matplotlib.pyplot as plt
from collections import deque
from memory_profiler import memory_usage
import networkx as nx

#visualizing using NetworkX

# Breadth-First Search (BFS) for adjacency matrix representation
# finds if there is a path from source to sink with available capacity
def bfs_capacity_path_matrix(graph, source, sink, parent):
    visited = [False] * len(graph)  # track visited nodes
    queue = deque([source])  # start queue with the source node
    visited[source] = True  # put sign source as visited

    while queue:
        node = queue.popleft()  # dequeue (current node)
        for neighbor, capacity in enumerate(graph[node]):  # look all neighbors
            if not visited[neighbor] and capacity > 0:  # if not visited and capacity > 0
                queue.append(neighbor)  # enqueue neighbor
                visited[neighbor] = True  # put sign neighbor as visited
                parent[neighbor] = node  # keep the path
                if neighbor == sink:  # if sink is reached, return True
                    return True
    return False  # No path 

# Ford-Fulkerson algorithm using adjacency matrix
# computes the maximum flow in a graph

def ford_fulkerson_matrix(graph, source, sink):
    parent = [-1] * len(graph)  # initialize an array (store the path)
    max_flow = 0  # initialize maximum flow

    # Augment flow while there is a path from source to sink
    while bfs_capacity_path_matrix(graph, source, sink, parent):
        flow_path = float('Inf')  # start with infinite path flow
        s = sink
        while s != source:  # trace the path + finding minimum capacity
            flow_path = min(flow_path, graph[parent[s]][s])
            s = parent[s]

        max_flow += flow_path  # add path flow to overall flow

        # update residual capacities 
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= flow_path  # reduce forward edge
            graph[v][u] += flow_path  # increase backward edge
            v = parent[v]

    return max_flow

# Breadth-First Search (BFS) for adjacency list representation
# finds if there is a path from source to sink with available capacity
def bfs_capacity_path_list(graph, source, sink, parent):
    visited = {node: False for node in graph}  # track visited nodes
    queue = deque([source])  # initialize queue with the source node
    visited[source] = True  # marking source as visited

    while queue:
        node = queue.popleft()  # dequeue the current node
        for neighbor, capacity in graph[node].items():  # check all neighbors
            if not visited[neighbor] and capacity > 0:  # If not visited and capacity > 0
                queue.append(neighbor)  # enqueue neighbor
                visited[neighbor] = True  # put sign (true) neighbor as visited
                parent[neighbor] = node  # store the path
                if neighbor == sink:  # if sink is reached, return True
                    return True
    return False  # No path 

# Ford-Fulkerson algorithm using adjacency list
# computes the maximum flow in a graph
def ford_fulkerson_list(graph, source, sink):
    parent = {}  # dictionary (store the path)
    max_flow = 0  # initialize maximum flow

    # augment flow while there is a path from source to sink
    while bfs_capacity_path_list(graph, source, sink, parent):
        flow_path = float('Inf')  # start with infinite path flow
        s = sink
        while s != source:  # trace the path and find minimum capacity
            flow_path = min(flow_path, graph[parent[s]][s])
            s = parent[s]

        max_flow += flow_path  # add path flow to overall flow

        # update residual capacities in the graph
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= flow_path  # reduce forward edge
            graph[v][u] = graph.get(v, {}).get(u, 0) + flow_path  # increase backward edge
            v = parent[v]

    return max_flow

# Measure memory usage for the adjacency matrix representation
def measure_memory_matrix(graph, source, sink):
    return ford_fulkerson_matrix(graph, source, sink)  # Run algorithm

# calculate memory usage for the adjacency list representation
def measure_memory_list(graph, source, sink):
    return ford_fulkerson_list(graph, source, sink)  # running algorithm

# run and calculate execution time and memory for adjacency matrix
def run_and_measure_matrix(graph, source, sink):
    starting_time = time.time()  # starting time
    max_flow = ford_fulkerson_matrix(graph, source, sink)  # execute algorithm
    ending_time = time.time()  # ending time
    execution_time = ending_time - starting_time  # end of the execution time (Last e.t)
    mem_usage = memory_usage((measure_memory_matrix, (graph, source, sink)))  # calculate last memory usage
    return execution_time, max(mem_usage)

# run and measure execution time and memory for adjacency list
def run_and_measure_list(graph, source, sink):
    starting_time = time.time()  # starting time
    max_flow = ford_fulkerson_list(graph, source, sink)  # execute algorithm
    ending_time = time.time()  # ending time
    execution_time = ending_time - starting_time  # calculate execution time
    mem_usage = memory_usage((measure_memory_list, (graph, source, sink)))  # calculate last memory usage
    return execution_time, max(mem_usage)

# generate data for matrix and list comparisons
def collect_data():
    sizes = [5, 10, 15, 20, 25, 30]  # different graph sizes 
    times_matrix, memory_matrix = [], []  # for store matrix results
    times_list, memory_list = [], []  # for store list results
    for size in sizes:
        # generate a fully connected graph with constant capacity
        matrix_graph = [[0] * size for _ in range(size)]
        list_graph = {i: {} for i in range(size)}
        for i in range(size):
            for j in range(i + 1, size):
                capacity = 10
                matrix_graph[i][j] = capacity  # add capacity to matrix
                list_graph[i][j] = capacity  # add capacity to list

        # calculate and store results for both representations
        t_matrix, m_matrix = run_and_measure_matrix(matrix_graph, 0, size - 1)
        t_list, m_list = run_and_measure_list(list_graph, 0, size - 1)

        times_matrix.append(t_matrix)
        memory_matrix.append(m_matrix)
        times_list.append(t_list)
        memory_list.append(m_list)

    return sizes, times_matrix, memory_matrix, times_list, memory_list

# Plot graphs for time and memory usage
def plot_graphs(sizes, times_matrix, memory_matrix, times_list, memory_list):
    plt.figure(figsize=(14, 6))  # Create a figure with specific dimensions

    # execution time
    plt.subplot(1, 2, 1)
    plt.plot(sizes, times_matrix, label="Matrix Time", marker='o')
    plt.plot(sizes, times_list, label="List Time", marker='s')
    plt.xlabel("Graph Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Execution Time vs Graph Size")
    plt.legend()

    # memory usage
    plt.subplot(1, 2, 2)
    plt.plot(sizes, memory_matrix, label="Matrix Memory", marker='o', color='red')
    plt.plot(sizes, memory_list, label="List Memory", marker='s', color='orange')
    plt.xlabel("Graph Size")
    plt.ylabel("Memory Usage (MB)")
    plt.title("Memory Usage vs Graph Size")
    plt.legend()

    plt.tight_layout()  
    plt.show()  

def main():
    sizes, times_matrix, memory_matrix, times_list, memory_list = collect_data()  # collect data
    plot_graphs(sizes, times_matrix, memory_matrix, times_list, memory_list)  # plot results draw graph


if __name__ == "__main__":
    main()
