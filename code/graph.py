from networkx.algorithms.connectivity import minimum_st_node_cut
from global_variables import *
from network_tools import *
from log import *
from tqdm import tqdm
import random
import operator
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use('Agg')


G = None
new_G = None

def initialize_graph(new:bool=False):
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

def add_nodes(new:bool=False,args:argparse.ArgumentParser=None):
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
        for name, node in tqdm(dict_of_objects.items()):
            for neighbor in node.get_N_of_u():
                try:
                    if neighbor not in G.neighbors(node.get_name()):
                        edges.append((node.get_name(),neighbor))
                except:
                    edges.append((node.get_name(),neighbor))
    else:
        edges = create_edges(connected_dominating_set)
    
    if args != None:
        write_message(args,"[+] Add all edges in list to graph.","INFO")
    G.add_edges_from(edges) if not new else new_G.add_edges_from(edges)
    if args != None:
        write_message(args,"[+] All edges added to graph.","INFO")
    
def construct_new_graph(edges:list,first_time:int,args:argparse.ArgumentParser=None):
    """
    Description: Construct new graph only with nodes of CDS

    Args:
        -

    Returns:
        -
    """
    global new_G
    

    if first_time:
        initialize_graph(True)
        add_nodes(True,args)
    else:
        new_G.add_edges_from(edges)

def add_node(node:str,new:bool=True):
    """
    Description: Add node to network

    Args:
        node(string):  Name of node to be added

    Returns:
        -
    """
    global new_G
    global G

    edges = []
    if isinstance(node,list):
        edges = create_edges(node)
    else:
        edges = create_edges([node])

    if new:
        new_G.add_edges_from(edges)
    else:
        G.add_edges_from(edges)

def return_subgraph(list_of_nodes:list):
    global G

    return G.subgraph(list_of_nodes)

def remove_node(node:str,new:bool=True):
    """
    Description: Remove node from network

    Args:
        node(string):  Name of node to be removed

    Returns:
        -
    """
    global new_G
    global G

    if new:
        new_G.remove_node(node)
    else:
        G.remove_node(node)

def remove_nodes_from_graph(nodes:list,new:bool=True):
    """
    Description: Remove nodes from graph.

    Args:
        nodes(list): A list with nodes to be removed
        new(boolean): A variable that define which graph is.
    Returns:
        -
    """
    for dominator in nodes:
        if new:
            remove_node(dominator)
        else:
            remove_node(dominator,False)

def check_k_connectivity(args:argparse.ArgumentParser,source:str,destination:str):
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

def find_node_connectivity(new:bool=False):
    """
    Description: Find connectivity of network

    Args:
        -
    Returns:
        node_connectivity
    """
    global new_G
    global G

    node_connectivity = 0
    if new:
        node_connectivity = nx.node_connectivity(new_G)
    else:
        node_connectivity = nx.node_connectivity(G)
    
    return node_connectivity

def find_minimum_vertex_cut(new:bool=False,s:tuple=None,t:tuple=None):
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

def _is_k_connected(args:argparse.ArgumentParser):
    """
    Description: Check if network is k-connected

    Args:
        args (obj): An object with all user arguments
    Returns:
        boolean
    """
    global new_G

    if args == None:
        return nx.is_k_edge_connected(new_G, k=3)
    return nx.is_k_edge_connected(new_G, k=int(args.k))

def check_dominators_connectivity(args:argparse.ArgumentParser,n:int,node_type:str):
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
                if neighbor not in list(connected_dominating_set.keys()):
                    if neighbor not in list(candidate_dominators.keys()):
                        candidate_dominators[neighbor] = 1
                    else:
                        candidate_dominators[neighbor] += 1
        candidate_dominators = dict(sorted(candidate_dominators.items(), key=operator.itemgetter(1)))

        cdominators = []
        for candidate_dominator in list(candidate_dominators.keys()):
            dominator_obj = dict_of_objects[candidate_dominator]
            counter = 0
            for neighbor in dominator_obj.get_N_of_u():
                if neighbor in list(connected_dominating_set.keys()):
                    counter += 1
            
            if counter >= int(args.k):
                connected_dominating_set[candidate_dominator] = 1
                add_dominator_to_all_nodes(candidate_dominator)
                remove_nodes_from_dominatees([candidate_dominator])
                cdominators.append(candidate_dominator)
                
                break
        
        return cdominators

