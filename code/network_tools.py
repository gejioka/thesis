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

def create_edges(nodes):
    """
    Description: Create new edges between new nodes and dominators

    Args:
        nodes (list): A list with nodes to be added to graph

    Returns:
        edges
    """
    edges = []

    for node in nodes:
        for neighbor in dict_of_objects[node].get_N_of_u():
            if neighbor in connected_dominating_set.keys():
                edges.append((node,neighbor))
    
    return edges

def add_dominatee_to_CDS(args,vertex_connectivity = False):
    """
    Description: Add dominatee to CDS 

    Args:
        args (obj): An object with all user input arguments

    Returns:
        - or ERROR_CODE
    """
    import graph as g

    sequense_size = 1
    next_node = 0
    nodes_list = []
    previous_len_CDS = 0
    while (not g._is_k_connected(args) and sequense_size <= max(int(args.k),int(args.m)) and previous_len_CDS != len(connected_dominating_set)) or vertex_connectivity:
        previous_len_CDS = len(connected_dominating_set)
        
        try:
            nodes_list = [get_list_of_dominatees()[next_node][0]]
        except Exception:
            next_node = 0
            sequense_size += 1
        if sequense_size > 1:
            for i in range(max(int(args.k),int(args.m))):
                if next_node < len(get_list_of_dominatees()):
                    nodes_list = find_sequense_nodes(nodes_list,get_list_of_dominatees())
        
        if len(nodes_list) == 0 or next_node >= len(get_list_of_dominatees()): #sequense_size:
            next_node = 0
            sequense_size += 1

        dom_list = []
        for node in nodes_list:
            if len(dict_of_objects[node].get_dominators()) >= int(args.k):
                dom_list.append(node)
                if len(dom_list) >= max(int(args.k),int(args.m)):
                    break

        for node in dom_list:
            connected_dominating_set[node] = 1
            add_dominator_to_all_nodes(node)
            remove_nodes_from_dominatees([node])
            g.add_node(node)

            try:
                get_list_of_dominatees().pop(get_list_of_dominatees().index([i for i in get_list_of_dominatees() if i[0] == node][0]))
                write_message(args,"Node with name {} removed from list of dominatees!!!".format(node),"INFO")
                if all_dominators_have_k_dominators(int(args.k)) and all_dominees_have_m_dominators(int(args.m)) and g._is_k_connected(args):
                    break
            except Exception:
                pass
        
        next_node += 1

        if sequense_size > max(int(args.k),int(args.m)):
            write_message(args,"This input network cannot create {}-{}-MCDS".format(args.k,args.m),"INFO")
            return -1

def get_network_layers():
    """
    Description: Return the number of layers in the network.

    Args:
        -

    Returns:
        number_of_layers
    """
    list_of_layers = []
    number_of_layers = 0
    
    for key in dict_of_objects.keys():
        if int(dict_of_objects[key].get_layer()) not in list_of_layers:
            list_of_layers.append(int(dict_of_objects[key].get_layer()))
            number_of_layers += 1
    
    return number_of_layers

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
            if int(args.algorithm) == 2:
                for node in dict_of_objects:
                    node_obj = dict_of_objects[node]
                    if key in node_obj.get_dominators():
                        node_obj.add_temp_dominator(key)
                        node_obj.get_dominators().remove(key)

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
                
                if int(args.algorithm) == 2:
                    for node in dict_of_objects:
                        node_obj = dict_of_objects[node]
                        if key in node_obj.get_temp_dominators():
                            node_obj.get_dominators().append(key)
                            node_obj.delete_temp_dominator(key)
                        node_obj.clear_temp_dominators()
        else:
            import graph as g

            g.remove_node(key)
            write_message(args,"Try to remove dominator from neighbor for all nodes...","INFO")
            for node in dict_of_objects:
                node_obj = dict_of_objects[node]
                try:
                    node_obj.get_dominators().remove(key)
                    node_obj.add_temp_dominator(key)
                except Exception:
                    pass
            write_message(args,"Check if network is connected without node {}".format(key),"INFO")
            
            if all_dominators_have_k_dominators(int(args.k)) and all_dominees_have_m_dominators(int(args.m)) and g._is_k_connected(args):
                for node in dict_of_objects:
                    node_obj = dict_of_objects[node]
                    node_obj.clear_temp_dominators()
                    
                write_message(args,"[-] Node with name {} removed from CDS".format(key),"INFO")
            else:
                connected_dominating_set[key] = value
                for node in dict_of_objects:
                    node_obj = dict_of_objects[node]
                    if key in node_obj.get_temp_dominators():
                        node_obj.get_dominators().append(key)
                        node_obj.delete_temp_dominator(key)
                    node_obj.clear_temp_dominators()
                g.add_node(key)
                add_dominator_to_all_nodes(key)
                write_message(args,"[!] Node with name {} cannot be removed because CDS will disconnected".format(key),"INFO")
                counter += 1
                
