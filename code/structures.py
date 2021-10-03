from global_variables import *
from network_tools import *
from metrics import *
from graph import *
from log import *
import network_parser as np
import time
import ast
import sys
import re

def choose_parser(path:str,args:argparse.ArgumentParser):
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

def create_dict_of_nodes(args:argparse.ArgumentParser):
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
                    item = list(filter(None,item))
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

def create_structures(user_input:int,args:argparse.ArgumentParser):
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
            if args.mcds:
                write_process_message(args,1,True)
            else:
                write_process_message(args,1,False)
            start = time.time()
        links = create_dict_of_nodes(args)
        if args.time:
            end = time.time()
            write_message(args,"Time running process 1: {}".format(end-start),"INFO",True)
            if args.mcds:
                write_process_message(args,2,True)
            else:
                write_process_message(args,2,False)
            start = time.time()
        dict_of_objects = create_objects_of_nodes(links,args)
        
        # Release links
        links = None
        if args.time:
            end = time.time()
            write_message(args,"Time running process 2: {}".format(end-start),"INFO",True)
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

def find_number_of_layers(nodes:list):
    """
    Description: Find the number of all layers in the graph and return it

    Args:
        nodes (int): A list with all the nodes in the graph

    Returns:
        all_layers
    """
    all_layers=[]
    for node in nodes:
        for layer in nodes[node]["interlinks"]:
            if layer not in all_layers:
                all_layers.append(layer)
    return all_layers

def create_objects_of_nodes(nodes:dict,args:argparse.ArgumentParser): 
    """
    Description: Create all objects of nodes for this network

    Args:
        nodes (dictionary): A dictionary with all nodes

    Returns:
        list_of_objecs
    """
    import node
    import log

    all_layers = find_number_of_layers(nodes)
    
    for key in nodes:
        node_obj = node.Node(key)
        node_obj.set_layer(nodes[key]["layer"])
        node_obj.set_intralinks(nodes[key]["intralinks"])
        node_obj.set_interlinks(nodes[key]["interlinks"])
        node_obj.find_N_of_u(nodes[key]["intralinks"],nodes[key]["interlinks"])
        node_obj.find_N2_or_N3_of_u(nodes,2)
        node_obj.set_node_degree(metrics.find_node_degree(nodes,key))
        metrics.decice_pci_algorithm(args,nodes,key,node_obj,len(all_layers))

        # Write log messages
        if args.log:
            log.write_message(args,"[+] A new node with name {} added to network and is in layer {}".format(key,nodes[key]["layer"]),"INFO")
            log.write_message(args,"Node with name {} has {} neighbors in its layer and {} in other layers".format(key,len(nodes[key]["intralinks"])\
                ,len([nodes[key]["interlinks"][a] for a in nodes[key]["interlinks"]])),"DEBUG")
            message = "The number of layers which node has neighbors is {} and are the following [%s]\n"%", ".join(map(str,[str(a) for a in nodes[key]["interlinks"]]))
            message = message.format(len(nodes[key]["interlinks"]))
            log.write_message(args,message,"DEBUG")

        dict_of_objects[node_obj.get_name()] = node_obj

    return dict_of_objects