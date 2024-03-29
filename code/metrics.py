from __future__ import division
import time
import random

from networkx.generators.small import dodecahedral_graph
import node
from itertools import chain
from global_variables import *

def find_node_degree(nodes:dict,key:str):
    """
    Description: Find the degree of node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        key (String): The key of specific node

    Returns:
        Size of internal links of specific node
    """
    
    return len(nodes[key]['intralinks'])

def find_total_degree(nodes:dict,key:str):
    """
    Description: Find total degree of node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        key (String): The key of specific node

    Returns:
        Size of total links of specific node
    """
    all_neighbors=[]
    if "interlinks" in list(nodes[key].keys()):
        all_neighbors=nodes[key]["intralinks"]
        for layer in nodes[key]["interlinks"]:
            for neighbor in nodes[key]["interlinks"][layer]:
                if neighbor not in all_neighbors:
                    all_neighbors.append(neighbor)
    else:
        all_neighbors=nodes[key]["intralinks"]

    return len(all_neighbors)

def find_neighbors_per_layer(nodes:dict,node:str,neighbor:str):
    """
    Description: Find the neighbors per layer for input node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The name of specific node

    Returns:
        A dictionary with all neighbors per layer
    """
    neighbors_per_layer = {}
    
    if neighbor in nodes[node]["intralinks"]:
        neighbors_per_layer["intralinks"] = find_node_degree(nodes,neighbor)
    neighbors_per_layer["interlinks"] = {}
    for layer in nodes[neighbor]["interlinks"]:
        neighbors_per_layer["interlinks"][layer] = len(nodes[neighbor]["interlinks"][layer])
    
    return neighbors_per_layer 

def dominators_per_layer(connected_dominating_set:dict):
    """
    Description: Find dominators per layer and add them to list

    Args:
        connected_dominating_set (dictionary): A dictionary with all nodes in CDS
    Returns:
        A list with all dominators per layer
    """
    list_of_layers = []
    number_of_layers = 0
    
    for key in connected_dominating_set:
        if int(dict_of_objects[key].get_layer()) not in list_of_layers:
            list_of_layers.append(int(dict_of_objects[key].get_layer()))
            number_of_layers += 1
    list_of_layers = [0]*number_of_layers
    
    for key in connected_dominating_set:
        list_of_layers[int(dict_of_objects[key].get_layer())-1] += 1

    return list_of_layers
    
def different_layers_node_reach(nodes:dict):
    """
    Description: Find how many layers specific node reach

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
    Returns:
        Size of all different layers which this node reach
    """
    return len(nodes["key"]["interlinks"])

def find_links_between_neighbors(pci_nodes:list):
    """
    Description: Find all links between neighbors which partitiate PCI of specific node

    Args:
        pci_nodes (list): A list with pci of nodes

    Returns:
        The unique links between neighbors participate to PCI of this node
    """
    unique_links = 0    # All unique links between nodes that participate xPCI
    list_of_links = []      # A list with all nodes have links with other nodes
    for node in pci_nodes:
        node_obj = dict_of_objects[node[0]]
        for neighbor in node_obj.get_N_of_u():
            if list(filter(lambda tup: neighbor in tup, pci_nodes)):
                if neighbor < node[0] and (neighbor,node[0]) not in list_of_links:
                    list_of_links.append((neighbor,node[0]))
                    unique_links += 1
                elif neighbor > node[0] and (node[0],neighbor) not in list_of_links:
                    list_of_links.append((node[0],neighbor))
                    unique_links += 1
    return unique_links

def random_nodes(list_of_nodes:list,pci_value:int):
    """
    Description: Return k random nodes of list

    Args:
        list_of_nodes (list): A list with all nodes participate the pci value
        pci_value (int): The value of pci

    Returns:
        List with k random nodes
    """
    return random.sample(list_of_nodes,pci_value)

def decice_pci_algorithm(args:argparse.ArgumentParser,nodes:list,node:dict,node_obj:node.Node,all_layers:int):
    """
    Description: Decide which pci algorithm to use as metric

    Args:
        args  (obj): An object with all user arguments 
        nodes (list): A list with all nodes of network
        node  (dict): A dictionary with node informations
        node_obj(obj): An object with node informations
    Returns:
        List with k random nodes
    """
    if args.pci == "degree":
        node_obj.set_node_degree(find_node_degree(nodes,node))
    elif args.pci == "cl":
        result = find_xPCI(nodes,node)
        node_obj.set_xPCI(result[0])
        node_obj.set_xPCI_nodes(result[1])
    elif args.pci == "x":
        result = find_xPCI(nodes,node)
        node_obj.set_xPCI(result[0])
        node_obj.set_xPCI_nodes(result[1])
    elif args.pci == "new":
        node_obj.set_localPCI(single_layer_pci(nodes,node)[0])
        mlPCI = find_mlPCI(nodes,node)
        node_obj.set_mlPCI(mlPCI)
        node_obj.set_newPCI(find_newPCI(nodes,node,mlPCI))
        node_obj.find_weight()
    elif args.pci == "la":
        node_obj.set_laPCI(find_laPCI(nodes,node)[0])
    elif args.pci == "al":
        node_obj.set_alPCI(find_alPCI(nodes,node,all_layers))
    elif args.pci == "ml":
        node_obj.set_mlPCI(find_mlPCI(nodes,node))
    elif args.pci == "ls":
        node_obj.set_lsPCI(find_lsPCI(nodes,node))
    elif args.pci == "sl":
        node_obj.set_localPCI(single_layer_pci(nodes,node)[0])

