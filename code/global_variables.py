import metrics

NUMBEROFNODES       = 0     # A variable of number of nodes for this network
NUMBEROFNEIGHBORS   = 0     # A variable of number of neighbors for this network
NUMBEROFLAYERS      = 0     # A variable of number of layers for this network

SMALL   = 10        # Number of nodes for small network
MEDIUM  = 100       # Number of nodes for medium network
LARGE   = 1000      # Number of nodes for large network
ENORMOUS = 10000    # Number of nodes for enormous network

connected_dominating_set = []   # A list with all node in CDS
list_of_objects = []            # A list with all objects represent nodes

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

def create_objects_of_nodes(nodes):
    import node

    for key in nodes:
        node_obj = node.Node(key)
        node_obj.set_layer(nodes[key]["layer"])
        node_obj.set_intralinks(nodes[key]["intralinks"])
        node_obj.set_interlinks(nodes[key]["interlinks"])
        node_obj.find_N_of_u(nodes[key]["intralinks"],nodes[key]["interlinks"])
        node_obj.find_N2_of_u(nodes)
        result = metrics.find_xPCI(nodes,key)
        node_obj.set_xPCI(result[0])
        node_obj.set_xPCI_nodes(result[1])

        list_of_objects.append(node_obj)
    
    return list_of_objects

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

