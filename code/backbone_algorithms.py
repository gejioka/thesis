from tqdm import tqdm
from network_tools import *
from metrics import *
from graph import *
import ml_visualization as mlv
import time
import sys

### Global variables ###
MAX_SEQUENSE = 3
ERROR_CODE = -1
threshold = 20

def last_step(algorithm:str,args:argparse.ArgumentParser):
    """
    Description: Check if DS is connected, minimize it and plot it

    Args:
        -

    Returns:
        -
    """
    
    # Check if DS is connected
    if args.algorithm == "1" or args.algorithm == "2":
        if args.time:
            if args.mcds:
                write_process_message(args,4,True)
            else:
                write_process_message(args,4,False)
            start = time.time()
        try:
            connectivity_list = check_connectivity(dict_of_objects[list(connected_dominating_set.keys())[0]],[],connected_dominating_set)
            if args.time:
                end = time.time()
                write_message(args,"Time running process 4: {}".format(end-start),"INFO",True)
            is_connected = False
            if len(set(connectivity_list) & set(list(dict_of_objects.keys()))) == len(connected_dominating_set):
                write_message(args,"Dominating set (DS) is connected.","INFO")
                is_connected = True
            else:
                write_message(args,"Dominating set (DS) is not connected.","INFO")

            if algorithm == 2:
                if args.time:
                    if args.mcds:
                        write_process_message(args,5,True)
                    else:
                        write_process_message(args,5,False)
                    start = time.time()
                results = poll_nodes_for_dominators({},args)
                non_significant_nodes = [k for k,v in results[0].items() if int(v) == 0]
                write_message(args,"[+] Create list with non significant nodes","INFO")
                write_message(args,"List of non significant list created. Nodes induced to list are [%s]"%", ".join(non_significant_nodes),"DEBUG")
                if not is_connected:
                    add_next_dominators(results[1],args)
                    remove_non_significant_nodes(non_significant_nodes,args)
                else:
                    add_next_dominators(results[1],args)
                    remove_non_significant_nodes(non_significant_nodes,args)
                if args.time:
                    end = time.time()
                    write_message(args,"Time running process 5: {}".format(end-start),"INFO",True)
        except Exception as err:
            print(err)
            
    # Find Minimum Connected Dominating Set (MCDS)
    if args.mcds:
        if args.time:
            if args.algorithm == "1":
                if args.mcds:
                    write_process_message(args,5,True)
                else:
                    write_process_message(args,5,False)
            elif args.algorithm == "2":
                if args.mcds:
                    write_process_message(args,6,True)
                else:
                    write_process_message(args,6,False)
            else:
                if args.mcds:
                    write_process_message(args,4,True)
                else:
                    write_process_message(args,4,False)
            start = time.time()
        find_MCDS(args)
        if args.time:
            end = time.time()
            if args.algorithm == "1":
                write_message(args,"Time running process 5: {}".format(end-start),"INFO",True)
            elif args.algorithm == "2":
                write_message(args,"Time running process 6: {}".format(end-start),"INFO",True)
            else:
                write_message(args,"Time running process 4: {}".format(end-start),"INFO",True)
    
    if args.algorithm == "1" or args.algorithm == "2":
        try:
            connectivity_list = check_connectivity(dict_of_objects[list(connected_dominating_set.keys())[0]],[],connected_dominating_set)
            if len(set(connectivity_list) & set(list(dict_of_objects.keys()))) == len(connected_dominating_set):
                write_message(args,"Dominating set (DS) is connected.","INFO")
            else:
                write_message(args,"Dominating set (DS) is not connected.","INFO")
        except Exception as err:
            print(err)

    plotting(args,True)
    all_dominees_have_dominators()

def plotting(args:argparse.ArgumentParser,input_graph:bool=False):
    """
    Description: Plot network

    Args:
        args (obj): An object with all arguments of user
    Returns:
        -
    """
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
    
    if input_graph:
        # Print input graph
        if not testing:
            if args.plotting:
                plot_input_graph()

def preprocess(dict_of_objects:dict,algorithm:str,args:argparse.ArgumentParser):
    """
    Description: Preprocess phase 

    Args:
        dict_of_objects (dict): A dictionary with all objects of nodes
        algorithm (string): The name of the input algorithm
        args (obj): An object with all arguments of user
    Returns:
        start
    """
    names = {"1": "milcom",
             "2": "new",
             "3": "robust"}

    # Write log messages
    start = 0
    if args.log:
        write_message(args,"[!] Start running {} algorithm".format(names[algorithm]),"INFO")
    if args.time:
        if args.mcds:
            write_process_message(args,3,True)
        else:
            write_process_message(args,3,False)
        start = time.time()

    if algorithm == "3":
        set_list_of_dominatees([(i,0.0,0.0) for i in list(dict_of_objects.keys())])

    write_message(args,"Create object for each node...","INFO")
    for name, node in tqdm(dict_of_objects.items()):
        if args.pci == "cl":
            node.set_unique_links_between_nodes(find_links_between_neighbors(node.get_xPCI_nodes()))
            node.find_clPCI()
        if args.centrality:
            node.find_betweeness_centrality(dict_of_objects)
    
    write_message(args,"Calculate total centrality for each node...","INFO")
    if args.centrality:
        for name, node in tqdm(dict_of_objects.items()):
            calculate_total_centrality(node)

    write_message(args,"Find PCI metrics for every node...","INFO")
    for name, node in tqdm(dict_of_objects.items()):
        node.find_Nu_PCIs(dict_of_objects,args.pci,args)

    write_message(args,"Find dominator for each node...","INFO")
    for name, node in tqdm(dict_of_objects.items()):
        node.find_dominator(dict_of_objects,args)

    if algorithm == "3":
        # Every node decides whether it is dominator or dominatee
        write_message(args,"Start phase 2","INFO")
        for name, node in tqdm(dict_of_objects.items()):
            node.node_decision(args)
    return start

