from metrics import *
from node import *
from global_variables import *
from graph import *
from log import *
import networkx as nx
import network_parser as np
import ml_visualization as mlv
import operator
import argparse
import logging
import time
import sys
import ast
import os
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

def create_dict_of_nodes(args):
    """
    Description: Create a dictionary with all nodes and their links

    Args:
        path (String): Path of .txt file which represent multi-layer network

    Returns:
        A dictionary with status of all nodes
    """
    links = {}
    try:
        with open(args.path,"r") as f:
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
    except IOError as err:
        write_message(args,err,"ERROR")
        sys.exit(1)
    except Exception as err:
        write_message(args,err,"ERROR")

    return links

def choose_parser(path):
    """
    Description: Choose parser for specific file

    Args:
        path (String): The path of specific file
    Returns:
        An int represents 1 of 2 parsers
    """
    try:
        with open(path,"r") as f:
            for line in f:
                if ";" in line:
                    return 1
    except IOError as err:
        write_message(args,err,"ERROR")
        sys.exit(1)
    except Exception as err:
        write_message(args,err,"ERROR")
        sys.exit(1)

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

def find_MCDS(args):
    """
    Description: Minimize existing connected dominating set (CDS)

    Args:
        -
    Returns:
        -
    """
    write_message(args,"[!] CDS created. Need to minimize CDS and create MCDS", "INFO")
    write_message(args,"[!] Start to minimize CDS","INFO")
    
    counter = 0
    while counter < len(connected_dominating_set) and len(connected_dominating_set) > 1:
        # Remove dominator from DS to find out if it needs
        key = list(connected_dominating_set.iteritems())[counter][0]
        value = connected_dominating_set.pop(key)
        write_message(args,"[-] Try to remove node with name {}".format(key),"INFO")

        # Check if every dominatee has dominator
        all_nodes = []
        for key1 in connected_dominating_set:
            all_nodes = all_nodes + dict_of_objects[key1].get_N_of_u()
            if key1 not in all_nodes:
                all_nodes.append(key1)
        
        # Check if DS is connected without dominator
        connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
        all_nodes = dict_of_objects[list(connected_dominating_set.keys())[0]].remove_duplicate(all_nodes)
        if not len(set(connectivity_list)&set(connected_dominating_set)) == len(connected_dominating_set) or not len(set(all_nodes)&set(dict_of_objects)) == len(dict_of_objects):
            connected_dominating_set[key] = value
            write_message(args,"[!] Node with name {} cannot be removed because CDS will disconnected".format(key),"INFO")
            counter += 1
        else:
            write_message(args,"[-] Node with name {} removed from CDS","INFO")
            message = "New CDS with out node {} is [%s]"%", ".join([a for a in connected_dominating_set])
            message = message.format(key)
            write_message(args,message,"DEBUG")
        
def create_structures(user_input,args):
    """
    Description: Create a dictionary with all objects of nodes in network

    Args:
        user_input (int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        pci
    """
    pci = args.pci
    parser = choose_parser(args.path)

    # Choose parser depends on network file format
    if parser == 1:
        if args.time:
            print "\nProcess 1 of 6"
            start = time.time()
        links = create_dict_of_nodes(args)
        if args.time:
            end = time.time()
            print "Time running process 1:", end-start
        
            print "\nProcess 2 of 6"
            start = time.time()
        dict_of_objects = create_objects_of_nodes(links,user_input,args)
        # Release links
        links = None
        if args.time:
            end = time.time()
            print "Time running process 2:", end-start
    else:
        try:
            np.parser(user_input,args)
        except IOError as err:
            write_message(args,err,"ERROR")
            sys.exit(1)
        except Exception as err:
            write_message(args,err,"ERROR")
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
        write_message(args,"[+] Add to DS node with name {}".format(node[0]),"INFO")
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
        write_message(args,"[-] Try to remove node with name {} from CDS".format(node),"INFO")
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
            write_message(args,"[!] Node with name {} cannot be removed because network disconnected!".format(node), "INFO")
        else:
            write_message(args,"[-] Node with name {} removed from CDS".format(node),"INFO")


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