def check_constraint5(args:argparse.ArgumentParser):
    """
    Description: Check if constraint 5 is satisfied

    Args:
        args (obj): An object which contains all user arguments
        k (int): An integer with k value
        m (int): An integer with m value
    Returns:
        boolean
    """
    
    dominators = []
    if int(args.k) > 0 and int(args.m) > 0:
        result = check_dominators_connectivity(args,int(args.k),"dominator")
        if result != None: 
            dominators += result
        
        result = check_dominators_connectivity(args,int(args.m),"dominatee")
        if result != None:
            dominators += result
    else:
        write_message(args,"k and m values must be bigger than zero","ERROR")
        return -1
    
    return dominators

def remain_on_DS(args:argparse.ArgumentParser,vertex_connectivity:float,first_time:bool,new_nodes:list):
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

    nodes_to_remove = []
    if first_time:
        try:
            vertex_connectivity = find_minimum_vertex_cut(True)
        except Exception:
            pass
        for node in new_nodes:
            for dominator in list(connected_dominating_set.keys()):
                if dominator not in dict_of_objects[node].get_N_of_u():
                    vertex_connectivity = find_minimum_vertex_cut(True,node,dominator)
                    
                    message = "[!] Minimum vertex cut {}--->{} is: [%s]"%", ".join(vertex_connectivity)
                    message = message.format(node,dominator)
                    write_message(args,message,"DEBUG")

                if len(vertex_connectivity) < int(args.k):
                    for vertex in vertex_connectivity:
                        if vertex not in nodes_to_remove:
                            nodes_to_remove.append(vertex)

                if len(vertex_connectivity) < K:
                    K = len(vertex_connectivity)
        try:
            remove_dominators_from_all_nodes(vertex_connectivity)
            remove_nodes_from_DS(vertex_connectivity)
            remove_nodes_from_graph(vertex_connectivity)

            write_message(args,"[!] Minimum vertex cut for backbone is: [%s]"%", ".join(list(vertex_connectivity)),"INFO")
            if len(vertex_connectivity) < K:
                K = len(vertex_connectivity)

        except Exception:
            K = 0
    else:
        for node in new_nodes:
            node_obj = dict_of_objects[node]
            if len(node_obj.get_dominators()) >= int(args.k):
                connected_dominating_set[node] = 1
                add_dominator_to_all_nodes(node)
                remove_nodes_from_dominatees([node])

    return K

def poll_nodes_for_dominators(dict_of_next_dominators:dict,args:argparse.ArgumentParser):
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
            node_obj = dict_of_objects[list(connected_dominating_set.keys())[i]]
            if list(connected_dominating_set.keys())[j] not in node_obj.get_N_of_u():
                paths = list(nx.all_shortest_paths(G,list(connected_dominating_set.keys())[i],list(connected_dominating_set.keys())[j]))
                for path in paths:
                    message = "Sortest path from {} --> {} is [%s]"%", ".join(path)
                    message = message.format(dict_of_objects[list(connected_dominating_set.keys())[i]].get_name(),dict_of_objects[list(connected_dominating_set.keys())[j]].get_name())
                    write_message(args,message,"DEBUG")
                    for node in path[1:len(path)-1]:
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

def nodes_to_remove(connected_dominating_set:dict,percentage:int):
    """
    Description: Reutn the number of node to be removed from network

    Args:
        connected_dominating_set(dict): A dictionary with all nodes in backbone
        percentage(int): The percentage of nodes to be removed
    Returns:
        number_of_nodes
    """
    return int(round((len(connected_dominating_set)*percentage)/100.0))


def check_robustness(connected_dominating_set:dict,args:argparse.ArgumentParser):
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
        connected_dominating_set.pop(random.choice(list(connected_dominating_set.keys())))
        if all_dominees_have_dominators():
            write_message(args, "Have removed " + str(i+1) + " nodes", "DEBUG")
        else:
            write_message(args, "Network disconnected", "DEBUG")
            break

def plot_local_graph(network:nx.Graph):
    """
    Description: Create and plot local network

    Args:
        network (Graph)

    Returns:
        -
    """
    nx.draw(network,with_labels = True)
    plt.show()

def plot_input_graph(new:bool=False):
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
            print(err)
    else:
        try:
            nx.draw(new_G, with_labels = True)
        except Exception as err:
            print(err)
    
    plt.plot()