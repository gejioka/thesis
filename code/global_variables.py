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
list_of_dominatees = []         # A list with all dominaties
central_nodes = []              # A list of nodes with most neighbors
all_neighbors = []              # A list with all neighbors of all nodes
all_pairs = []                  # A list with all pairs of nodes in CDS

# A dictionary with all levels of logging
LEVELS = {  'debug'     : logging.DEBUG,        
            'info'      : logging.INFO,
            'warning'   : logging.WARNING,
            'error'     : logging.ERROR,
            'critical'  : logging.CRITICAL
}

def set_list_of_dominatees(list_of_dom):
    """
    Description: Update list of dominatees

    Args:
        list_of_dom (list): The updated list of dominatees

    Returns:
        -
    """
    global list_of_dominatees

    list_of_dominatees = list_of_dom

def get_list_of_dominatees():
    """
    Description: Return list of dominatees

    Args:
        -

    Returns:
        list_of_dominatees
    """
    global list_of_dominatees

    return list_of_dominatees

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

def print_CDS(args):
    """
    Description: Print Connected Dominating Set(CDS) for this network

    Args:
        -

    Returns:
        -
    """
    import log
    import network_tools as nt

    to_print = ""

    for node, value in connected_dominating_set.iteritems():
        number_of_dominatees = nt.find_number_of_dominatees(dict_of_objects[node])
        log.write_message(args,"Node name is " + node + " and number of dominatees is " + str(number_of_dominatees),"INFO")
    
    backbone = "CDS" if args.cds else ("MCDS" if args.mcds else "RMCDS")
    log.write_message(args,"[!] Number of nodes in {} is: {}".format(backbone,len(connected_dominating_set)),"INFO")