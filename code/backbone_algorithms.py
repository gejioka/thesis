from network_tools import *
from metrics import *
from graph import *
import ml_visualization as mlv
import time


def last_step(algorithm,args):
    """
    Description: Check if DS is connected, minimize it and plot it

    Args:
        -

    Returns:
        -
    """
    if args.time:
        write_message(args,"Process 4 of 6","INFO")
        start = time.time()
    # Check if DS is connected
    connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
    if args.time:
        end = time.time()
        write_message(args,"Time running process 4: {}".format(end-start),"INFO")
    is_connected = False
    if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
        write_message(args,"Dominating set (DS) is connected.","INFO")
        is_connected = True
    else:
        write_message(args,"Dominating set (DS) is not connected.","INFO")
    if algorithm == 2:
        if args.time:
            write_message(args,"Process 5 of 6","INFO")
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
            write_message(args,"Time running process 5: {}".format(end-start),"INFO")
            
    # Find Minimum Connected Dominating Set (MCDS)
    if args.mcds:
        if args.time:
            write_message(args,"Process 6 of 6","INFO")
            start = time.time()
        find_MCDS(args)
        if args.time:
            end = time.time()
            write_message(args,"Time running process 6: {}".format(end-start),"INFO")
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
        write_message(args,"Process 3 of 6","INFO")
        start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        if args.pci == "cl":
            node.set_unique_links_between_nodes(find_links_between_neighbors(node.get_xPCI_nodes()))
            node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,args.pci)
        node.find_dominator(dict_of_objects)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_node_dominators()])
        message = message.format(node.get_name(),len(node.get_node_dominators()))
        write_message(args,message,"DEBUG")
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_node_dominators()])
        message = message.format(node.get_name(),len(node.get_node_dominators()))
        write_message(args,message,"DEBUG")
    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO")
    
    plotting(args)
    
    last_step(1,args)

    # for name, node in dict_of_objects.iteritems():
    #     node.print_number_of_dominators()

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
        write_message(args,"Process 3 of 6","INFO")
        start = time.time()
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        if args.pci == "cl":
            node.set_unique_links_between_nodes(find_links_between_neighbors(node.get_xPCI_nodes()))
            node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,args.pci)
        node.find_dominator(dict_of_objects)
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
        message = "Node with name {} has {} dominators. The dominators are [%s]"%", ".join([a.get_name() for a in node.get_node_dominators()])
        message = message.format(node.get_name(),len(node.get_node_dominators()))
        write_message(args,message,"DEBUG")
    if args.time:
        end = time.time()
        write_message(args,"Time running process 3: {}".format(end-start),"INFO")

    plotting(args)

    last_step(2,args)

    # for name, node in dict_of_objects.iteritems():
    #     node.print_number_of_dominators()

def robust_algorithm(user_input,args):
    """
    Description: Create a CDS for this network

    Args:
        user_input(int): Option 1 is for milcom algorithm, 2 for new algorithm and 3 for robust algorithm

    Returns:
        -
    """
    if args.log:
        write_message(args,"[!] Start running robust algorithm","INFO")
    if args.time:
        write_message(args,"Process 3 of 6","INFO")
        start = time.time()
    
    # Assign a very large number to k(G') for first time
    vertex_connectivity = float("inf")
    
    # Create Dominating Set (DS) of network
    for name, node in dict_of_objects.iteritems():
        if args.pci == "cl":
            node.set_unique_links_between_nodes(find_links_between_neighbors(node.get_xPCI_nodes()))
            node.find_clPCI()
        node.find_Nu_PCIs(dict_of_objects,args.pci)
        node.find_dominator(dict_of_objects)
    for name, node in dict_of_objects.iteritems():
        node.add_node_in_CDS(user_input)
    for name, node in dict_of_objects.iteritems():
        node.node_decision(args)
    construct_new_graph()
    vertex_connectivity = remain_on_DS(args,vertex_connectivity)
    while vertex_connectivity < int(args.k):
        construct_new_graph()
        vertex_connectivity = remain_on_DS(args,vertex_connectivity)
    
    results = poll_nodes_for_dominators({},args)
    non_significant_nodes = [k for k,v in results[0].iteritems() if int(v) == 0]
    add_next_dominators(results[1],args)
    remove_non_significant_nodes(non_significant_nodes,args)

    print_CDS(args)
    plot_input_graph(True)
    plotting(args)
    
    connectivity_list = check_connectivity(dict_of_objects[connected_dominating_set.keys()[0]],[],connected_dominating_set)
    if args.time:
        end = time.time()
        write_message(args,"Time running process 4: {}".format(end-start),"INFO")
    is_connected = False
    if len(set(connectivity_list) & set(dict_of_objects.keys())) == len(connected_dominating_set):
        write_message(args,"Dominating set (DS) is connected.","INFO")
        is_connected = True
    else:
        write_message(args,"Dominating set (DS) is not connected.","INFO")

    # for name, node in dict_of_objects.iteritems():
    #     node.print_number_of_dominators()