from global_variables import *
from networkx.algorithms.connectivity import minimum_st_node_cut
from log import *
import networkx as nx
import matplotlib.pyplot as plt

G = None

def initialize_graph():
    """
    Description: Initialize a new graph object

    Args:
        -

    Returns:
        G
    """
    global G
    G = nx.Graph()
    
def add_nodes():
    """
    Description: Add nodes to graph

    Args:
        G (Graph): An object represent this network

    Returns:
        G
    """
    global G
    edges = []
    for name, node in dict_of_objects.iteritems():
        for neighbor in node.get_N_of_u():
            try:
                if neighbor not in G.neighbors(node.get_name()):
                    edges.append((node.get_name(),neighbor))
            except:
                edges.append((node.get_name(),neighbor))
    
    G.add_edges_from(edges)
    
def check_k_connectivity(source,destination):
    """
    Description: Check if network is k-connected

    Args:
        G (Graph):  An object represent this network

    Returns:
        -
    """
    global G
    maximum_disjoint_paths = []
    sorted_paths = []
    all_paths = nx.all_simple_paths(G,source,destination)
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
    write_message(args,"[!] Maximum disjoint paths are: " + str(maximum_disjoint_paths),"INFO")
    write_message(args,"Network is {}-connected.".format(len(maximum_disjoint_paths)),"INFO")
    
    return len(maximum_disjoint_paths)

def find_node_connectivity():
    """
    Description: Find connectivity of network

    Args:
        -
    Returns:
        node_connectivity
    """
    global G

    node_connectivity = nx.node_connectivity(G)
    return node_connectivity

def poll_nodes_for_dominators(dict_of_next_dominators,args):
    """
    Description: All nodes in connected dominating set poll other nodes to join

    Args:
        dict_of_next_nodes (dictionary)

    Returns:
        -
    """
    global G

    counter = 0
    dict_of_significant_nodes = {}
    write_message(args,"[!] Start poll proccess","INFO")
    write_message(args,"[!] Try to add most significant nodes to DS and remove non significant nodes.","INFO")
    for i in range(counter,len(connected_dominating_set)):
        for j in range(counter+1,len(connected_dominating_set)):
            node_obj = dict_of_objects[connected_dominating_set.keys()[i]]
            if connected_dominating_set.keys()[j] not in node_obj.get_N_of_u():
                paths = list(nx.shortest_path(G,connected_dominating_set.keys()[i],connected_dominating_set.keys()[j]))
                message = "Sortest path from {} --> {} is [%s]"%", ".join(paths)
                message = message.format(dict_of_objects[connected_dominating_set.keys()[i]].get_name(),dict_of_objects[connected_dominating_set.keys()[j]].get_name())
                write_message(args,message,"DEBUG")
                for node in paths[1:len(paths)-1]:
                    write_message(args,"[!] Check significance of node with name {}".format(node),"INFO")
                    if node not in dict_of_next_dominators:
                        if node not in connected_dominating_set:
                            write_message(args,"[+] Node with name {} added to list with next dominators".format(node),"INFO")
                            dict_of_next_dominators[node] = 1
                        else:
                            if node not in dict_of_significant_nodes:
                                write_message(args,"[+] Node with name {} added to list with significant nodes".format(node),"INFO")
                                dict_of_significant_nodes[node] = 1
                            else:
                                write_message(args,"[-] Node with name {} already exist in list with significant nodes".format(node),"INFO")
                                dict_of_significant_nodes[node] += 1
                    else:
                        write_message(args,"[-] Node with name {} already exist in list with next dominators".format(node),"INFO")
                        dict_of_next_dominators[node] += 1
                else:
                    break
        counter += 1

    for node in connected_dominating_set:
        if node not in dict_of_significant_nodes:
            dict_of_significant_nodes[node] = 0
    
    return (dict_of_significant_nodes,dict_of_next_dominators) 

def plot_local_graph(network):
    """
    Description: Create and plot local network

    Args:
        network (Graph)

    Returns:
        -
    """
    nx.draw(network,with_labels = True)
    plt.show()

def plot_input_graph():
    """
    Description: Create and plot input network

    Args:
        -

    Returns:
        -
    """
    global G

    nx.draw(G,with_labels = True)
    plt.show()