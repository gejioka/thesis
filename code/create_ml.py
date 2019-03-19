from metrics import *
from node import *
from global_variables import *
from graph import *
import network_parser as np
import ml_visualization as mlv
import operator
import time
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
    intralayer_links = [neighbor[0] for neighbor in neighbors if node_layer == neighbor[1]]
    
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
                line = line.replace(", ",",")
                item = re.split(' |\t',line)
                item = filter(None,item)
                neighbors = item[2].split(";")
                for i in range(len(neighbors)):
                    neighbors[i] = ast.literal_eval(neighbors[i])
                intralayer_links = find_intralayer_links(int(item[1]),neighbors)
                interlayer_links = find_interlayer_links(int(item[1]),neighbors)

                links[item[0]] = {"layer" : item[1], "intralinks" : intralayer_links, "interlinks" : interlayer_links}
    return links
    
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

def choose_parser(path):
    """
    Description: Choose parser for specific file

    Args:
        path (String): The path of specific file
    Returns:
        An int represents 1 of 2 parsers
    """
    with open(path,"r") as f:
        for line in f:
            if ";" in line:
                return 1
    return 2

def check_connectivity(node_obj,connectivity_list,current_connected_dominating_set):
    """
    Description: Check if dominating set is connected

    Args:
        node_obj (Node): An object representation of node
        connectivity_list (list): A list with all connected nodes in DS
    Returns:
        connectivity list
    """
    connectivity_list.append(node_obj.get_name())
    for neighbor in node_obj.get_N_of_u():
        if neighbor in current_connected_dominating_set and neighbor not in connectivity_list:
            connectivity_list = check_connectivity(dict_of_objects[neighbor],connectivity_list,current_connected_dominating_set)
    return connectivity_list

def find_MCDS():
    """
    Description: Find Minimum Connected Dominating Set (MCDS) of this network

    Args:
        -
    Returns:
        -
    """
    is_connected = False    # Boolean variable which used to check connectivity of DS
    significant_nodes = []  # A list with all significant nodes of DS
    counter = 0
    while not is_connected:
        temp_connected_dominating_set = {}
        if counter == len(connected_dominating_set.keys()):
            break
        node_to_remove = connected_dominating_set.keys()[counter] # A variable for node to be removed from DS
        value = connected_dominating_set.pop(node_to_remove)
        if len(temp_connected_dominating_set) == 1:
            break
        connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],temp_connected_dominating_set)
        # Check if all dominees have at least one dominator as neighbor
        all_nodes = []
        for key1 in connected_dominating_set:
            all_nodes = all_nodes + dict_of_objects[key1].get_N_of_u()
            if connected_dominating_set[key1] not in all_nodes:
                all_nodes.append(dict_of_objects[key1].get_name())
        final_list = []
        for item in all_nodes: 
            if item not in final_list: 
                final_list.append(item)
        # Check if node belongs to dominating set need to be removed
        if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set) and len(final_list) == len(dict_of_objects):
            pass
        # Add node to list with significant nodes
        else:
            connected_dominating_set[node_to_remove] = value
            counter += 1
            significant_nodes.append(node_to_remove)
            if len(significant_nodes) == len(connected_dominating_set.keys()):
                is_connected = True

def create_structures(user_input):
    """
    Description: Create a dictionary with all objects of nodes in network

    Args:
        user_input (int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        pci
    """
    pci = check_args(sys.argv)
    parser = choose_parser(sys.argv[1])
    
    # Choose parser depends on network file format
    if parser == 1:
        print "\nProcess 1 of 6"
        start = time.time()
        links = create_dict_of_nodes(sys.argv[1])
        end = time.time()
        print "Time running process 1:", end-start
        
        print "\nProcess 2 of 6"
        start = time.time()
        dict_of_objects = create_objects_of_nodes(links,user_input)
        # Release links
        links = None
        end = time.time()
        print "Time running process 2:", end-start
    else:
        np.parser(user_input)
        
    # Create network
    initialize_graph()
    add_nodes()

    return pci

def remove_duplicates(input_list):
    """
    Description: Remove duplicates of input list and return it

    Args:
        input_list (list): Input list

    Returns:
        final_list
    """
    final_list = []
    for item in input_list: 
        if item not in final_list: 
            final_list.append(item) 
    return final_list

