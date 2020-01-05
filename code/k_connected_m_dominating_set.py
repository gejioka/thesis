from operator import itemgetter
from graph import *
import networkx as nx
import matplotlib.pyplot as plt
import ast
import re

class node:
    def __init__(self,name,neighbors,number_of_neighbors):
        self.name = name
        self.neighbors = neighbors
        self.number_of_neighbors = number_of_neighbors

    def get_name(self):
        return self.name
    
    def get_neighbors(self):
        return self.neighbors
    
    def get_number_of_neighbors(self):
        return self.number_of_neighbors

list_of_nodes = {}

def plot_graph(G,nodes):
    G = nx.Graph()
    
    edges = []
    for node in nodes:
        for neighbor in node[2]:
            edges.append((node[1],neighbor[0]))
    G.add_edges_from(edges)
    k_components = nx.k_components(G)
    print "The network is {}-connected".format(len(k_components))

    nx.draw(G,with_labels = True)
    plt.show()

def parse_network(links):
    with open("network.txt","r") as f:
        for line in f:
            if line[0] != "#" and len(line) > 1:
                line = line.replace(", ",",")
                item = re.split(' |\t',line)
                item = filter(None,item)
                neighbors = item[2].split(";")
                
                for i in range(len(neighbors)):
                    neighbors[i] = ast.literal_eval(neighbors[i])[0]
                links.append((len(neighbors),item[0],neighbors))
                list_of_nodes[item[0]] = node(item[0],neighbors,len(neighbors))
    return links

def findKMCDS(nodes):
    dominating_set = []

    for node in nodes:
        if len(set(dominating_set) & set(list_of_nodes[node[1]].get_neighbors())) < 2:
            dominating_set.append(node[1])
    print "Dominating Set (DS) is:", dominating_set

links = []
links = parse_network(links)
findKMCDS(links)
plot_graph(G,links)