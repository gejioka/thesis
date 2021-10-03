from __future__ import division
import math
import networkx as nx
import metrics as mt
from graph import *
from global_variables import *

class Node:
    def __init__(self:object,name:str):
        """
        Description: Initialize object

        Args:
            name (String): The name of this node

        Returns:
            An object type Node
        """
        self.name = name
        self.clPCI = 0.0
        self.xPCI_value = 0
        self.newPCI = 0.0
        self.laPCI = 0
        self.alPCI = 0
        self.mlPCI = 0
        self.node_degree = 0
        self.localPCI = 0
        self.lsPCI = 0
        self.weight = 0.0
        self.centrality = 0.0
        self.N_of_u = []
        self.N2_of_u = []
        self.N3_of_u = []
        self.dominators = []
        self.dominatees = []
        self.temp_dominators = []
        self.centralities_list = []
        self.number_of_dominatees = 0

        self.Ns_of_u_dict = {1:self.N_of_u,2:self.N2_of_u,3:self.N3_of_u}
       
    def get_name(self:object):
        """
        Description: Return name of node

        Args:
            -

        Returns:
            name
        """
        return self.name
    
    def set_layer(self:object,layer:int):
        """
        Description: Set layer of node

        Args:
            layer (int): A variable for the layer

        Returns:
            -
        """
        self.layer = layer
    
    def get_layer(self:object):
        """
        Description: Return layer of node

        Args:
            -

        Returns:
            layer
        """
        return self.layer
    
    def set_node_degree(self:object,node_degree:int):
        """
        Description: Set degree of node

        Args:
            layer (int): A variable for node degree

        Returns:
            -
        """
        self.node_degree = node_degree

    def get_node_degree(self:object):
        """
        Description: Return node degree

        Args:
            -

        Returns:
            node_degree
        """
        return self.node_degree

    def find_N_of_u(self:object,intralinks:list,interlinks:list):
        """
        Description: Find N(u) where u is specific node

        Args:
            intralinks (list): A list with intra-layer links
            interlinks (list): A list with inter-layer links

        Returns:
            N(u)
        """
        self.N_of_u = intralinks
        for neighbor in interlinks:
            self.N_of_u = self.N_of_u + interlinks[neighbor]
        self.N_of_u = self.remove_duplicate(self.N_of_u)
        self.Ns_of_u_dict[1] = self.N_of_u

    def set_N_of_u(self:object,N_of_u:list):
        """
        Description: Set N(u)

        Args:
            N_of_u (list): List with neighbor of u

        Returns:
            -
        """
        self.N_of_u = N_of_u
    
    def get_N_of_u(self:object):
        """
        Description: Return N(u) where u is specific node

        Args:
            -

        Returns:
            N_of_u list
        """
        return self.N_of_u
    
    def set_intralinks(self:object,intralinks:list):
        """
        Description: Set list with intra-layer links 

        Args:
            intralinks (list): List of intra-layer links

        Returns:
            -
        """
        self.intralinks = intralinks
    
    def get_intralinks(self:object):
        """
        Description: Return list with intra-layer links

        Args:
            -
        Returns:
            A list with all intra-layer links
        """
        return self.intralinks

    def set_interlinks(self:object,interlinks:list):
        """
        Description: Set list with inter-layer links

        Args:
            interlinks (list): List of inter-layer links

        Returns:
            -
        """
        self.interlinks = interlinks
    
    def get_interlinks(self:object):
        """
        Description: Return list of inter-layer links

        Args:
            -

        Returns:
            A list with all inter-layer links
        """
        return self.interlinks
    
    def set_localPCI(self:object,localPCI:int):
        """
        Description: Set local PCI of this node

        Args:
            localPCI (int): A variable which tell us how important is this node in it's neighborhood

        Returns:
            -
        """
        self.localPCI = localPCI
    
    def get_localPCI(self:object):
        """
        Description: Return local PCI of this node

        Args:
            -

        Returns:
            localPCI
        """
        return self.localPCI

    def set_xPCI(self:object,xPCI_value:float):
        """
        Description: Set xPCI value of node

        Args:
            xPCI_value

        Returns:
            -
        """
        self.xPCI_value = xPCI_value
    
    def get_xPCI(self:object):
        """
        Description: Return xPCI value of node

        Args:
            -

        Returns:
            xPCI_value of node
        """
        return self.xPCI_value
    
    def set_xPCI_nodes(self:object,xPCI_nodes:list):
        """
        Description: Set xPCI nodes list

        Args:
            xPCI_nodes

        Returns:
            -
        """
        self.xPCI_nodes = xPCI_nodes
    
    def get_xPCI_nodes(self:object):
        """
        Description: Return a list with all nodes participate xPCI of this node

        Args:
            -

        Returns:
            xPCI nodes list
        """
        return self.xPCI_nodes
    
    def set_laPCI(self:object,laPCI:int):
        """
        Description: Set laPCI for this node.

        Args:
            laPCI (int): Number for layer agnostic PCI metric

        Returns:
            -
        """
        self.laPCI = laPCI

    def get_laPCI(self:object):
        """
        Description: Return laPCI for this node

        Args:
            -

        Returns:
            laPCI
        """
        return self.laPCI

    def set_alPCI(self:object,alPCI:int):
        """
        Description: Set alPCI for this node.

        Args:
            laPCI (int): Number for all layer PCI metric

        Returns:
            -
        """
        self.alPCI = alPCI
    
    def get_alPCI(self:object):
        """
        Description: Return alPCI for this node

        Args:
            -

        Returns:
            alPCI
        """
        return self.alPCI

    def set_mlPCI(self:object,mlPCI:int):
        """
        Description: Set mlPCI for this node.

        Args:
            mlPCI (int): Number which tell us that, node has at least k neighbors in n layers

        Returns:
            -
        """
        self.mlPCI = mlPCI

    def get_mlPCI(self:object):
        """
        Description: Return mlPCI for this node

        Args:
            -

        Returns:
            mlPCI
        """
        return self.mlPCI

    def set_lsPCI(self:object,lsPCI:int):
        """
        Description: Set lsPCI for this node.

        Args:
            lsPCI (int): Number which tell us that, node has at least n neighbors in n layers

        Returns:
            -
        """
        self.lsPCI = lsPCI

    def get_lsPCI(self:object):
        """
        Description: Return lsPCI for this node

        Args:
            -

        Returns:
            lsPCI
        """
        return self.lsPCI

    def set_newPCI(self:object,newPCI:int):
        """
        Description: Set newPCI for this node

        Args:
            newPCI (int): Variable for new PCI of node

        Returns:
            -
        """
        self.newPCI = newPCI

    def get_newPCI(self:object):
        """
        Description: Return newPCI for this node

        Args:
            -

        Returns:
            newPCI
        """
        return self.newPCI

    def find_weight(self:object):
        """
        Description: Find how important is this node

        Args:
            -

        Returns:
            -
        """
        self.weight = 0.3*self.localPCI + 0.7*self.newPCI

    def set_weight(self:object,weight:float):
        """
        Description: Set total weight for this node 

        Args:
            weight (float): Variable for total weight

        Returns:
            -
        """
        self.weight = weight

    def get_weight(self:object):
        """
        Description: Return the weight for this node

        Args:
            -

        Returns:
            weight
        """
        return self.weight

    def find_betweeness_centrality(self:object):
        """
        Description: Create local network and find betweeness centrality for node

        Args:
            dict_of_objects: A dictionary with all nodes of input network

        Returns:
            betweeness centrality
        """
        list_of_nodes = []
        
        list_of_nodes = self.N_of_u
        local_network = return_subgraph(list_of_nodes)
        
        self.centralities_list = sorted([items for items in nx.betweenness_centrality(local_network).items() if items[1] > 0.0],key=lambda x: x[1],reverse=True)
    
    def get_centrality(self:object):
        """
        Description: Return node betweeness centrality

        Args:
            -

        Returns:
            betweeness centrality
        """
        return self.centrality

    def increace_centrality(self:object,centrality:float):
        """
        Description: Increace node betweeness centrality

        Args:
            centrality (float): Centrality of node

        Returns:
            betweeness centrality
        """
        self.centrality += centrality

    def get_centralities_list(self:object):
        """
        Description: Return a list with betweeness centralities for all neighbor nodes

        Args:
            -

        Returns:
            centralities list
        """
        return self.centralities_list

    def find_clPCI(self:object):
        """
        Description: Find clPCI value for this node

        Args:
            -

        Returns:
            -
        """
        try:
            self.clPCI = self.xPCI_value*math.log(self.unique_links,2.0)
        except Exception:
            self.clPCI = 0.0

    def get_clPCI(self:object):
        """
        Description: Return clPCI value for this node

        Args:
            -

        Returns:
            clPCI value
        """
        return self.clPCI

    def set_unique_links_between_nodes(self:object,unique_links:int):
        """
        Description: Set unique links between nodes participate xPCI for this node

        Args:
            unique_links

        Returns:
            -
        """
        self.unique_links = unique_links

    def remove_duplicate(self:object,input_list:list):
        """
        Description: Remove all duplicate items of input list

        Args:
            input_list (list): The input list

        Returns:
            A list without duplicates
        """ 
        final_list = []
        for item in input_list: 
            if item not in final_list: 
                final_list.append(item) 
        return final_list
    
    def remove_dominator(self:object,dominator:str):
        """
        Description: Remove dominator of list

        Args:
            dominator (string): The name of dominator

        Returns:
            -
        """ 
        if dominator in self.dominators:
            self.dominators.remove(dominator)
    
    def find_N2_or_N3_of_u(self:object,nodes:dict,neighborhood:list):
        """
        Description: Find N2(u) where u is specific node

        Args:
            nodes (dictionary): A dictionary with all nodes

        Returns:
            N2(u)
        """
        # Create a list with next neighborhood of node
        for neighbor in self.Ns_of_u_dict[neighborhood-1]:
            self.Ns_of_u_dict[neighborhood] = self.Ns_of_u_dict[neighborhood] + nodes[neighbor]["intralinks"]
            try:
                self.Ns_of_u_dict[neighborhood] = self.Ns_of_u_dict[neighborhood] + reduce(lambda x,y :x+y,nodes[neighbor]["interlinks"].values())
            except Exception:
                pass
        self.Ns_of_u_dict[neighborhood] = self.remove_duplicate(self.Ns_of_u_dict[neighborhood])
        try:
            self.Ns_of_u_dict[neighborhood].remove(self.name)
        except Exception:
            pass

        # Check if next neighborhood is N2(u) and remove all nodes of list exist in N(u)
        if neighborhood == 2:
            self.Ns_of_u_dict[neighborhood] = list(set(self.Ns_of_u_dict[neighborhood])-set(self.Ns_of_u_dict[neighborhood-1]))
            self.N2_of_u = self.Ns_of_u_dict[neighborhood]
        else:
            # Check if next neighborhood is N3(u) and remove all nodes of list exist in N(u) and N2(u)
            self.Ns_of_u_dict[neighborhood] = list(set(self.Ns_of_u_dict[neighborhood])-set(self.Ns_of_u_dict[neighborhood-1]))
            if len(self.N_of_u) > len(self.Ns_of_u_dict[neighborhood]):
                self.Ns_of_u_dict[neighborhood] = list(set(self.Ns_of_u_dict[neighborhood-2])-set(self.Ns_of_u_dict[neighborhood]))
            else:
                self.Ns_of_u_dict[neighborhood] = list(set(self.Ns_of_u_dict[neighborhood])-set(self.Ns_of_u_dict[neighborhood-2]))
            self.N3_of_u = self.Ns_of_u_dict[neighborhood]
        
        return self.Ns_of_u_dict[neighborhood]

    def get_N2_of_u(self:object):
        """
        Description: Return two hopes away neighbors of this node

        Args:
            -

        Returns:
            N2_of_u
        """
        return self.N2_of_u
    
    def get_N3_of_u(self:object):
        """
        Description: Return three hopes away neighbors of this node

        Args:
            -

        Returns:
            N3_of_u
        """
        return self.N3_of_u
    
    def get_dominators(self:object):
        """
        Description: Return a list with all dominators for this node

        Args:
            -

        Returns:
            dominators
        """
        return self.dominators
    
    def add_temp_dominator(self:object,temp_dominator:str):
        """
        Description: Add a temporary dominator to list

        Args:
            temp_dominator(String): The name of temporary dominator

        Returns:
            dominators
        """
        self.temp_dominators.append(temp_dominator)
    
    def delete_temp_dominator(self:object,temp_dominator:str):
        """
        Description: Delete a temporary dominator frmo list

        Args:
            temp_dominator(String): The name of temporary dominator

        Returns:
            -
        """
        try:
            self.temp_dominators.remove(temp_dominator)
        except Exception:
            pass
    
    def clear_temp_dominators(self:object):
        """
        Description: Clear list of temp dominators

        Args:
            -

        Returns:
            -
        """
        self.temp_dominators = []

    def get_temp_dominators(self:object):
        """
        Description: Return temporary dominators of this node

        Args:
            -

        Returns:
            temp_dominators
        """
        return self.temp_dominators
    
    def find_all_nodes_to_3hops(self:object):
        """
        Description: Create a list with all nodes 3-hop away from each node in network

        Args:
            start_node (String): Name of specific node

        Returns:
            N2_of_u
        """
        self.all_3hop_nodes = []
        self.all_3hop_nodes = self.N_of_u + self.N2_of_u + self.N3_of_u

    def get_all_nodes_to_3hop(self:object):
        """
        Description: Return a list with all nodes 3-hop away from this node

        Args:
            -

        Returns:
            all_3hop_nodes
        """
        return self.all_3hop_nodes

    def find_Nu_PCIs(self:object,dict_of_objects:dict,pci:str,args:argparse.ArgumentParser):
        """
        Description: Add all xPCI values of neighbors to a list and sort it

        Args:
            dict_of_objects (list): A list with all node objects

        Returns:
            -
        """
        self.Nu_xPCIs_list = []
        for neighbor in self.N_of_u:
            node_obj = dict_of_objects[neighbor]
            if node_obj != None:
                if pci == "degree":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_node_degree(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_node_degree()))
                elif pci == "sl":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_localPCI(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_localPCI()))
                elif pci == "la":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_laPCI(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_laPCI()))
                elif pci == "al":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_alPCI(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_alPCI()))
                elif pci == "ml":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_mlPCI(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_mlPCI()))
                elif pci == "ls":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_lsPCI(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_lsPCI()))
                elif pci == "x":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_xPCI(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_xPCI()))
                elif pci == "cl":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_clPCI(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_clPCI()))
                elif pci == "new":
                    if args.centrality:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_weight(),node_obj.get_centrality()))
                    else:
                        self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_weight()))

        if args.centrality:      
            self.Nu_xPCIs_list.sort(key=lambda tup: (tup[1],tup[2]),reverse=True)
        else:
            self.Nu_xPCIs_list.sort(key=lambda tup: tup[1],reverse=True)

    def check_for_dominator(self:object,dict_of_objects:dict):
        """
        Description: Check if all nodes has dominators

        Args:
            dict_of_objects (list): A list with all node objects

        Returns:
            dominator or None if doesn't exist
        """
        node_obj = dict_of_objects[self.get_name()]
        for dominator in connected_dominating_set:
            if dominator in node_obj.get_N_of_u():
                return dominator
        return None

    def find_next_dominators(self:object,node_obj:object,next_dominators_dict:dict):
        """
        Description: Find next dominator

        Args:
            node_obj(object): An object with node informations
            next_dominators_dict(dictionary): A dictionary with all dominators
        Returns:
            next_dominators_dict
        """
        if not set(node_obj.get_N_of_u()) & set([a[0] for a in connected_dominating_set]):
            for neighbor in node_obj.get_N_of_u():
                if neighbor not in next_dominators_dict:
                    next_dominators_dict[neighbor] = 1
                else:
                    next_dominators_dict[neighbor] += 1
        return next_dominators_dict

    def node_decision(self:object,args:argparse.ArgumentParser):
        """
        Description: Node decide for itself to be a dominator

        Args:
            args (obj): An object with all arguments of user

        Returns:
            -
        """
        # A dictionary with all PCI metrics
        metrics_dict = {"degree"    : self.node_degree,
                        "cl"        : self.clPCI,
                        "x"         : self.xPCI_value,
                        "new"       : self.newPCI,
                        "la"        : self.laPCI,
                        "al"        : self.alPCI,
                        "ml"        : self.mlPCI,
                        "ls"        : self.lsPCI,
                        "sl"        : self.localPCI}

        if len(self.dominators) < int(args.m):
            for neighbor in self.N_of_u:
                if neighbor in list(connected_dominating_set.keys()):
                    if neighbor not in self.dominators:
                        self.dominators.append(neighbor)
            if len(self.dominators) < int(args.m):
                if self.name not in list(connected_dominating_set.keys()):
                    if args.algorithm != "3":
                        connected_dominating_set[self.name] = 1
                    else:
                        counter = 0
                        for neighbor in self.N_of_u:
                            if neighbor in list(connected_dominating_set.keys()):
                                counter += 1
                        if counter >= int(args.k):
                            connected_dominating_set[self.name] = 1
                            add_dominator_to_all_nodes(self.name)
                            remove_nodes_from_dominatees([self.name])
                else:
                    connected_dominating_set[self.name] += 1
            else:
                if args.pci:
                    if args.centrality:
                        append_list_of_dominatees((self.name,metrics_dict[args.pci],self.centrality))
                    else:
                        append_list_of_dominatees((self.name,metrics_dict[args.pci]))
                else:
                    if args.centrality:
                        append_list_of_dominatees((self.name,metrics_dict["cl"],self.centrality))
                    else:
                        append_list_of_dominatees((self.name,metrics_dict[args.pci]))
        else:
            if args.pci:
                if args.centrality:
                    append_list_of_dominatees((self.name,metrics_dict[args.pci],self.centrality))
                else:
                    append_list_of_dominatees((self.name,metrics_dict[args.pci]))
            else:
                if args.centrality:
                    append_list_of_dominatees((self.name,metrics_dict["cl"],self.centrality))
                else:
                    append_list_of_dominatees((self.name,metrics_dict[args.pci]))

    def construct_m_value(self,args):
        """
        Description: Construct m value and return it

        Args:
            args (object): An object with all user arguments

        Returns:
            m
        """
        m = 0
        if args.m:
            m = int(args.m)
        else:
            m = 1
        return m

    def choose_node(self:object,node_1:tuple,node_2:tuple,args:argparse.ArgumentParser):
        """
        Description: Compare two nodes and return more significant

        Args:
            node_1 (tuple): A tuple with informations for node 1 (name,PCI,centrality)
            node_2 (tuple): A tuple with informations for node 2 (name,PCI,centrality)
        Returns:
            node
        """
        if node_1[2] / node_2[2] <= 1 - float(args.tolerance): 
            return node_2[0]
        else:
            if node_2[1] / node_1[1] > 1 - node_1[2] / node_2[2]: 
                return node_1[0]
            return node_2[0]
            

    def compare_nodes(self:object,node_1:tuple,node_2:tuple,args:argparse.ArgumentParser):
        """
        Description: Compare n and n-1 nodes and return the most significant of two nodes 

        Args:
            node_1 (tuple): A tuple with all informations for node 1
            node_2 (tuple): A tuple with all informations for node 2 
            args (obj): An object with all user arguments
        Returns:
            node 
        """
        
        if node_1[1] > 0:
            if node_2[1] / node_1[1] >= 1 - float(args.tolerance): # Find the ratio between PCIn-1 and PCIn and compare it with user input tolerance
                if node_2[2] > node_1[2]:
                    return self.choose_node(node_1,node_2,args) 
                else:
                    if node_1[2] > 0: 
                        return self.choose_node(node_2,node_1,args)
                    else:
                        return node_1[0]
        else:
            if node_2[2] > node_1[2]:
                return node_2[0]
            else:
                return node_1[0]

        return node_1[0]

    def find_dominator(self:object,dict_of_objects:dict,args:argparse.ArgumentParser):
        """
        Description: Find dominator of node

        Args:
            -

        Returns:
            -
        """
        m = self.construct_m_value(args)

        for i in range(m):
            for node in list(connected_dominating_set.keys()):
                node_obj = dict_of_objects[node]
                if self.name in node_obj.get_N_of_u():
                    if node not in self.dominators:
                        self.dominators.append(node)
                        add_dominator_to_all_nodes(node)
                        remove_nodes_from_dominatees([node])
                        break

        if args.centrality:         
            self.Nu_xPCIs_list.sort(key=lambda x: (x[1],x[2]),reverse=True)
        else:
            self.Nu_xPCIs_list.sort(key=lambda x: x[1],reverse=True)

        new_node = self.compare_nodes(self.Nu_xPCIs_list[0],self.Nu_xPCIs_list[1],args) if len(self.Nu_xPCIs_list) > 1 and args.centrality else self.Nu_xPCIs_list[0][0]
        if new_node in list(connected_dominating_set.keys()):
            connected_dominating_set[new_node] += 1
        else:
            connected_dominating_set[new_node] = 1
            add_dominator_to_all_nodes(new_node)
            remove_nodes_from_dominatees([new_node])
                
    def all_2_hop_has_dominator(self:object):
        """
        Description: Check if all 2 hop neighbors have dominator

        Args:
            -

        Returns:
            boolean
        """
        for _2_hop_neighbor in self.N2_of_u:
            nodeObj = dict_of_objects[_2_hop_neighbor]
            has_dominator = False
            for neighbor in nodeObj.get_N_of_u():
                if neighbor in list(connected_dominating_set.keys()) and neighbor in self.N_of_u:
                    has_dominator = True
            if not has_dominator:
                return False
        return True

    def add_node_in_CDS(self:object,args:argparse.ArgumentParser):
        """
        Description: Check if exists node of N2 of u without dominator as neighbor
                     and if so add as dominator node of N of u this with largest xPCI
                     covers at least one new node in N2 of u.

        Args:
            -

        Returns:
            -
        """
        
        if args.centrality:
            self.Nu_xPCIs_list.sort(key=lambda x: (x[1],x[2]),reverse=True)
        else:
            self.Nu_xPCIs_list.sort(key=lambda x: x[1],reverse=True)
        
        if not self.all_2_hop_has_dominator():
            counter = 1
            for node in self.Nu_xPCIs_list:
                nodeObj = dict_of_objects[self.compare_nodes(self.Nu_xPCIs_list[counter-1],self.Nu_xPCIs_list[counter],args)] if len(self.Nu_xPCIs_list) > 1 and args.centrality else dict_of_objects[node[0]]
                if self.all_2_hop_has_dominator():
                    break
                for _2_hop_neighbor in nodeObj.get_N_of_u():
                    if _2_hop_neighbor in self.N2_of_u:
                        _2_hop_neighborObj = dict_of_objects[_2_hop_neighbor]
                        if nodeObj.get_name() not in list(connected_dominating_set.keys()):
                            connected_dominating_set[nodeObj.get_name()] = 1
                        else:
                            connected_dominating_set[nodeObj.get_name()] += 1
                        if node[0] not in _2_hop_neighborObj.get_dominators():
                            _2_hop_neighborObj.get_dominators().append(node[0])
                            if node[0] not in self.dominators:
                                self.dominators.append(node[0])
                            break
                counter += 1

    def print_number_of_dominators(self:object,args:argparse.ArgumentParser):
        """
        Description: Print the number of dominators for specific node

        Args:
            -

        Returns:
            -
        """
        if self.name not in list(connected_dominating_set.keys()):
            write_message(args, "Number of dominators for node with name {} is {}".format(self.name,len(self.dominators)) + " and list of names is: [%s]"%", ".join([a.get_name() for a in self.dominators]), "INFO")
        else:
            write_message(args, "Node with name {} is dominator and number of dominators for this node is {}".format(self.name,len(self.dominators)) + " and list of names is: [%s]"%", ".join([a.get_name() for a in self.dominators]), "INFO")
    
    def __str__(self:object):
        """
        Description: Change str representation of node object

        Args:
            -

        Returns:
            New representation of str
        """
        string_obj = "Name of node is: " + str(self.name) + "\n" + "Layer of node is: " + str(self.layer) + "\n" + "Intra-layer links are: " + str(self.intralinks) + "\n" + "Inter-layer links are: " + str(self.interlinks) + "\n" + "N(u) is: " + str(self.N_of_u) + "\n" + "N2(u) is: " + str(self.N2_of_u) + "\n" + "xPCI is: " + str(self.xPCI_value) + "\n" + "Unique links are: " + str(self.unique_links) + "\n"
        return string_obj