def add_next_dominators(list_of_next_dominators):
    """
    Description: Add next dominators to connected dominating set

    Args:
        list_of_next_dominators (list): A list with next dominators

    Returns:
        -
    """
    # Sort list of next dominators by how important are
    sorted_list_of_next_dominators = sorted(list_of_next_dominators.items(), key=operator.itemgetter(1))  
    
    # Add next dominators until DS be connected
    for node in sorted_list_of_next_dominators:
        connected_dominating_set[node[0]] = node[1]
        connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
        if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set) and all_dominees_have_dominators():
            break

def remove_non_significant_nodes(non_significant_nodes):
    """
    Description: Check if can remove dominators that not significants

    Args:
        non_significant_nodes (list): A list with non significant nodes

    Returns:
        -
    """
    for node in non_significant_nodes:
        # Remove node from connected dominating set
        value = connected_dominating_set.pop(node)
        # Check if DS is still connected
        try:
            connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
        except Exception as err:
            pass
        is_connected = False
        if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
            # Check if all dominees have at least one dominator 1-hop away
            all_nodes = []
            for key in connected_dominating_set:
                all_nodes = all_nodes + dict_of_objects[key].get_N_of_u()
            final_list = remove_duplicates(all_nodes)
            # Check if node belongs to dominating set need to be removed
            if len(final_list) != len(dict_of_objects):
                connected_dominating_set[node] = value
            is_connected = True
        if not is_connected:
            connected_dominating_set[node] = value

def all_dominees_have_dominators():
    """
    Description: Check if all dominees have dominator

    Args:
        -

    Returns:
        -
    """
    all_nodes = []
    for node in connected_dominating_set:
        node_obj = dict_of_objects[node]
        all_nodes = all_nodes + node_obj.get_N_of_u()
    final_list = remove_duplicates(all_nodes)
    if len(final_list) == len(dict_of_objects):
        return True
    
    return False

def last_step(algorithm):
    """
    Description: Check if DS is connected, minimize it and plot it

    Args:
        -

    Returns:
        -
    """
    print "\nProcess 4 of 6"
    start = time.time()
    # Check if DS is connected
    connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
    end = time.time()
    print "Time running process 4:", end-start
    is_connected = False
    if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
        print "\nDS is connected\n"
        is_connected = True
    else:
        print "\nDS is not connected\n"
    if algorithm == 2:
        print "\nProcess 5 of 6"
        start = time.time()
        results = poll_nodes_for_dominators({})
        non_significant_nodes = [k for k,v in results[0].iteritems() if int(v) == 0]
        if not is_connected:
            add_next_dominators(results[1])
            remove_non_significant_nodes(non_significant_nodes)
        else:
            add_next_dominators(results[1])
            remove_non_significant_nodes(non_significant_nodes)
        end = time.time()
        print "Time running process 5:", end-start

    # Find Minimum Connected Dominating Set (MCDS)
    print "\nProcess 6 of 6"
    start = time.time()
    find_MCDS()
    end = time.time()
    print "Time running process 6:", end-start

    connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
    if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
        print "\nDS is connected\n"
    else:
        print "\nDS is not connected\n"

    print_CDS()
    mlv.multilayer_visualization()
    
    # Print input graph
    plot_input_graph()

def milcom_algorithm(pci,user_input):
    """
    Description: Create a CDS for this network

    Args:
        pci (String): A variable tell us which PCI algorithm to use
        user_input(int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        -
    """
    print "\nProcess 3 of 6"
    start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        unique_links = find_links_between_neighbors(node.get_xPCI_nodes())
        node.set_unique_links_between_nodes(unique_links)
        node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,pci)
        node.find_dominator(dict_of_objects)
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
    end = time.time()
    print "Time running process 3:", end-start
    
    last_step(1)

def new_algorithm(user_input):
    """
    Description: Create a CDS for this network

    Args:
        user_input(int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        -
    """
    print "\nProcess 3 of 6"
    start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        node.find_weight()
        node.find_Nu_PCIs(dict_of_objects,"new")
        node.add_node_in_CDS(user_input)
    end = time.time()
    print "Time running process 3:", end-start
    print 

    print_CDS()
    mlv.multilayer_visualization()

    last_step(2)

if __name__=="__main__":
    # Get user input and check if this input is correct
    user_input = int(raw_input("Choose one of the following algorithms: 1.milcom algorithm\n\t\t\t\t\t2.new algorithm\n"))
    if user_input not in [1,2]:
        print "Wrong input. Type 1 for milcom or 2 for new algorithm."
        exit(1)

    # Run one of the algorithms
    pci = create_structures(user_input)
    if user_input == 1:
        milcom_algorithm(pci,user_input)
    else:
        new_algorithm(user_input)