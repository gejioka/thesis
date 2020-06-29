from global_variables import *
from log import *
import operator

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
    import graph

    write_message(args,"[!] CDS created. Need to minimize CDS and create MCDS", "INFO")
    write_message(args,"[!] Start to minimize CDS","INFO")
    
    counter = 0
    while counter < len(connected_dominating_set) and len(connected_dominating_set) > 1:
        # Remove dominator from DS to find out if it needs
        key = list(connected_dominating_set.iteritems())[counter][0]
        value = connected_dominating_set.pop(key)
        write_message(args,"[!] Try to remove node with name {}".format(key),"INFO")

        # Check if every dominatee has dominator
        all_nodes = []
        if int(args.algorithm) == 1 or int(args.algorithm) == 2:
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
                write_message(args,"[-] Node with name {} removed from CDS".format(key),"INFO")
                message = "New CDS with out node {} is [%s]"%", ".join([a for a in connected_dominating_set])
                message = message.format(key)
                write_message(args,message,"DEBUG")
        else:
            m_dominators=True
            graph.remove_node(key)
            for node in dict_of_objects:
                node_obj = dict_of_objects[node]
                #if len(node_obj.get_dominators()) < int(args.m) or not graph._is_k_connected(args): 
                if len(set(node_obj.get_N_of_u())&set(connected_dominating_set.keys())) < int(args.m) or not graph._is_k_connected(args):
                    connected_dominating_set[key] = value
                    graph.construct_new_graph()
                    write_message(args,"[!] Node with name {} cannot be removed because CDS will disconnected".format(key),"INFO")
                    counter += 1
                    m_dominators=False
                    break
            if m_dominators:
                dominator_obj = dict_of_objects[key]
                for neighbor in dominator_obj.get_N_of_u():
                    try:
                        dict_of_objects[neighbor].get_dominators().remove(dominator_obj)
                    except Exception:
                        pass
                write_message(args,"[-] Node with name {} removed from CDS".format(key),"INFO")

def add_next_dominators(list_of_next_dominators,args):
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

def remove_non_significant_nodes(non_significant_nodes,args):
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
            if int(args.algorithm) == 3:
                if not all_dominees_have_m_dominators(int(args.m)):
                    connected_dominating_set[node] = value
            else: 
                if not all_dominees_have_dominators():
                    connected_dominating_set[node] = value
            is_connected = True
        if not is_connected:
            connected_dominating_set[node] = value
            write_message(args,"[!] Node with name {} cannot be removed because network disconnected!".format(node), "INFO")
        else:
            write_message(args,"[-] Node with name {} removed from CDS".format(node),"INFO")

def find_number_of_dominatees(node):
        """
        Description: Find the number of dominateesof every node

        Args:
            args (obj): An object with all arguments of user

        Returns:
            -
        """
        number_of_dominatees = 0
        for neighbor in node.get_N_of_u():
            if neighbor not in connected_dominating_set.keys():
            #if dict_of_objects[neighbor] not in node.dominators:
                number_of_dominatees += 1
        return number_of_dominatees

def all_dominees_have_m_dominators(m):
    """
    Description: Check if all dominees have at least m dominators

    Args:
        m (int): The minimum number of dominators need to have every node

    Returns:
        -
    """
    for key in dict_of_objects.keys():
        number_of_dominators = 0
        node_obj = dict_of_objects[key]
        for neighbor in node_obj.get_N_of_u():
            if neighbor in connected_dominating_set.keys():
                number_of_dominators += 1
        if number_of_dominators < m:
            return False
    return True

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
        all_nodes = all_nodes + dict_of_objects[node].get_N_of_u()
    final_list = remove_duplicates(all_nodes)
    if len(final_list) == len(dict_of_objects):
        return True
    
    return False