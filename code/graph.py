from networkx.algorithms.connectivity import minimum_st_node_cut
from global_variables import *
from network_tools import *
from log import *
import random
import operator
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
    #     for edge in G.edges():
    #         _edge_added = False

    #         if args != None:
    #             write_message(args,"[+] Try to add edge in edges...","INFO")
    #         if edge[0] in connected_dominating_set.keys() and edge[1] in connected_dominating_set.keys():
    #             _edge_added = True
    #             edges.append(edge)
    #             if args != None:
    #                 write_message(args,"[+] Edge {}<-->{} added to edges.".format(edge[0],edge[1]),"DEBUG")
    #         else:
    #             if (not all_dominees_have_m_dominators(args.m)) or (not all_dominators_have_k_dominators(args.k)):
    #                 _edge_added = True
    #                 edges.append(edge)
    #                 if args != None:
    #                     write_message(args,"[+] Edge {}<-->{} added to edges.".format(edge[0],edge[1]),"DEBUG")
    #         if not _edge_added:
    #             write_message(args,"[-] Edge {}<-->{} removed from edges.".format(edge[0],edge[1]),"DEBUG")
    # if args != None:
    #     write_message(args,"[+] Add all edges in list to graph.","INFO")
    # G.add_edges_from(edges) if not new else new_G.add_edges_from(edges)
    # if args != None:
    #     write_message(args,"[+] All edges added to graph.","INFO")
        for node in connected_dominating_set:
            for neighbor in dict_of_objects[node].get_N_of_u():
                # if neighbor in connected_dominating_set or not (all_dominees_have_dominators() and all_dominators_have_k_dominators(int(args.k)) and all_dominees_have_m_dominators(int(args.m))):
                edges.append((node,neighbor))
    if args != None:
        write_message(args,"[+] Add all edges in list to graph.","INFO")
    G.add_edges_from(edges) if not new else new_G.add_edges_from(edges)
    if args != None:
        write_message(args,"[+] All edges added to graph.","INFO")
    
    # # TODO: If network is not connected after adding nodes test this case
    if args:
        if all_dominees_have_dominators() and all_dominators_have_k_dominators(int(args.k)) and all_dominees_have_m_dominators(int(args.m)):
            print "Network is connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        else:
            print "Network is not connected!!!!!!!!!!!!!!!!!!!!!"

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

def find_minimum_vertex_cut(new=False,s=None,t=None):
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
        if s != None and t != None:
            return minimum_st_node_cut(new_G,s,t)
        return nx.minimum_node_cut(new_G)
    return None

def _is_k_connected(args):
    """
    Description: Check if network is k-connected

    Args:
        args (obj): An object with all user arguments
    Returns:
        boolean
    """
    return nx.is_k_edge_connected(new_G, k=int(args.k))

def check_dominators_connectivity(args,n,node_type):
    """
    Description: Check if all dominators are k-connected

    Args:
        k (int): An integer with k value
    Returns:
        boolean
    """
    candidate_dominators = {}

    results = None
    if node_type == "dominator":
        results = all_dominators_have_k_dominators(n,return_list=True)
    elif node_type == "dominatee":
        results = all_dominees_have_m_dominators(n,return_list=True)
    else:
        write_message(args,"There is no node type with name {}".format(node_type),"WARNING")
        return -1

    if isinstance(results,list):
        for node in results:
            node_obj = dict_of_objects[node]
            for neighbor in node_obj.get_N_of_u():
                if neighbor not in connected_dominating_set.keys():
                    if neighbor not in candidate_dominators.keys():
                        candidate_dominators[neighbor] = 1
                    else:
                        candidate_dominators[neighbor] += 1
        candidate_dominators = dict(sorted(candidate_dominators.items(), key=operator.itemgetter(1)))
        connected_dominating_set[candidate_dominators.keys()[0]]

def check_constraint5(args):
    """
    Description: Check if constraint 5 is satisfied

    Args:
        args (obj): An object which contains all user arguments
        k (int): An integer with k value
        m (int): An integer with m value
    Returns:
        boolean
    """
    CDS_before = {}
    CDS_after = {}

    if int(args.k) > 0 and int(args.m) > 0:
        while CDS_before != CDS_after:
            CDS_before = connected_dominating_set.copy()

            check_dominators_connectivity(args,int(args.k),"dominator")
            check_dominators_connectivity(args,int(args.m),"dominatee")

            CDS_after = connected_dominating_set.copy()
    else:
        write_message(args,"k and m values must be bigger than zero","ERROR")
        return -1
    

def remain_on_DS(args,vertex_connectivity):
    """
    Description: Decide which nodes will remain in CDS

    Args:
        vertex_connectivity (float): The vertex connectivity of network
    Returns:
        -
    """
    # global new_G

    # K = 0
    # try:
    #     K = len(vertex_connectivity)
    # except Exception:
    #     K = vertex_connectivity

    # temp_dominators = []
    # for i in range(len(connected_dominating_set.keys())):
    #     s = connected_dominating_set.keys()[i]
    #     for j in range(i+1,len(connected_dominating_set.keys())):
    #         t = connected_dominating_set.keys()[j]
    #         if connected_dominating_set.keys()[i] not in dict_of_objects[connected_dominating_set.keys()[j]].get_N_of_u():
    #             vertex_connectivity = find_minimum_vertex_cut(True,s,t)
    #             if len(vertex_connectivity) < K:
    #                 K = len(vertex_connectivity)
    #             else:
    #                 if s not in temp_dominators:
    #                     temp_dominators.append(s)
                
    #             if len(vertex_connectivity) < min(int(args.k),int(args.m)):
    #                 if s not in temp_dominators:
    #                     temp_dominators.append(s)
    #     temp_dominators = []

    # for dominator in temp_dominators:
    #     value = connected_dominating_set.pop(dominator)
    #     for node in dict_of_objects.keys():
    #         node_obj = dict_of_objects[node]
    #         try:
    #             node_obj.add_temp_dominator(dominator)
    #             node_obj.get_dominators().remove(dominator)
    #         except Exception:
    #             pass
        
    #     if all_dominators_have_k_dominators(int(args.k)) and all_dominees_have_m_dominators(int(args.m)):
    #         for node in dict_of_objects.keys():
    #             node_obj = dict_of_objects[node]
    #             node_obj.clear_temp_dominators()
    #     else:
    #         connected_dominating_set[dominator] = value
    #         for node in dict_of_objects.keys():
    #             node_obj = dict_of_objects[node]
    #             if node in node_obj.get_temp_dominators():
    #                 node_obj.get_dominators().append(node)
    #                 node_obj.delete_temp_dominator(node)
    #             node_obj.clear_temp_dominators()

    #         write_message(args,"[!] Node with name {} cannot be removed because CDS will disconnected".format(node),"INFO")
    # return K

    global new_G
    
    write_message(args,"[!] Try to find minimum vertex cut in backbone...","INFO")
    K = vertex_connectivity
    vertex_connectivity = find_minimum_vertex_cut(True)

    write_message(args,"[!] Minimum vertex cut for backbone is: [%s]"%", ".join(list(vertex_connectivity)),"INFO")
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