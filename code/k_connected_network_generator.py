from random import *
import matplotlib.pyplot as plt
import networkx as nx

def add_nodes(G,nodes):
    edges = []
    print nodes
    for name, neighbors in nodes.iteritems():
        for neighbor in neighbors:
            edges.append((name,neighbor))
    G.add_edges_from(edges)
    
    return G

k = int(raw_input("Give number of connectivity: "))
number_of_nodes = int(raw_input("Give number of nodes: "))

neighbors = {}
for node in range(number_of_nodes):
    for i in range(number_of_nodes):
        if node not in neighbors:
            neighbors[node] = []
        else:
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

G = nx.Graph()
G = add_nodes(G,neighbors)
nx.draw(G,with_labels = True)
plt.show()