def add_next_dominators(list_of_next_dominators,args):
    """
    Description: Add next dominators to connected dominating set

    Args:
        list_of_next_dominators (list): A list with next dominators

    Returns:
        -
    """
    import graph as g

    # Sort list of next dominators by how important are
    sorted_list_of_next_dominators = sorted(list_of_next_dominators.items(), key=operator.itemgetter(1))  
    
    # Add next dominators until DS be connected
    for node in sorted_list_of_next_dominators:
        connected_dominating_set[node[0]] = node[1]
        g.add_node(node[0],False)
        add_dominator_to_all_nodes(node[0])
        remove_nodes_from_dominatees([node[0]])
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
            write_message(args,err,"WARNING")

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
                number_of_dominatees += 1
        return number_of_dominatees

def add_dominator_to_all_nodes(dominator):
    """
    Description: Add new dominator as neighbor to all nodes

    Args:
        dominator (string): A string with name of specific dominator

    Returns:
        -
    """
    
    for node in dict_of_objects.keys():
        node_obj = dict_of_objects[node]
        if dominator in node_obj.get_N_of_u():
            if dominator not in node_obj.get_dominators():
                node_obj.get_dominators().append(dominator)

def remove_dominators_from_all_nodes(dominators):
    """
    Description: Remove dominators from all nodes in graph.

    Args:
        dominator (string): A string with name of specific dominator

    Returns:
        -
    """
    for node in dict_of_objects.keys():
        node_obj = dict_of_objects[node]
        for dominator in dominators:
            node_obj.remove_dominator(dominator)

def remove_nodes_from_dominatees(nodes):
    """
    Description: Remove nodes from list of dominatees

    Args:
        nodes (list): A list with nodes to be deleted from list

    Returns:
        -
    """
    _to_remove = []
    for node in nodes:
        if node in connected_dominating_set.keys():
            _to_remove.append(node)
    
    set_list_of_dominatees([i for i in get_list_of_dominatees() if i[0] not in _to_remove])

def find_sequense_nodes(nodes_list,dominatee):
    """
    Description: Find a team of nodes who previous were dominatees and need turn to dominators 

    Args:
        nodes_list (list): A list with nodes to be added to CDS
        dominatee (string): The name of the first dominatee
    Returns:
        nodes_list
    """
    same_nodes = 0
    
    for dominatee in get_list_of_dominatees():
        if dominatee not in nodes_list:
            dominatee_obj = dict_of_objects[dominatee[0]]
            for node in nodes_list:
                if node in dominatee_obj.get_N_of_u():
                    same_nodes += 1
            if same_nodes == len(nodes_list):
                nodes_list.append(dominatee[0])
        
                return nodes_list
    return []

def remove_nodes_from_DS(dominators):
    """
    Description: Remove dominators from dominating set.

    Args:
        dominators (list): A list with dominators to be removed

    Returns:
        -
    """
    for dominator in dominators:
        connected_dominating_set.pop(dominator)

def all_dominees_have_m_dominators(m,return_list=False):
    """
    Description: Check if all dominees have at least m dominators

    Args:
        m (int): The minimum number of dominators need to have every node

    Returns:
        -
    """
    _no_connected_dominatees = []
    for key in dict_of_objects.keys():
        node_obj = dict_of_objects[key]
        if len(node_obj.get_dominators()) < int(m):
            if not return_list:
                return False
            else:
                _no_connected_dominatees.append(key)
    if not return_list:
        return True
    else:
        if _no_connected_dominatees:
            return _no_connected_dominatees
        else:
            return True

def all_dominators_have_k_dominators(k,return_list=False):
    """
    Description: Check if all dominators have at least k dominators as neighbors

    Args:
        k (int): The minimum number of dominators need to have every dominator as neighbor

    Returns:
        boolean
    """
    _no_connected_dominators = []
    for key in connected_dominating_set.keys():
        dominator = dict_of_objects[key]
        if len(dominator.get_dominators()) < int(k):
            if not return_list:
                return False
            else:
                _no_connected_dominators.append(key)
    if not return_list:
        return True
    else:
        if _no_connected_dominators:
            return _no_connected_dominators
        else:
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