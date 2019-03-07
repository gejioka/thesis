from __future__ import division
import time
import random
from itertools import chain
from global_variables import *

def find_node_degree(nodes,key):
    """
    Description: Find the degree of node

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        key (String): The key of specific node

    Returns:
        Size of internal links of specific node
    """
    return len(nodes[key]["intralinks"])

def different_layers_node_reach(nodes,key):
    """
    Description: Find how many layers specific node reach

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        key (String): The key of specific node

    Returns:
        Size of all different layers which this node reach
    """
    return len(nodes["key"]["interlinks"])

def find_links_between_neighbors(pci_nodes):
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
            if filter(lambda tup: neighbor in tup, pci_nodes):
                if neighbor < node[0] and (neighbor,node[0]) not in list_of_links:
                    list_of_links.append((neighbor,node[0]))
                    unique_links += 1
                elif neighbor > node[0] and (node[0],neighbor) not in list_of_links:
                    list_of_links.append((node[0],neighbor))
                    unique_links += 1
    
    return unique_links

def random_nodes(list_of_nodes,pci_value):
    """
    Description: Return k random nodes of list

    Args:
        list_of_nodes (list): A list with all nodes participate the pci value
        pci_value (int): The value of pci

    Returns:
        List with k random nodes
    """
    return random.sample(list_of_nodes,pci_value)

def single_layer_pci(nodes,node):
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

def create_interlayer_nodes_list(nodes,parent,key,list_of_interlayer_nodes):
    """
    Description: Create a list with all nodes which participate the xPCI

    Args:
        nodes (dictionary): A dictionary with all informations of all nodes
        parent (String): The parent of specific node
        key (String): The key of the specific node
        list_of_interlayer_nodes: A list with all interlayer nodes

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
    
def find_xPCI(nodes,node):
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

def find_mlPCI(nodes,node):
    """
    Description: Find mlPCI for this node

    Args:
        -

    Returns:
        layers, min_nodes
    """
    number_of_layers = 1
    number_of_nodes = 1
    layers_counter = 0
    mlPCI = 0
    while True:
        layers_counter = 0
        for layer in nodes[node]["interlinks"]:
            if len(nodes[node]["interlinks"][layer]) >= number_of_nodes:
                layers_counter += 1
                if layers_counter == number_of_layers:
                    mlPCI = layers_counter
                    break
        if mlPCI < number_of_layers:
            break
        else:
            number_of_layers += 1
            number_of_nodes += 1
    return mlPCI

def find_newPCI(nodes,node,mlPCI):
    """
    Description: Find newPCI metric for this node

    Args:
        nodes (dictionary): A dictionary with all nodes of network
        node (String):      The name of specific node
        k (int):            The number of minimun neighbors has node per layer
        n ()

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