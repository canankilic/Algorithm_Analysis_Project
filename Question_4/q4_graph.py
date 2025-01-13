# Question 4: Graph Algorithm
# Esmanur Yorulmaz - 210201008
# Canan Kılıç - 220201037

import csv  # to read .csv files
from queue import PriorityQueue  # import priority queue for Dijkstra's algorithm
import networkx as nx  # for graph visualization
import matplotlib.pyplot as plt  # for plotting and visualization

class Graph: # graph class to represent cities and roads

    def __init__(self): # define the graph list
        self.graph_list = {}

    def new_edge_adder(self, origin_city, destination_city, distance): # to add new road to the graph
        if origin_city not in self.graph_list: # check if the city is already in the graph
            self.graph_list[origin_city] = []
        if destination_city not in self.graph_list:
            self.graph_list[destination_city] = []
        self.graph_list[origin_city].append((destination_city, distance)) # add road and distance between origin and destination
        self.graph_list[destination_city].append((origin_city, distance))

    def edge_remover(self, origin_city, destination): # to remove road between two cities
        if origin_city in self.graph_list: # remove destination city from graph
            self.graph_list[origin_city] = [(city_node, distance_between_cities) for city_node, distance_between_cities in self.graph_list[origin_city] if city_node != destination]
        if destination in self.graph_list: # remove origin city from graph
            self.graph_list[destination] = [(city_node, distance_between_cities) for city_node, distance_between_cities in self.graph_list[destination] if city_node != origin_city]

    def read_csv_files(self, dataset): # read csv files for data
        with open(dataset, 'r') as file:
            read_file = csv.DictReader(file)
            for row in read_file:
                origin_city = row['Origin'].lower()
                destination_city = row['Destination'].lower()
                distance = int(row['Distance'])
                self.new_edge_adder(origin_city, destination_city, distance)

    def __str__(self): # show the graph as string
        result = ""
        for city, roads in self.graph_list.items():
            result += f"{city}: {roads}\n"
        return result

def visualize_routes(graph, start_location, shortest_paths, iteration=None): # visualization function

    G_visual = nx.Graph()

    for origin, neighbors in graph.graph_list.items(): # add edges to the graph
        for destination, distance in neighbors:
            if not G_visual.has_edge(origin, destination):
                G_visual.add_edge(origin, destination, weight=distance)

    plt.figure(figsize=(15, 15)) # create the plot for visual
    position_graph = nx.spring_layout(G_visual, seed=42)

    # draw graph visual part for representing the graph
    nx.draw_networkx_nodes(G_visual, position_graph, node_size=1500, node_color="lightblue", alpha=0.6)
    nx.draw_networkx_edges(G_visual, position_graph, width=2, alpha=0.6, edge_color="gray")
    nx.draw_networkx_labels(G_visual, position_graph, font_size=12, font_weight="bold", font_color="black")

    edge_labels = nx.get_edge_attributes(G_visual, "weight") # draw distances
    nx.draw_networkx_edge_labels(G_visual, position_graph, edge_labels=edge_labels, font_size=10, font_color="red")

    for label, (x, y) in position_graph.items():
        position_graph[label] = (x, y + 0.05)  # adjust the vertical position

    plt.title(f"Delivery Routes from {start_location.capitalize()}")
    plt.axis("off")  # Turn off the axis

    # save the graph
    if iteration is None:
        plt.savefig("question4_initial.png")  # initial graph
    else:
        plt.savefig(f"question4_{iteration}.png")  # after each option

def road_selection_dijkstra(graph, start): # Dijkstra's algorithm to find the shortest path
    distances = {city_node: float('inf') for city_node in graph.graph_list}
    distances[start] = 0

    visited_city = set() # set the visited cities to avoid duplication
    p_queue = PriorityQueue()
    p_queue.put((0, start)) # pivoting

    while not p_queue.empty(): # process the cities in the priority queue until it's empty
        current_distance, current_city_node = p_queue.get()

        if current_city_node in visited_city:
            continue

        visited_city.add(current_city_node) # add visited city to current visited city

        for neighbor, graph_weight in graph.graph_list[current_city_node]: # iteratively take all neighbors
            if neighbor not in visited_city: # skip the neighbor if it's been visited
                new_distance = current_distance + graph_weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    p_queue.put((new_distance, neighbor)) # add the neighbor to the priority queue

    return distances

def main():

    graph = Graph()

    graph.read_csv_files('cities.csv') # read the datas

    cities = ", ".join([city.capitalize() for city in graph.graph_list.keys()]) # take input from user
    starting_point = input(f"Enter the start location from these cities: {cities}: ").lower() # prompt user about cities

    if starting_point not in graph.graph_list:
        print("Error: No such city in the list.")
        return

    dijkstra_shortest_paths = road_selection_dijkstra(graph, starting_point) # take the shortest paths
    print("\nShortest delivery routes with Dijkstra’s algorithm:")
    for destination, distance in sorted(dijkstra_shortest_paths.items(), key=lambda x: x[1]):
        if distance == float('inf'): # show deleted road, if any (infinity)
            print(f"{starting_point.capitalize()} -> {destination.capitalize()}: deleted road, please use another destination")
        else:
            print(f"{starting_point.capitalize()} -> {destination.capitalize()}: {distance} units")

    visualize_routes(graph, starting_point, dijkstra_shortest_paths) # row graph before any dynamic performance


    # dynamic updates
    iteration = 1
    while True:
        print("\nIf you want to add any road, press 1")
        print("If you want to delete any road, press 2")
        print("If you want to exit, press 0")
        user_input = input("Enter: ")

        if user_input == '1':  # add road
            destination = input("Enter the destination you want to add a road to: ").lower()

            if destination == starting_point:
                print("This destination area is already in the list, select another area.")
                continue

            if destination in [city_node.lower() for city_node, _ in graph.graph_list[starting_point]]:
                print("This road already exists.")
                continue

            try:
                distance = int(input("Enter the distance: "))
                graph.new_edge_adder(starting_point, destination, distance)
                print(f"Road added between {starting_point.capitalize()} and {destination.capitalize()} with distance {distance}.")
            except ValueError:
                print("Error: Distance must be an integer.")

        elif user_input == '2':  # delete road
            destination = input("Enter the destination you want to delete: ").lower()

            found_road = False
            for city_node in graph.graph_list:
                for neighbor, _ in graph.graph_list[city_node]:
                    if neighbor == destination:
                        found_road = True # if road is in the list remove the road and all other roads it is connected with
                        graph.edge_remover(city_node, destination)
                        print(f"Road removed between {city_node.capitalize()} and {destination.capitalize()}.")
                        break

            if not found_road:
                print(f"There is no road to {destination.capitalize()} in the graph.")

        elif user_input == '0':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

        dijkstra_shortest_paths = road_selection_dijkstra(graph, starting_point) # find shortest path after dynamic operations
        print("\nNew delivery routes (after dynamic programming):")
        for destination, distance in sorted(dijkstra_shortest_paths.items(), key=lambda x: x[1]):
            if distance == float('inf'): # show deleted roads
                print(f"{starting_point.capitalize()} -> {destination.capitalize()}: road closed due to road under construction , please use another destination")
            else:
                print(f"{starting_point.capitalize()} -> {destination.capitalize()}: {distance} units")

        visualize_routes(graph, starting_point, dijkstra_shortest_paths, iteration=iteration) # update the visualize routes
        iteration += 1

if __name__ == "__main__":
    main()
