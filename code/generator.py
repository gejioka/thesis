from __future__ import division
from random import randint
from sys import *
import random
import time
import global_variables as gv

def generate_layers_of_nodes():
    """
    Description: Generate tuples of nodes and the layers they beyong

    Args:
        -

    Returns:
        nodes and their layers list
    """
    nodes_layers_list = []
    for node in range(gv.NUMBEROFNODES):
        nodes_layers_list.append(((str(node),randint(1,gv.NUMBEROFLAYERS)),[]))
    nodes_layers_list.sort(key=lambda tup: tup[1],reverse=False)
    
    return nodes_layers_list

def add_neighbor_to_node(node:tuple,neighbor:tuple):
    """
    Description: Add a new node as neighbor of this node

    Args:
        node (tuple): A variable for specific node
        neighbor (tuple): A variable for specific neighbor of node

    Returns:
        nodes_layer_list
    """
    for i in range(len(nodes_layers_list)):
        if nodes_layers_list[i][0] == node and node[0] in neighbor[1]:
            nodes_layers_list[i][1].append(neighbor[0])
            break
    
    return nodes_layers_list

def generate_neighbors(nodes_layers_list:list,node:tuple,first_time:bool):
    """
    Description: Generate neighbors of the specific node

    Args:
        nodes_layers_list (list): A list with all nodes and their layers

    Returns:
        A list with all neighbors of this node
    """
    is_central = bool(random.getrandbits(1))
    
    if is_central and gv.NUMBEROFCENTRALNODES > 0:
        num_of_neighbors = gv.NUMBEROFCENTRALNODESNEIGHBORS
        gv.central_nodes.append(node)
        gv.NUMBEROFCENTRALNODES -= 1
    else:
        num_of_neighbors = randint(1,gv.NUMBEROFNEIGHBORS)

    [node[1].append(nodes_layers_list[i][0]) for i in range(len(nodes_layers_list)) if node[0] in nodes_layers_list[i][1] and nodes_layers_list[i][0] not in node[1]]
    num_of_neighbors -= len(node[1])
    
    for i in range(len(nodes_layers_list)):
        if nodes_layers_list[i][0] == node[0]:
            nodes_layers_list[i] = node
            break

    if first_time:    
        i = 0
        while i < num_of_neighbors:
            neighbor = random.choice(nodes_layers_list)
            if neighbor[0] != node[0]:
                for j in range(len(nodes_layers_list)):
                    if nodes_layers_list[j][0] == node[0] and neighbor[0] not in node[1]:
                        nodes_layers_list[j][1].append(neighbor[0])
                        nodes_layers_list = add_neighbor_to_node(neighbor,node)
                        i += 1
                        break
    
    return nodes_layers_list

def create_str(node:str,layer:int,neighbors:list):
    """
    Description: Create a string representation of the node it's layer and neighbors

    Args:
        node (String): The name of this node
        layer (int): The layer which this node belong
        neighbors (list): A list with all neighbors of this node

    Returns:
        A string representation of object
    """
    string_to_write = node + "\t" + str(layer) + "\t"
    for neighbor in neighbors:
        string_to_write += str(neighbor).replace(" ","") + ";"
    if string_to_write[len(string_to_write)-1] == ';':
        string_to_write = string_to_write[:-1]
    
    return string_to_write

def check_arguments(args:list):
    if len(args) > 2:
        print("Takes maximum 2 arguments. (3 given)")
        print("Run program like: python <path to program> <network size>")
        print("python <path to program> --help for more details")
        exit(1)
    elif len(args) == 2:
        if args[1] == "--help":
            print("Usage of program:")
            print("\tsmall:\t\tCreate a network with 10 nodes, maximum 5 neighbors and 1 layer")
            print("\tmedium:\t\tCreate a network with 100 nodes, maximum 50 neighbors and 10 layers (default)")
            print("\tlarge:\t\tCreate a network with 1000 nodes, maximum 500 neighbors and 100 layers")
            print("\tenormous:\tCreate a network with 10000 nodes, maximum 5000 neighbors and 1000 layers")
        elif args[1] == "small":
            gv.set_number_of_nodes(gv.SMALL)
            gv.set_number_of_neighbors(6)
            gv.set_number_of_layers(1)
        elif args[1] == "medium":
            gv.set_number_of_nodes(gv.MEDIUM)
            gv.set_number_of_neighbors(int(gv.MEDIUM/2))
            gv.set_number_of_layers(int(gv.MEDIUM/10))
        elif args[1] == "large":
            gv.set_number_of_nodes(gv.LARGE)
            gv.set_number_of_neighbors(int(gv.LARGE/2))
            gv.set_number_of_layers(int(gv.LARGE/10))
        elif args[1] == "enormous":
            gv.set_number_of_nodes(gv.ENORMOUS)
            gv.set_number_of_neighbors(int(10))
            gv.set_number_of_layers(int(20))
    elif len(args) == 1:
        gv.set_number_of_nodes(gv.MEDIUM)
        gv.set_number_of_neighbors(int(gv.MEDIUM/2))
        gv.set_number_of_layers(int(gv.MEDIUM/10))

if __name__=="__main__":
    check_arguments(argv)

    if(len(argv) > 1):
        if(argv[1] == "--help"):
            exit(1)

    nodes_layers_list = generate_layers_of_nodes()

    type_of_network = ""
    if len(argv) > 1:
        type_of_network = argv[1]
    else:
        type_of_network = "medium"

    with open("dynamic_" + type_of_network + "_network.txt","w+") as f:
        stdout.write("Start writing network.")
        stdout.flush()
        time.sleep(1)
        stdout.write(".")
        stdout.flush()
        time.sleep(1)
        stdout.write(".")
        stdout.flush()
        time.sleep(1)
        f.truncate(0)
        for node in nodes_layers_list:
            nodes_layers_list = generate_neighbors(nodes_layers_list,node,True)
        
        for node in nodes_layers_list:
            nodes_layers_list = generate_neighbors(nodes_layers_list,node,False)

        for node in nodes_layers_list:
            string_to_write = create_str(node[0][0],node[0][1],node[1])
            f.write(string_to_write)
            f.write("\n")
        print("\nA new network created!")