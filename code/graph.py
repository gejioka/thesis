from networkx.algorithms.connectivity import minimum_st_node_cut
from global_variables import *
from network_tools import *
from log import *
import networkx as nx
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
    
def add_nodes(new=False):
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
            if edge[0] in connected_dominating_set.keys() and edge[1] in connected_dominating_set.keys():
                edges.append(edge)
    G.add_edges_from(edges) if not new else new_G.add_edges_from(edges)

def construct_new_graph():
    """
    Description: Construct new graph only with nodes of CDS

    Args:
        -

    Returns:
        -
    """
    global new_G
    
    initialize_graph(True)
    add_nodes(True)

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

# def find_minimum_vertex_cut(s,t,new=False):
#     """
#     Description: Find minimum vertex cut

#     Args:
#         new (bool): A variable to decide which graph to use. Default value <False>
#     Returns:
#         minimum_node_cut
#     """
#     global G
#     global new_G

#     if not new:
#         return minimum_st_node_cut(G,s,t)
#     else:
#         return minimum_st_node_cut(new_G,s,t)

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

def remain_on_DS(args,vertex_connectivity):
    """
    Description: Decide which nodes will remain in CDS

    Args:
        vertex_connectivity (float): The vertex connectivity of network
    Returns:
        -
    """
    global new_G
    plot_input_graph(True)
    to_remove=[]
    vertex_connectivity = find_minimum_vertex_cut(True)
    # print vertex_connectivity
    # print len(vertex_connectivity)
    for node in new_G.edges():
        for node1 in list(vertex_connectivity):
            if node1 in node:
                if node[0] not in to_remove:
                    to_remove.append(node[0])
                if node[1] not in to_remove:
                    to_remove.append(node[1])
    remove_non_significant_nodes(to_remove,args)

    return len(vertex_connectivity)
#     # for node in to_remove:
#     #     new_G.remove_node(node)
#     #     del connected_dominating_set[node]
#     # for node in connected_dominating_set.keys():
#     #     if new_G.degree(node) == 0:
#     #         new_G.remove_node(node)
#     #         del connected_dominating_set[node]
    
#     # for node in list(vertex_connectivity):
#     #     print "Node name is:", node
#     #     del connected_dominating_set[node]
    # for node in connected_dominating_set.keys():
    #     for node1 in list(vertex_connectivity):
    #         if node1 in connected_dominating_set[node]:
    #             del connected_dominating_set[node]

    #del connected_dominating_set[list(vertex_connectivity[])]
    # for s in connected_dominating_set.keys():
    #     s_obj = dict_of_objects[s]
    #     for t in connected_dominating_set.keys():
    #         t_obj = dict_of_objects[t]
    #         if t_obj.get_name() not in s_obj.get_N_of_u():
    #             minimum_st_cut = len(find_minimum_vertex_cut(s,t,True))
    #             print connected_dominating_set
    #             if minimum_st_cut < min(int(args.k),int(args.m)):
    #                 del connected_dominating_set[s]
    #                 break
    #                 # if s > t and (s,t) not in to_remove:
    #                 #     to_remove.append((s,t))
    #                 # else:
    #                 #     if (t,s) not in to_remove:
    #                 #         to_remove.append((t,s))
    #             elif minimum_st_cut < vertex_connectivity:
    #                 vertex_connectivity = minimum_st_cut
    
    # #print "HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE",to_remove
    # return vertex_connectivity

# def remain_on_DS(args,vertex_connectivity):
#     """
#     Description: Decide which nodes will remain in CDS

#     Args:
#         vertex_connectivity (float): The vertex connectivity of network
#     Returns:
#         -
#     """
#     global new_G
#     plot_input_graph(True)
#     to_remove=[]

#     # Assign a very large number to k(G') for first time
#     vertex_connectivity = float("inf")
#     for i in range(len(connected_dominating_set)):
#         #node1_obj = dict_of_objects[connected_dominating_set.keys()[i]]
#         for j in range(i,len(connected_dominating_set)):
#             node2_obj = dict_of_objects[connected_dominating_set.keys()[j]]
#             if connected_dominating_set.keys()[i] != connected_dominating_set.keys()[j] and connected_dominating_set.keys()[i] not in node2_obj.get_N_of_u():
#                 minimum_cut = find_minimum_vertex_cut(connected_dominating_set.keys()[i],connected_dominating_set.keys()[j],True)
#                 if len(minimum_cut) < vertex_connectivity:
#                     if len(minimum_cut) >= int(args.k):
#                         vertex_connectivity = len(minimum_cut)
#                     else:
#                         to_remove.append(connected_dominating_set.keys()[i])
#                 if len(minimum_cut) < min(int(args.k),int(args.m)):
#                     to_remove.append(connected_dominating_set.keys()[i])
#                 # for node in new_G.edges():
#                 #     for node1 in list(vertex_connectivity):
#                 #         if node1 in node:
#                 #             if node[0] not in to_remove:
#                 #                 to_remove.append(node[0])
#                 #             if node[1] not in to_remove:
#                 #                 to_remove.append(node[1])
#                 remove_non_significant_nodes(to_remove,args)

#     return vertex_connectivity

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
        nx.draw(G,with_labels = True)
        plt.show()
    else:
        nx.draw(new_G,with_labels = True)
        plt.show()