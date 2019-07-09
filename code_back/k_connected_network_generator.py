from global_variables import *
from random import *
from metrics import *
import matplotlib.pyplot as plt
import networkx as nx

def add_nodes(G,nodes):
    """
    Description: Add edges between nodes of graph

    Args:
        G (Graph):          An object for network
        nodes (dictionary): A dictionary with all nodes of network

    Returns:
        G
    """
    edges = []
    for name, neighbors in nodes.iteritems():
        for neighbor in neighbors:
            edges.append((name,neighbor))
    G.add_edges_from(edges)
    
    return G

# User inputs
k = int(raw_input("Give number of connectivity: "))
number_of_nodes = int(raw_input("Give number of nodes: "))
connectivity = int(raw_input("Give connectivity of network:\t1. Low\n\t\t\t\t2. Medium\n\t\t\t\t3. High\n"))

# Set the number of neighbors by given connectivity
number_of_neighbors = 0
if connectivity == 1:
    number_of_neighbors = LOWCONNECTIVITY
elif connectivity == 2:
    number_of_neighbors = MEDIUMCONNECTIVITY
elif connectivity == 3:
    number_of_neighbors = HIGHCONNECTIVITY
else:
    print "There is no option", connectivity
    exit(1)

# Add neighbors of nodes but every node has at least k neighbors
neighbors = {}
for node in range(number_of_nodes):
    for i in range(number_of_neighbors):
        if node not in neighbors:
            neighbors[node] = []
        if len(neighbors[node]) <= k:
            while True:
                neighbor = randint(0, number_of_nodes-1)
                if neighbor not in neighbors[node]:
                    neighbors[node].append(neighbor)
                    break
        else:
            if randint(0,1) == 1:
                neighbor = randint(1, number_of_nodes-1)
                if neighbor not in neighbors[node]:
                    neighbors[node].append(neighbor)

# Create and plot k-connected network
G = nx.Graph()
G = add_nodes(G,neighbors)
nx.draw(G,with_labels = True)
plt.show()