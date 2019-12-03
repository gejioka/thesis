from sys import *
import logging
import metrics
import collections

NUMBEROFNODES                   = 0     # A variable of number of nodes for this network
NUMBEROFNEIGHBORS               = 0     # A variable of number of neighbors for this network
NUMBEROFLAYERS                  = 0     # A variable of number of layers for this network
NUMBEROFCENTRALNODES            = 0     # A variable of number of central nodes for this network
NUMBEROFCENTRALNODESNEIGHBORS   = 0     # A variable of number of neighbors of central node for this network

SMALL   = 10        # Number of nodes for small network
MEDIUM  = 100       # Number of nodes for medium network
LARGE   = 1000      # Number of nodes for large network
ENORMOUS = 10000    # Number of nodes for enormous network

LOWCONNECTIVITY     = 3
MEDIUMCONNECTIVITY  = 10
HIGHCONNECTIVITY    = 20 

connected_dominating_set = {}   # A dictionary with all node in CDS
dict_of_objects = {}            # A dictionary with all objects represent nodes
central_nodes = []              # A list of nodes with most neighbors
all_neighbors = []              # A list with all neighbors of all nodes

# A dictionary with all levels of logging
LEVELS = {  'debug'     : logging.DEBUG,        
            'info'      : logging.INFO,
            'warning'   : logging.WARNING,
            'error'     : logging.ERROR,
            'critical'  : logging.CRITICAL
}

def set_number_of_nodes(num_of_nodes):
    """
    Description: Set number of nodes for this network

    Args:
        num_of_nodes (int): Max value of nodes

    Returns:
        -
    """
    global NUMBEROFNODES
    NUMBEROFNODES = num_of_nodes

def set_number_of_neighbors(num_of_neighbors):
    """
    Description: Set number of neighbors for this network

    Args:
        num_of_neighbors (int): Max value of neighbors

    Returns:
        -
    """
    global NUMBEROFNEIGHBORS
    NUMBEROFNEIGHBORS = num_of_neighbors

def set_number_of_layers(num_of_layers):
    """
    Description: Set number of layers for this network

    Args:
        num_of_neighbors (int): Max value of layers

    Returns:
        -
    """
    global NUMBEROFLAYERS
    NUMBEROFLAYERS = num_of_layers

def set_number_of_central_nodes(number_of_central_nodes):
    """
    Description: Set number of central nodes for this network

    Args:
        number_of_central_nodes (int): Max value of central nodes

    Returns:
        -
    """
    global NUMBEROFCENTRALNODES
    NUMBEROFCENTRALNODES = number_of_central_nodes

def set_number_of_neighbors_for_central_nodes(network_type):
    """
    Description: Set number of neighbors for central nodes of this network

    Args:
        network_type (string): The type of network

    Returns:
        -
    """
    global NUMBEROFCENTRALNODESNEIGHBORS

    if network_type == "small":
        NUMBEROFCENTRALNODESNEIGHBORS = SMALL/3
    elif network_type == "medium":
        NUMBEROFCENTRALNODESNEIGHBORS = MEDIUM/2
    elif network_type == "large":
        NUMBEROFCENTRALNODESNEIGHBORS = LARGE/5
    elif network_type == "enormous":
        NUMBEROFCENTRALNODESNEIGHBORS = ENORMOUS/20

def create_objects_of_nodes(nodes,user_input,args):
    """
    Description: Create all objects of nodes for this network

    Args:
        nodes (dictionary): A dictionary with all nodes

    Returns:
        list_of_objecs
    """
    import node
    import log
    
    for key in nodes:
        node_obj = node.Node(key)
        node_obj.set_layer(nodes[key]["layer"])
        node_obj.set_intralinks(nodes[key]["intralinks"])
        node_obj.set_interlinks(nodes[key]["interlinks"])
        node_obj.find_N_of_u(nodes[key]["intralinks"],nodes[key]["interlinks"])

        # Write log messages
        if args.log:
            log.write_message(args,"[+] A new node with name {} added to network and is in layer {}".format(key,nodes[key]["layer"]),"INFO")
            log.write_message(args,"Node with name {} has {} neighbors in its layer and {} in other layers".format(key,len(nodes[key]["intralinks"])\
                ,len([nodes[key]["interlinks"][a] for a in nodes[key]["interlinks"]])),"DEBUG")
            message = "The number of layers which node has neighbors is {} and are the following [%s]\n"%", ".join(map(str,[str(a) for a in nodes[key]["interlinks"]]))
            message = message.format(len(nodes[key]["interlinks"]))
            log.write_message(args,message,"DEBUG")
        if user_input == 1:
            node_obj.find_N2_or_N3_of_u(nodes,2)
            result = metrics.find_xPCI(nodes,key)
            node_obj.set_xPCI(result[0])
            node_obj.set_xPCI_nodes(result[1])
        else:
            node_obj.find_N2_or_N3_of_u(nodes,2)
            localPCI = metrics.single_layer_pci(nodes,key)[0]
            mlPCI = metrics.find_mlPCI(nodes,key)
            newPCI = metrics.find_newPCI(nodes,key,mlPCI)
            node_obj.set_localPCI(localPCI)
            node_obj.set_mlPCI(mlPCI)
            node_obj.set_newPCI(newPCI)

        dict_of_objects[node_obj.get_name()] = node_obj

    return dict_of_objects

def print_CDS(args):
    """
    Description: Print Connected Dominating Set(CDS) for this network

    Args:
        -

    Returns:
        -
    """
    import log

    to_print = ""

    for node, value in connected_dominating_set.iteritems():
        log.write_message(args,"Node name is " + node + " and number of dominees is " + str(value),"INFO")
    log.write_message(args,"[!] Number of nodes in MCDS is: {}".format(len(connected_dominating_set)),"INFO")