def single_layer_pci(nodes:dict,node:str):
    """
    Description: Find pci value for node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The specific node

    Returns:
        pci value
    """
    degrees = []
    pci_value = 0
    number_of_neighbors = 1
    for neighbor in nodes[node]["intralinks"]:
        degree = find_node_degree(nodes,neighbor)
        degrees.append((neighbor,degree))
    
    while True:
        if sum(i[1] >= number_of_neighbors for i in degrees) >= number_of_neighbors:
            degrees = [i for i in degrees if i[1] >= number_of_neighbors]
            number_of_neighbors += 1
        else:
            pci_value = number_of_neighbors - 1
            break

    list_of_nodes = random_nodes(degrees,pci_value)

    return (pci_value,list_of_nodes)

def calculate_total_centrality(node:str):
    """
    Description: Calculate total centrality for a node

    Args:
        node (String): The specific node

    Returns:
        -
    """
    for name,centrality in node.get_centralities_list():
        dict_of_objects[name].increace_centrality(centrality)
            
def create_interlayer_nodes_list(nodes:dict,parent:str,key:str,list_of_interlayer_nodes:list):
    """
    Description: Create a list with all nodes which participate the xPCI

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        parent (String): The parent of specific node
        key (String): The key of the specific node
        list_of_interlayer_nodes(list): A list with all interlayer nodes

    Returns:
        list_of_interlayer_nodes
    """
    if nodes[key]["interlinks"]:
        for k in nodes[key]["interlinks"]:
            for item in nodes[key]["interlinks"][k]:
                if item not in list_of_interlayer_nodes:
                    list_of_interlayer_nodes.append(item)
            for node in nodes[key]["interlinks"][k]:
                if node != parent and node not in list_of_interlayer_nodes:
                    list_of_interlayer_nodes = create_interlayer_nodes_list(nodes,key,node,list_of_interlayer_nodes)
    return list_of_interlayer_nodes
    
def find_xPCI(nodes:dict,node:str):
    """
    Description: Calculate xPCI value for specific node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The specific node

    Returns:
        xPCI value
    """
    xPCI = 0
    xPCI_nodes = []
    list_of_interlayer_nodes = create_interlayer_nodes_list(nodes,None,node,[])
    list_of_interlayer_nodes = []
    for key in nodes[node]["interlinks"]:
        list_of_interlayer_nodes = list(set(list_of_interlayer_nodes) | set(nodes[node]["interlinks"][key]))
    
    if node not in list_of_interlayer_nodes:
        list_of_interlayer_nodes.append(node)

    for i in list_of_interlayer_nodes:
        result = single_layer_pci(nodes,i)
        xPCI = xPCI + result[0]
        xPCI_nodes = xPCI_nodes + result[1]
    
    return (xPCI,xPCI_nodes)

def find_laPCI(nodes:dict,node:str):
    """
    Description: Calculate laPCI value for specific node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The specific node

    Returns:
        laPCI value
    """
    la_degrees = []
    laPCI = 0
    number_of_neighbors = 1
    
    # Add all internal neighbors to list
    for neighbor in nodes[node]["intralinks"]:
        degree = find_total_degree(nodes,neighbor)
        if neighbor not in [i[0] for i in la_degrees]:
            la_degrees.append((neighbor,degree))

    # Add all external neighbors to list
    for layer in nodes[node]["interlinks"]:
        for neighbor in nodes[node]["interlinks"][layer]:
            degree = find_total_degree(nodes,neighbor)
            if neighbor not in [i[0] for i in la_degrees]:
                la_degrees.append((neighbor,degree))

    while True:
        if sum(i[1] >= number_of_neighbors for i in la_degrees) >= number_of_neighbors:
            la_degrees = [i for i in la_degrees if i[1] >= number_of_neighbors]
            number_of_neighbors += 1
        else:
            laPCI = number_of_neighbors - 1
            break
    
    la_degrees.sort(key=lambda tup: tup[1],reverse=True)
    list_of_nodes = la_degrees[:laPCI]
    
    return (laPCI,list_of_nodes)

def create_list_of_neighbors(nodes:dict,node:str):
    """
    Description: Create a list with all neighbors of node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The specific node

    Returns:
        list_of_neighbors
    """ 
    neighbors_per_layer = None
    list_of_neighbors = []
    for neighbor in nodes[node]["intralinks"]:
        neighbors_per_layer = dict(find_neighbors_per_layer(nodes,node,neighbor))
        list_of_neighbors.append(neighbors_per_layer)
    for layer in nodes[node]["interlinks"]:
        for neighbor in nodes[node]["interlinks"][layer]:
            neighbors_per_layer = find_neighbors_per_layer(nodes,node,neighbor)
            list_of_neighbors.append(neighbors_per_layer)
    return list_of_neighbors

