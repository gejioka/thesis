from metrics import *
from node import *
from global_variables import *
import sys
import ast
import os.path
import re

sys.setrecursionlimit(150000)

def find_intralayer_links(node_layer,neighbors):
    """
    Description: Find all intra-layer links for a specific node

    Args:
        node_layer (int): Layer of the node
        neighbors (list): A list with all neighbors of node

    Returns:
        A list with all intra-layer links
    """
    intralayer_links = []
    
    for neighbor in neighbors:
        if node_layer == neighbor[1]:
            intralayer_links.append(neighbor[0])
    return intralayer_links

def find_interlayer_links(node_layer,neighbors):
    """
    Description: Find all inter-layer links for a specific node

    Args:
        node_layer (int): Layer of the node
        neighbors (list): A list with all neighbors of node

    Returns:
        A list with all inter-layer links
    """
    interlayer_links = {}

    for neighbor in neighbors:
        if node_layer != neighbor[1]:
            if neighbor[1] not in interlayer_links:
                temp_list = []
                temp_list.append(neighbor[0])
                interlayer_links[neighbor[1]] = temp_list
            else:
                interlayer_links[neighbor[1]].append(neighbor[0])
    
    return interlayer_links

def create_dict_of_nodes(path):
    """
    Description: Create a dictionary with all nodes and their links

    Args:
        path (String): Path of .txt file which represent multi-layer network

    Returns:
        A dictionary with status of all nodes
    """
    links = {}
    with open(path,"r") as f:
        for line in f:
            if line[0] != "#" and len(line) > 1:
                item = re.split(' |\t',line)
                item = filter(None,item)
                neighbors = item[2].split(";")
                for i in range(len(neighbors)):
                    neighbors[i] = ast.literal_eval(neighbors[i])
                intralayer_links = find_intralayer_links(int(item[1]),neighbors)
                interlayer_links = find_interlayer_links(int(item[1]),neighbors)

                links[item[0]] = {"intralinks" : intralayer_links, "interlinks" : interlayer_links}
    return links

def create_objects_of_nodes(nodes):
    for node in nodes:
        node_obj = Node(node)
        node_obj.set_intralinks(nodes[node]["intralinks"])
        node_obj.set_interlinks(nodes[node]["interlinks"])
        node_obj.find_N_of_u(nodes[node]["intralinks"],nodes[node]["interlinks"])
        node_obj.find_N2_of_u(nodes)
        result = find_xPCI(nodes,node)
        node_obj.set_xPCI(result[0])
        node_obj.set_xPCI_nodes(result[1])

        list_of_objects.append(node_obj)
    
    return list_of_objects

def check_args(args):
    """
    Description: Check if user's argument is correct

    Args:
        args (list): A list with console arguments

    Returns:
        Terminate program if arguments are not correct
    """
    pci = ""
    if len(args) == 3:
        pci = args[2]   # User set the pci algorithm he wants
    elif len(args) == 2:
        if args[1] == "--help":
            print "Usage of pci argument:"
            print "\tcl:\tRun program with cross-layer PCI (clPCI).\n\t\tThe default algorithm"
            print "\tx:\tRun program with Exhaustive PCI (xPCI)."
            exit(1)
        elif not os.path.isfile(args[1]):
            print "Wrong or inexistent file name. Please give an existing file name"
            exit(1)
        else:
            pci = "cl"
    elif len(args) == 1:
        print "A few arguments. Need at least 2 arguments but you give only " + str(len(args))
        print "Run program like: python <path to program> <path to file> <pci> (optional)"
        print "python <path to program> --help for more details"
        exit(1)
    
    return pci

if __name__=="__main__":
    pci = check_args(sys.argv)
    links = create_dict_of_nodes(sys.argv[1])
    list_of_objects = create_objects_of_nodes(links)
    for node in list_of_objects:
        unique_links = find_links_between_neighbors(node.get_xPCI_nodes())
        node.set_unique_links_between_nodes(unique_links)
        node.find_clPCI()
        node.find_Nu_PCIs(list_of_objects,pci)
        node.find_dominator()
    for node in list_of_objects:
        node.add_node_in_CDS()
    print_CDS()