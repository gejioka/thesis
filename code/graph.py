from global_variables import *
import networkx as nx
import matplotlib.pyplot as plt

def add_nodes(G):
    """
    Description: Add nodes to graph

    Args:
        G (Graph): An object represent this network

    Returns:
        G
    """
    edges = []
    for node in list_of_objects:
        for neighbor in node.get_N_of_u():
            try:
                if neighbor not in G.neighbors(node.get_name()):
                    edges.append((node.get_name(),neighbor))
            except:
                edges.append((node.get_name(),neighbor))
    
    G.add_edges_from(edges)
    
    return G
    
def create_graph():
    """
    Description: Create and plot final network

    Args:
        -

    Returns:
        -
    """
    G = nx.Graph()
    G = add_nodes(G)
    nx.draw(G,with_labels = True)
    plt.show()