def has_atleast_k_neighbors(k:int,list_of_neighbors:list,all_layers:int=None):
    """
    Description: Check if specific node has atleast k_neighbors

    Args:
        k (int): The number of neighbors
        list_of_neighbors (list): A list with all neighbors of this node
        all_layers(int): The number of all layers of network

    Returns:
        boolean
    """
    neighbors=0
    for neighbor in list_of_neighbors:
        if "intralinks" in neighbor:
            if neighbor["intralinks"] >= k and all(i >= k for i in neighbor["interlinks"].values()) and len(neighbor["interlinks"])+1 == all_layers:
                neighbors += 1
        else:
            if all(i >= k for i in neighbor["interlinks"].values()) and len(neighbor["interlinks"]) == all_layers:
                neighbors += 1
    if neighbors >= k:
        return True
    return False

def has_interlinks(interlinks:dict,n:int,k:int,intra_flag:bool):
    """
    Description: Check if specific node has atleast k_neighbors to n layers

    Args:
        intelinks(dict): A dictionary with all interlayer links of node
        k(int): The number of neighbors
        n(int): The number of layers
        intra_flag(boolean): A variable that tells if node has k neighbors to its layer

    Returns:
        boolean
    """
    counter = 0
    for layer in interlinks:
        if interlinks[layer] >= k:
            counter += 1
        if intra_flag:
            if n - counter == 1:
                return True
        else:
            if counter == n:
                return True
    return False

def k_neighbors_to_n_layers(n:int,list_of_neighbors:list):
    """
    Description: Check if has k neighbors with k neighbors each in n layers

    Args:
        n(int): Number of layers
        list_of_neighbors(list): A list with all neighbors of node

    Returns:
        k value
    """
    k = n

    while True:
        neighbors=0
        for neighbor in list_of_neighbors:
            if n == 1:
                if "intralinks" in neighbor:
                    if neighbor["intralinks"] >= k:
                        neighbors += 1
            else:
                if "intralinks" in neighbor:
                    if neighbor["intralinks"] >= k:
                        if neighbor["interlinks"]:
                            if has_interlinks(neighbor["interlinks"],n,k,True):
                                neighbors += 1
                else:
                    if neighbor["interlinks"]:
                        if has_interlinks(neighbor["interlinks"],n,k,False):
                            neighbors += 1
        if neighbors >= k:
            k += 1
        else:
            k -= 1
            break
    
    return k

def find_alPCI(nodes:dict,node:str,all_layers:int):
    """
    Description: Calculate alPCI value for specific node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The specific node
        all_layers(int): The number of layers for this network

    Returns:
        alPCI value
    """
    number_of_nodes = 1
    
    list_of_neighbors = create_list_of_neighbors(nodes,node)
    while True:
        if has_atleast_k_neighbors(number_of_nodes,list_of_neighbors,all_layers):
            number_of_nodes += 1
        else:
            number_of_nodes -= 1
            break
    return number_of_nodes

def find_mlPCI(nodes:dict,node:str):
    """
    Description: Calculate mlPCI value for specific node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The specific node
    
    Returns:
        mlPCI value
    """
    number_of_layers = 1
    mlPCI = []

    list_of_neighbors = create_list_of_neighbors(nodes,node)
    while True:
        k = k_neighbors_to_n_layers(number_of_layers,list_of_neighbors)
        if k >= number_of_layers:
            number_of_layers += 1
            mlPCI.append(k)
        else:
            break
    return sum(mlPCI)

def find_lsPCI(nodes:dict,node:str):
    """
    Description: Calculate mlPCI value for specific node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        node (String): The specific node
    
    Returns:
        mlPCI value
    """
    number_of_layers = 1
    mlPCI = []

    list_of_neighbors = create_list_of_neighbors(nodes,node)
    while True:
        k = k_neighbors_to_n_layers(number_of_layers,list_of_neighbors)
        if k >= number_of_layers:
            number_of_layers += 1
            mlPCI.append(k)
        else:
            break
    return len(mlPCI)

def find_newPCI(nodes:dict,node:str,mlPCI:float):
    """
    Description: Find newPCI metric for this node

    Args:
        nodes (dictionary): A dictionary with all nodes of network
        node (String):      The name of specific node
        mlPCI(float):       The value of metric mlPCI

    Returns:
        layers, min_nodes
    """
    totalPCI = 0
    newPCI = 0
    neighbors = 0
    for layer in nodes[node]["interlinks"]:
        neighbors += len(nodes[node]["interlinks"][layer])
        for neighbor in nodes[node]["interlinks"][layer]:
            totalPCI += single_layer_pci(nodes,neighbor)[0]
    if mlPCI < len(nodes[node]["interlinks"]):
        newPCI = (mlPCI**2/float(neighbors))*totalPCI
    else:
        newPCI = totalPCI

    return newPCI