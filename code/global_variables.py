NUMBEROFNODES                   = 0     # A variable of number of nodes for this network
NUMBEROFNEIGHBORS               = 0     # A variable of number of neighbors for this network
NUMBEROFLAYERS                  = 0     # A variable of number of layers for this network
NUMBEROFCENTRALNODES            = 0     # A variable of number of central nodes for this network
NUMBEROFCENTRALNODESNEIGHBORS   = 0     # A variable of number of neighbors of central node for this network

SMALL   = 10        # Number of nodes for small network
MEDIUM  = 100       # Number of nodes for medium network
LARGE   = 1000      # Number of nodes for large network
ENORMOUS = 10000    # Number of nodes for enormous network

connected_dominating_set = []   # A list with all node in CDS
list_of_objects = []            # A list with all objects represent nodes
central_nodes = []              # A list of nodes with most neighbors
all_neighbors = []              # A list with all neighbors of all nodes

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

def print_CDS():
    """
    Description: Print Connected Dominating Set(CDS) for this network

    Args:
        -

    Returns:
        -
    """
    to_print = ""
    for node in connected_dominating_set:
        print node