def last_step(algorithm,args):
    """
    Description: Check if DS is connected, minimize it and plot it

    Args:
        -

    Returns:
        -
    """
    if args.time:
        print "\nProcess 4 of 6"
        start = time.time()
    # Check if DS is connected
    connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
    if args.time:
        end = time.time()
        print "Time running process 4:", end-start
    is_connected = False
    if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
        print "\nDS is connected\n"
        is_connected = True
    else:
        print "\nDS is not connected\n"
    if algorithm == 2:
        if args.time:
            print "\nProcess 5 of 6"
            start = time.time()
        results = poll_nodes_for_dominators({},args)
        non_significant_nodes = [k for k,v in results[0].iteritems() if int(v) == 0]
        write_message(args,"[+] Create list with non significant nodes","INFO")
        write_message(args,"List of non significant list created. Nodes induced to list are [%s]"%", ".join(non_significant_nodes),"DEBUG")
        if not is_connected:
            add_next_dominators(results[1])
            remove_non_significant_nodes(non_significant_nodes)
        else:
            add_next_dominators(results[1])
            remove_non_significant_nodes(non_significant_nodes)
        if args.time:
            end = time.time()
            print "Time running process 5:", end-start

    # Find Minimum Connected Dominating Set (MCDS)
    if args.mcds:
        if args.time:
            print "\nProcess 6 of 6"
            start = time.time()
        find_MCDS(args)
        if args.time:
            end = time.time()
            print "Time running process 6:", end-start

        connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
        if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
            print "\nDS is connected\n"
        else:
            print "\nDS is not connected\n"

    testing = False
    try:
        if args.testing:
            testing = True
    except Exception:
        pass
    
    if not testing:
        print_CDS(args)
        if args.plotting:
            mlv.multilayer_visualization()
    
    all_dominees_have_dominators()

    # Print input graph
    if not testing:
        if args.plotting:
            plot_input_graph()

def milcom_algorithm(pci,user_input,args):
    """
    Description: Create a CDS for this network

    Args:
        pci (String): A variable tell us which PCI algorithm to use
        user_input(int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        -
    """
    import log 

    if args.log:
        write_message(args,"[!] Start running milcom algorithm","INFO")
        write_message(args,"[!] Start to calculate cross-layer PCI for all nodes","INFO")
    if args.time:
        print "\nProcess 3 of 6"
        start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        # if args.log:
        #     log.write_message()
        unique_links = find_links_between_neighbors(node.get_xPCI_nodes())
        node.set_unique_links_between_nodes(unique_links)
        node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,pci)
        node.find_dominator(dict_of_objects)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_node_dominators()])
        message = message.format(node.get_name(),len(node.get_node_dominators()))
        write_message(args,message,"DEBUG")
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
    if args.time:
        end = time.time()
        print "Time running process 3:", end-start

    testing = False
    try:
        if args.testing:
            testing = True
    except Exception:
        pass
    
    if not testing:
        print_CDS(args)
        if args.plotting:
            mlv.multilayer_visualization()
    
    last_step(1,args)

def new_algorithm(user_input,args):
    """
    Description: Create a CDS for this network

    Args:
        user_input(int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        -
    """
    if args.time:
        print "\nProcess 3 of 6"
        start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        node.find_weight()
        node.find_Nu_PCIs(dict_of_objects,"new")
        node.find_dominator(dict_of_objects)
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_node_dominators()])
        message = message.format(node.get_name(),len(node.get_node_dominators()))
        write_message(args,message,"DEBUG")
    if args.time:
        end = time.time()
        print "Time running process 3:", end-start
        print 

    testing = False
    try:
        if args.testing:
            testing = True
    except Exception:
        pass
    
    if not testing:
        print_CDS(args)
        if args.plotting:
            mlv.multilayer_visualization()

    last_step(2,args)

