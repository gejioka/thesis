from networkx.algorithms.connectivity import minimum_st_node_cut
from global_variables import *
from network_tools import *
from log import *
import random
import networkx as nx
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

G = None
new_G = None

def initialize_graph(new=False):
    """
    Description: Initialize a new graph object

    Args:
        -

    Returns:
        G
    """
    global G
    global new_G

    if not new:
        G = nx.Graph()
    else:
        new_G = nx.Graph()

def add_nodes(new=False,args=None):
    """
    Description: Add nodes to graph

    Args:
        G (Graph): An object represent this network

    Returns:
        G
    """
    global G
    global new_G

    edges = []
    if not new:
        for name, node in dict_of_objects.iteritems():
            for neighbor in node.get_N_of_u():
                try:
                    if neighbor not in G.neighbors(node.get_name()):
                        edges.append((node.get_name(),neighbor))
                except:
                    edges.append((node.get_name(),neighbor))
    else:
        for edge in G.edges():
            _edge_added = False

            if args != None:
                write_message(args,"[+] Try to add edge in edges...","INFO")
            if edge[0] in connected_dominating_set.keys() and edge[1] in connected_dominating_set.keys():
                _edge_added = True
                edges.append(edge)
                if args != None:
                    write_message(args,"[+] Edge {}<-->{} added to edges.".format(edge[0],edge[1]),"DEBUG")
            else:
                if (not all_dominees_have_m_dominators(args.m)) or (not all_dominators_have_k_dominators(args.k)):
                    _edge_added = True
                    edges.append(edge)
                    if args != None:
                        write_message(args,"[+] Edge {}<-->{} added to edges.".format(edge[0],edge[1]),"DEBUG")
            if not _edge_added:
                write_message(args,"[-] Edge {}<-->{} removed from edges.".format(edge[0],edge[1]),"DEBUG")
    if args != None:
        write_message(args,"[+] Add all edges in list to graph.","INFO")
    G.add_edges_from(edges) if not new else new_G.add_edges_from(edges)
    if args != None:
        write_message(args,"[+] All edges added to graph.","INFO")

def construct_new_graph(args=None):
    """
    Description: Construct new graph only with nodes of CDS

    Args:
        -

    Returns:
        -
    """
    global new_G
    
    initialize_graph(True)
    add_nodes(True,args)

def remove_node(node):
    """
    Description: Remove node from network

    Args:
        node(string):  Name of node to be removed

    Returns:
        -
    """
    global new_G

    new_G.remove_node(node)

def check_k_connectivity(args,source,destination):
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

def find_node_connectivity(new=False):
    """
    Description: Find connectivity of network

    Args:
        -
    Returns:
        node_connectivity
    """
    global G

    node_connectivity = 0
    if new:
        node_connectivity = nx.node_connectivity(new_G)
    else:
        node_connectivity = nx.node_connectivity(G)
    
    return node_connectivity

def find_minimum_vertex_cut(new=False):
    """
    Description: Find minimum vertex cut

    Args:
        new (bool): A variable to decide which graph to use. Default value <False>
    Returns:
        minimum_node_cut
    """
    global G
    global new_G

    if not new:
        return nx.minimum_node_cut(G)
    else:
        return nx.minimum_node_cut(new_G)

def _is_k_connected(args):
    return nx.is_k_edge_connected(new_G, k=int(args.k))

def remain_on_DS(args,vertex_connectivity):
    """
    Description: Decide which nodes will remain in CDS

    Args:
        vertex_connectivity (float): The vertex connectivity of network
    Returns:
        -
    """
    global new_G
    
    write_message(args,"[!] Try to find minimum vertex cut in backbone...","INFO")
    K = vertex_connectivity
    vertex_connectivity = find_minimum_vertex_cut(True)

    write_message(args,"[!] Minimum vertex cut for backbone is: {}".format(vertex_connectivity),"INFO")
    if len(vertex_connectivity) < K:
        K = len(vertex_connectivity)

    return K

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

def nodes_to_remove(connected_dominating_set,percentage):
    """
    Description: Reutn the number of node to be removed from network

    Args:
        connected_dominating_set(dict): A dictionary with all nodes in backbone
        percentage(int): The percentage of nodes to be removed
    Returns:
        number_of_nodes
    """
    return int(round((len(connected_dominating_set)*percentage)/100.0))


def check_robustness(connected_dominating_set):
    """
    Description: Check the robustness of the backbone

    Args:
        connected_dominating_set(dict): A dictionary with all nodes in backbone
    Returns:
        -
    """
    global G

    number_of_nodes = nodes_to_remove(connected_dominating_set,20)
    for i in range(number_of_nodes):
        connected_dominating_set.pop(random.choice(connected_dominating_set.keys()))
        if all_dominees_have_dominators():
            print "Have removed " + str(i+1) + " nodes"
        else:
            print "Network disconnected"
            break

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

def plot_input_graph(new=False):
    """
    Description: Create and plot input network

    Args:
        -

    Returns:
        -
    """
    global G
    global new_G
    
    if not new:
        try:
            nx.draw(G, with_labels = True)
        except Exception as err:
            print err
    else:
        try:
            nx.draw(new_G,with_labels = True)
        except Exception as err:
            print err
    plt.show()