def main_process(dict_of_objects:dict,algorithm:str,args:argparse.ArgumentParser):
    """
    Description: Plot network

    Args:
        dict_of_objects (dict): A dictionary with all objects of nodes
        algorithm (string): The name of the input algorithm
        args (obj): An object with all arguments of user
        user_input (string): A variable with user input
    Returns:
        -
    """
    import graph as g

    if algorithm != "3":
        # Add dominators to CDS
        for _ , node in tqdm(dict_of_objects.items()):
            node.add_node_in_CDS(args)
            message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([dict_of_objects[a].get_name() for a in node.get_dominators()])
            message = message.format(node.get_name(),len(node.get_dominators()))
            write_message(args,message,"DEBUG")
    else:
        # Assign a very large number to k(G') for first time
        vertex_connectivity = float("inf")
        first_time = True
        if args.centrality:
            get_list_of_dominatees().sort(key=lambda tup: (len(dict_of_objects[tup[0]].get_dominators()),tup[1],tup[2]),reverse=True)
        else:
            get_list_of_dominatees().sort(key=lambda tup: (len(dict_of_objects[tup[0]].get_dominators()),tup[1]),reverse=True)
            
        previous_CDS_len = 0
        previous_vertex_connectivity = vertex_connectivity
        while True:
            if len(connected_dominating_set) == 0:
                write_message(args,"This input network cannot create {}-{}-MCDS".format(args.k,args.m),"INFO")
                return ERROR_CODE
            
            # Check constraint 5 and returns list with nodes to become dominators
            write_message(args,"[!] Starting check constraint 5","INFO")
            dominators = check_constraint5(args)
            
            # Add edges between old and new dominators
            edges=[]
            write_message(args,"[+] Create edges between new and old dominators.","INFO")
            if dominators:
                edges +=create_edges(dominators)
            
            # Construct new graph
            write_message(args,"Start phase 3","INFO")
            construct_new_graph(edges,first_time,args)

            # Run algorithm
            write_message(args,"Start phase 4","INFO")
            if previous_CDS_len != len(connected_dominating_set):
                vertex_connectivity = int(remain_on_DS(args,vertex_connectivity,first_time,dominators))
            else:
                add_dominatee_to_CDS(args)
                # if previous_vertex_connectivity != vertex_connectivity:
                #     add_dominatee_to_CDS(args)
                # else:
                #     add_dominatee_to_CDS(args)
                
            # Update variables
            first_time = False     
            previous_CDS_len = len(connected_dominating_set)
            
            # Construct new graph
            construct_new_graph(edges,first_time,args)
            
            if all_dominators_have_k_dominators(int(args.k)) and all_dominees_have_m_dominators(int(args.m)) and g._is_k_connected(args):
                break

def milcom_algorithm(args:argparse.ArgumentParser):
    """
    Description: Create a CDS for this network

    Args:
        pci (String): A variable tell us which PCI algorithm to use
        user_input(int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        -
    """ 
    start = preprocess(dict_of_objects,args.algorithm,args)

    main_process(dict_of_objects,args.algorithm,args)

    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO",True)
    
    plotting(args)
    
    last_step(1,args)

def new_algorithm(args:argparse.ArgumentParser):
    """
    Description: Create a CDS for this network

    Args:
        user_input(int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        -
    """
    start = preprocess(dict_of_objects,args.algorithm,args)

    main_process(dict_of_objects,args.algorithm,args)

    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO",True)

    plotting(args)

    last_step(2,args)

def k_connected(args:argparse.ArgumentParser):
    """
    Description: Check if network is k-connected

    Args:
        args(obj): An object with all user arguments

    Returns:
        -
    """
    network_connectivity = int(find_node_connectivity())
    if network_connectivity < max(int(args.m),int(args.k)):
        write_message(args,"This network is not {}-connected.".format(max(int(args.k),int(args.m))),"ERROR",args.testing)
        write_message(args,"This network is {}-connected.".format(network_connectivity),"INFO",args.testing)
        exit(1)

def robust_algorithm(args:argparse.ArgumentParser):
    """
    Description: Create a CDS for this network

    Args:
        user_input(int): Option 1 is for milcom algorithm, 2 for new algorithm and 3 for robust algorithm

    Returns:
        -
    """
    start = preprocess(dict_of_objects,args.algorithm,args)
    
    main_process(dict_of_objects,args.algorithm,args)
    
    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO",True)
    
    last_step(3,args)