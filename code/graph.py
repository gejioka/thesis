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
    for name, node in dict_of_objects.iteritems():
        for neighbor in node.get_N_of_u():
            try:
                if neighbor not in G.neighbors(node.get_name()):
                    edges.append((node.get_name(),neighbor))
            except:
                edges.append((node.get_name(),neighbor))
    
    G.add_edges_from(edges)
    
    return G

def check_k_connectivity(G):
    """
    Description: Check if network is k-connected

    Args:
        G (Graph):  An object represent this network

    Returns:
        -
    """
    maximum_disjoint_paths = []
    sorted_paths = []
    all_paths = nx.all_simple_paths(G,'v','u')
    list_of_paths = [path for path in all_paths]
    sorted_paths = sorted(list_of_paths,key=len)
    
    for path in sorted_paths:
        if maximum_disjoint_paths == []:
            maximum_disjoint_paths.append(path)
        else:
            is_disjoint_path = True
            for disjoint_paths in maximum_disjoint_paths:
                if len(set(path) & set(disjoint_paths)) > 2:
                    is_disjoint_path = False
            if is_disjoint_path:
                maximum_disjoint_paths.append(path)
    print "Maximum disjoint paths are: ", maximum_disjoint_paths
    print "Network is {}-connected".format(len(maximum_disjoint_paths))

    return len(maximum_disjoint_paths)
                
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
    check_k_connectivity(G)
    nx.draw(G,with_labels = True)
    plt.show()