def testing_function(args):
    _50_nodes_total         = "/home/giorgos/Documents/University/git_projects/thesis/code/root/50_nodes_total/"
    _degree_experiments     = "/home/giorgos/Documents/University/git_projects/thesis/code/root/degree_experiments/"
    _diameter_experiments   = "/home/giorgos/Documents/University/git_projects/thesis/code/root/diameter_experiments/"
    _layer_experiments      = "/home/giorgos/Documents/University/git_projects/thesis/code/root/layer_experiments/"

    # This code is for testing the two algorithms
    result = re.split('_DM|_D',args.path)[1].split("_")[0]
    if not result.isdigit():
        result = re.split('_DM|_D',args.path)[2].split("_")[0]
    
    string_to_write = ""
    if "50 nodes total" in args.path:
        if os.path.isfile(_50_nodes_total+"_"+str(result)+"_degree.txt"):
            try:
                with open(_50_nodes_total+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_50_nodes_total+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
    elif "Layers Experiments" in args.path:
        if os.path.isfile(_layer_experiments+"_"+str(result)+"_degree.txt"):
            try:
                with open(_layer_experiments+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_layer_experiments+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
    elif "Degree Experiments" in args.path:
        if os.path.isfile(_degree_experiments+"_"+str(result)+"_degree.txt"):
            try:
                with open(_degree_experiments+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_degree_experiments+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
    elif "Diameter Experiments" in args.path:
        if os.path.isfile(_diameter_experiments+"_"+str(result)+"_degree.txt"):
            try:
                with open(_diameter_experiments+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_diameter_experiments+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)

def check_arguments(parser,args):
    """
    Description: Check if all arguments exist and are correct

    Args:
        parser(object): An object which parse arguments
        args: A variable with all arguments of user     
    Returns:
        -
    """
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not args.path:
        parser.error("Need to add an input network")
        sys.exit(1)
    else:
        if not os.path.isfile(args.path):
            parser.error("Invalid input network. This file doesn't exist")
            sys.exit(1)
    if not args.algorithm:
        parser.error("Need to add an input algorithm")
        sys.exit(1)
    else:
        if not (args.algorithm == "1" or args.algorithm == "2"):
            parser.error("Invalid input algorithm. This algorithm doesn't exist")
            sys.exit(1)
    if args.pci not in ["cl","x"]:
        parser.error("Invalid PCI. This PCI code doesn't exist")
        sys.exit(1)
    if args.log:
        if args.logLevel.upper() not in [a.upper() for a in LEVELS.keys()]:
            parser.error("There in no log level {}. The list with all log levels is {}".format(args.logLevel.upper(),[name.upper() for name,obj in LEVELS.iteritems()]))
            sys.exit(1)
    else:
        if args.logLevel:
            parser.error("Cannot pass level argument without enable logging.")
            sys.exit(1)

def get_args():
    """
    Description: Create a parser and parse all arguments program needs to run

    Args:
        -
    Returns:
        args
    """
    # Create argument parser
    parser = argparse.ArgumentParser(description="Robust MCDS for multi-layer Ad hoc Networks")
    parser.add_argument("-fp", "--path", help="Path where network has stored", \
        action="store", dest="path", default=False)
    parser.add_argument("-p", "--pci", help="Algorithm which will use program to calculate PCI value",\
         nargs="?", const="cl", type=str, dest="pci", default="cl")
    parser.add_argument("-a", "--algorithm", help="Which algorithm will use program to calculate robust MCDS", \
        action="store", dest="algorithm", default=False)
    parser.add_argument("--cds", help="Create a connected dominating set for backbone in network", \
        action="store_true", dest="cds", default=False)
    parser.add_argument("--mcds", help="Create a minimum connected dominating set for backbone in network", \
        action="store_true", dest="mcds", default=False)
    parser.add_argument("--rmcds", help="Create a robust minimum connected dominating set for backbone in network", \
        action="store_true", dest="rmcds", default=False)
    parser.add_argument("--testing", help="Test which algorithm is better for each case", \
        action="store_true", dest="testing", default=False)
    parser.add_argument("--plotting", help="Needs or not to plot network", \
        action="store_true", dest="plotting", default=False)
    parser.add_argument("--clock", help="Track algorithm duration", \
        action="store_true", dest="time", default=False)
    parser.add_argument("--log", help="Check if need to add log messages", \
        action="store_true", dest="log", default=False)
    parser.add_argument("-lv", "--level", help="An argument for log level", \
        action="store", dest="logLevel", default=False)
    args = parser.parse_args()
    
    check_arguments(parser,args)

    return args

if __name__=="__main__":
    args = get_args()

    testing = False
    try:
        if args.testing:
            testing = True
    except Exception:
        pass
    
    if args.log:
        configure_logging(args)
    
    if args.log:
        # Create two format strings 
        alg = "milcom" if args.algorithm == 1 else "new"
        backbone = "CDS" if args.cds else ("MCDS" if args.mcds else "RMCDS")    
        
        # Write message
        write_message(args,"[!] Start running {} algorithm to create {} as backbone and path for input file is {}\n".format(alg,backbone,args.path),"INFO")

    # Get user input and check if this input is correct
    user_input = int(args.algorithm)
    if user_input not in [1,2]:
        write_message(args,"Wrong input. Type 1 for milcom or 2 for new algorithm.","ERROR")
        sys.exit(1)

    pci = create_structures(user_input,args)
    if user_input == 1:
        milcom_algorithm(pci,user_input,args)
    else:
        new_algorithm(user_input,args)

    # Write results to file
    if testing:
        testing_function(args)