from global_variables import *
from network_tools import *
from graph import *
from log import *
import network_parser as np
import time
import ast
import sys
import re

def choose_parser(path,args):
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

def create_structures(user_input,args):
    """
    Description: Create a dictionary with all objects of nodes in network

    Args:
        user_input (int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        pci
    """
    pci = args.pci
    parser = choose_parser(args.path,args)

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