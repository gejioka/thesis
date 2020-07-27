from network_tools import *
from metrics import *
from graph import *
import ml_visualization as mlv
import time
import sys

### Global variables ###
ERROR_CODE = -1

def last_step(algorithm,args):
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

        connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
        if args.time:
            end = time.time()
            write_message(args,"Time running process 4: {}".format(end-start),"INFO",True)
        is_connected = False
        if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
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
            non_significant_nodes = [k for k,v in results[0].iteritems() if int(v) == 0]
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
        connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
        if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
            write_message(args,"Dominating set (DS) is connected.","INFO")
        else:
            write_message(args,"Dominating set (DS) is not connected.","INFO")

    plotting(args,True)
    all_dominees_have_dominators()

def plotting(args,input_graph=False):
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
    if args.time:
        if args.mcds:
            write_process_message(args,3,True)
        else:
            write_process_message(args,3,False)
        start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        if args.pci == "cl":
            node.set_unique_links_between_nodes(find_links_between_neighbors(node.get_xPCI_nodes()))
            node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,args.pci)
        node.find_dominator(dict_of_objects,args)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_dominators()])
        message = message.format(node.get_name(),len(node.get_dominators()))
        write_message(args,message,"DEBUG")
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_dominators()])
        message = message.format(node.get_name(),len(node.get_dominators()))
        write_message(args,message,"DEBUG")
    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO",True)
    
    plotting(args)
    
    last_step(1,args)

def new_algorithm(user_input,args):
    """
    Description: Create a CDS for this network

    Args:
        user_input(int): Option 1 is for milcom algorithm and 2 for new algorithm

    Returns:
        -
    """
    if args.log:
        write_message(args,"[!] Start running new algorithm","INFO")
    if args.time:
        if args.mcds:
            write_process_message(args,3,True)
        else:
            write_process_message(args,3,False)
        start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        if args.pci == "cl":
            node.set_unique_links_between_nodes(find_links_between_neighbors(node.get_xPCI_nodes()))
            node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,args.pci)
        node.find_dominator(dict_of_objects,args)
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_dominators()])
        message = message.format(node.get_name(),len(node.get_dominators()))
        write_message(args,message,"DEBUG")
    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO",True)

    plotting(args)

    last_step(2,args)

def is_k_connected(args):
    """
    Description: Check if network is k-connected

    Args:
        args(obj): An object with all user arguments

    Returns:
        -
    """
    network_connectivity = int(find_node_connectivity())
    if network_connectivity < max(int(args.m),int(args.k)):
        write_message(args,"This network is not {}-connected.".format(args.m),"ERROR",args.testing)
        write_message(args,"This network is {}-connected.".format(network_connectivity),"INFO",args.testing)
        exit(1)

def robust_algorithm(user_input,args):
    """
    Description: Create a CDS for this network

    Args:
        user_input(int): Option 1 is for milcom algorithm, 2 for new algorithm and 3 for robust algorithm

    Returns:
        -
    """
    # Check if input network is k-connected
    is_k_connected(args)

    # Write log messages
    if args.log:
        write_message(args,"[!] Start running robust algorithm","INFO")
    if args.time:
        if args.mcds:
            write_process_message(args,3,True)
        else:
            write_process_message(args,3,False)
        start = time.time()
    
    # Create Dominating Set (DS) of network
    write_message(args,"Start phase 1","INFO")
    for name, node in dict_of_objects.iteritems():
        if args.pci == "cl":
            node.set_unique_links_between_nodes(find_links_between_neighbors(node.get_xPCI_nodes()))
            node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,args.pci)
        node.find_dominator(dict_of_objects,args)

    # Every node decides whether it is dominator or dominatee
    write_message(args,"Start phase 2","INFO")
    for name, node in dict_of_objects.iteritems():
        node.node_decision(args)
    
    # Assign a very large number to k(G') for first time
    vertex_connectivity = float("inf")

    counter = 0
    list_of_dominatees.sort(key=lambda tup: tup[1],reverse=True)
    while True:
        # Stop running algorithm when vertex_connectivity become smaller than k
        if vertex_connectivity >= int(args.k) and vertex_connectivity != float("inf") and all_dominators_have_k_dominators(int(args.k)) and all_dominees_have_m_dominators(int(args.m)) :
            break
        
        if check_constraint5(args) == ERROR_CODE:
            sys.exit(1)

        # Construct new graph
        write_message(args,"Start phase 3","INFO")
        construct_new_graph(args)

        # Run algorithm
        write_message(args,"Start phase 4","INFO")
        vertex_connectivity = remain_on_DS(args,vertex_connectivity)

        # try:
        #     write_message(args,"Add dominatee to list of dominators","INFO")
        #     connected_dominating_set[list_of_dominatees[counter][0]] = 1
        #     counter += 1
        # except Exception:
        #     pass
    
    # write_message(args,"Start phase 3","INFO")
    # construct_new_graph(args)
    # write_message(args,"Start phase 4","INFO")
    # vertex_connectivity = remain_on_DS(args,vertex_connectivity)
    # write_message(args,"Start phase 5","INFO")
    # list_of_dominatees.sort(key=lambda tup: tup[1],reverse=True)
    # counter=0
    # while vertex_connectivity < int(args.k):
    #     write_message(args,"Repeat phase 6","INFO")
    #     if counter < int(args.m) and list_of_dominatees:
    #         connected_dominating_set[list_of_dominatees[counter][0]] = 1
    #         construct_new_graph(args)
    #         write_message(args,"start phase 6.1","INFO")
    #         vertex_connectivity = remain_on_DS(args,vertex_connectivity)
    #         counter += 1
    #     else:
    #         break
    
    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO",True)
    # print_CDS(args)
    last_step(3,args)