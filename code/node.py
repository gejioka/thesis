from __future__ import division
import math
import networkx as nx
import metrics as mt
from global_variables import *

class Node:
    def __init__(self,name):
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
        self.N_of_u = []
        self.N2_of_u = []
        self.N3_of_u = []
        self.dominators = []
        self.dominatees = []
        self.number_of_dominatees = 0

        self.Ns_of_u_dict = {1:self.N_of_u,2:self.N2_of_u,3:self.N3_of_u}
       
    def get_name(self):
        """
        Description: Return name of node

        Args:
            -

        Returns:
            name
        """
        return self.name
    
    def set_layer(self,layer):
        """
        Description: Set layer of node

        Args:
            layer (int): A variable for the layer

        Returns:
            -
        """
        self.layer = layer
    
    def get_layer(self):
        """
        Description: Return layer of node

        Args:
            -

        Returns:
            layer
        """
        return self.layer
    
    def set_node_degree(self,node_degree):
        """
        Description: Set degree of node

        Args:
            layer (int): A variable for node degree

        Returns:
            -
        """
        self.node_degree = node_degree

    def get_node_degree(self):
        """
        Description: Return node degree

        Args:
            -

        Returns:
            node_degree
        """
        return self.node_degree

    def find_N_of_u(self,intralinks,interlinks):
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

    def set_N_of_u(self,N_of_u):
        """
        Description: Set N(u)

        Args:
            N_of_u (list): List with neighbor of u

        Returns:
            -
        """
        self.N_of_u = N_of_u
    
    def get_N_of_u(self):
        """
        Description: Return N(u) where u is specific node

        Args:
            -

        Returns:
            N_of_u list
        """
        return self.N_of_u
    
    def set_intralinks(self,intralinks):
        """
        Description: Set list with intra-layer links 

        Args:
            intralinks (list): List of intra-layer links

        Returns:
            -
        """
        self.intralinks = intralinks
    
    def get_intralinks(self):
        """
        Description: Return list with intra-layer links

        Args:
            -
        Returns:
            A list with all intra-layer links
        """
        return self.intralinks

    def set_interlinks(self,interlinks):
        """
        Description: Set list with inter-layer links

        Args:
            interlinks (list): List of inter-layer links

        Returns:
            -
        """
        self.interlinks = interlinks
    
    def get_interlinks(self):
        """
        Description: Return list of inter-layer links

        Args:
            -

        Returns:
            A list with all inter-layer links
        """
        return self.interlinks
    
    def set_localPCI(self,localPCI):
        """
        Description: Set local PCI of this node

        Args:
            localPCI (int): A variable which tell us how important is this node in it's neighborhood

        Returns:
            -
        """
        self.localPCI = localPCI
    
    def get_localPCI(self):
        """
        Description: Return local PCI of this node

        Args:
            -

        Returns:
            localPCI
        """
        return self.localPCI

    def set_xPCI(self,xPCI_value):
        """
        Description: Set xPCI value of node

        Args:
            xPCI_value

        Returns:
            -
        """
        self.xPCI_value = xPCI_value
    
    def get_xPCI(self):
        """
        Description: Return xPCI value of node

        Args:
            -

        Returns:
            xPCI_value of node
        """
        return self.xPCI_value
    
    def set_xPCI_nodes(self,xPCI_nodes):
        """
        Description: Set xPCI nodes list

        Args:
            xPCI_nodes

        Returns:
            -
        """
        self.xPCI_nodes = xPCI_nodes
    
    def get_xPCI_nodes(self):
        """
        Description: Return a list with all nodes participate xPCI of this node

        Args:
            -

        Returns:
            xPCI nodes list
        """
        return self.xPCI_nodes
    
    def set_laPCI(self,laPCI):
        """
        Description: Set laPCI for this node.

        Args:
            laPCI (int): Number for layer agnostic PCI metric

        Returns:
            -
        """
        self.laPCI = laPCI

    def get_laPCI(self):
        """
        Description: Return laPCI for this node

        Args:
            -

        Returns:
            laPCI
        """
        return self.laPCI

    def set_alPCI(self,alPCI):
        """
        Description: Set alPCI for this node.

        Args:
            laPCI (int): Number for all layer PCI metric

        Returns:
            -
        """
        self.alPCI = alPCI
    
    def get_alPCI(self):
        """
        Description: Return alPCI for this node

        Args:
            -

        Returns:
            alPCI
        """
        return self.alPCI

    def set_mlPCI(self,mlPCI):
        """
        Description: Set mlPCI for this node.

        Args:
            mlPCI (int): Number which tell us that, node has at least k neighbors in n layers

        Returns:
            -
        """
        self.mlPCI = mlPCI

    def get_mlPCI(self):
        """
        Description: Return mlPCI for this node

        Args:
            -

        Returns:
            mlPCI
        """
        return self.mlPCI

    def set_lsPCI(self,lsPCI):
        """
        Description: Set lsPCI for this node.

        Args:
            lsPCI (int): Number which tell us that, node has at least n neighbors in n layers

        Returns:
            -
        """
        self.lsPCI = lsPCI

    def get_lsPCI(self):
        """
        Description: Return lsPCI for this node

        Args:
            -

        Returns:
            lsPCI
        """
        return self.lsPCI

    def set_newPCI(self,newPCI):
        """
        Description: Set newPCI for this node

        Args:
            newPCI (int): Variable for new PCI of node

        Returns:
            -
        """
        self.newPCI = newPCI

    def get_newPCI(self):
        """
        Description: Return newPCI for this node

        Args:
            -

        Returns:
            newPCI
        """
        return self.newPCI

    def find_weight(self):
        """
        Description: Find how important is this node

        Args:
            -

        Returns:
            -
        """
        self.weight = 0.3*self.localPCI + 0.7*self.newPCI

    def set_weight(self,weight):
        """
        Description: Set total weight for this node 

        Args:
            weight (float): Variable for total weight

        Returns:
            -
        """
        self.weight = weight

    def get_weight(self):
        """
        Description: Return the weight for this node

        Args:
            -

        Returns:
            weight
        """
        return self.weight

    def find_clPCI(self):
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

    def get_clPCI(self):
        """
        Description: Return clPCI value for this node

        Args:
            -

        Returns:
            clPCI value
        """
        return self.clPCI

    def set_unique_links_between_nodes(self,unique_links):
        """
        Description: Set unique links between nodes participate xPCI for this node

        Args:
            unique_links

        Returns:
            -
        """
        self.unique_links = unique_links

    def remove_duplicate(self,input_list):
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
    
    def find_N2_or_N3_of_u(self,nodes,neighborhood):
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

    def get_N2_of_u(self):
        """
        Description: Return two hopes away neighbors of this node

        Args:
            -

        Returns:
            N2_of_u
        """
        return self.N2_of_u
    
    def get_N3_of_u(self):
        """
        Description: Return three hopes away neighbors of this node

        Args:
            -

        Returns:
            N3_of_u
        """
        return self.N3_of_u
    
    def get_node_dominators(self):
        """
        Description: Return dominators of specific node

        Args:
            -

        Returns:
            dominators
        """
        return self.dominators
    
    def find_all_nodes_to_3hops(self):
        """
        Description: Create a list with all nodes 3-hop away from each node in network

        Args:
            start_node (String): Name of specific node

        Returns:
            N2_of_u
        """
        self.all_3hop_nodes = []
        self.all_3hop_nodes = self.N_of_u + self.N2_of_u + self.N3_of_u

    def get_all_nodes_to_3hop(self):
        """
        Description: Return a list with all nodes 3-hop away from this node

        Args:
            -

        Returns:
            all_3hop_nodes
        """
        return self.all_3hop_nodes

    def get_dominators(self):
        return self.dominators

    def find_Nu_PCIs(self,dict_of_objects,pci):
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
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_node_degree()))
                elif pci == "sl":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_localPCI()))
                elif pci == "la":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_laPCI()))
                elif pci == "al":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_alPCI()))
                elif pci == "ml":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_mlPCI()))
                elif pci == "ls":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_lsPCI()))
                elif pci == "x":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_xPCI()))
                elif pci == "cl":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_clPCI()))
                elif pci == "new":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_weight()))
        self.Nu_xPCIs_list.sort(key=lambda tup: tup[1],reverse=True)
    
    def check_for_dominator(self,dict_of_objects):
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

    def find_next_dominators(self,node_obj,next_dominators_dict):
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
                neighbor_obj = dict_of_objects[neighbor]
                if neighbor not in next_dominators_dict:
                    next_dominators_dict[neighbor] = 1
                else:
                    next_dominators_dict[neighbor] += 1
        return next_dominators_dict

    def node_decision(self,args):
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
                if neighbor in connected_dominating_set.keys():
                    if dict_of_objects[neighbor] not in self.dominators:
                        self.dominators.append(dict_of_objects[neighbor])
            if len(self.dominators) < int(args.m):
                if self.name not in connected_dominating_set.keys():
                    connected_dominating_set[self.name] = 1
                else:
                    connected_dominating_set[self.name] += 1
            else:
                if args.pci:
                    list_of_dominatees.append((self.name,metrics_dict[args.pci]))
                else:
                    list_of_dominatees.append((self.name,metrics_dict["cl"]))

    def find_number_of_dominatees(self):
        """
        Description: Find the number of dominateesof every node

        Args:
            args (obj): An object with all arguments of user

        Returns:
            -
        """
        for neighbor in self.N_of_u:
            if neighbor not in connected_dominating_set.keys():
                self.number_of_dominatees += 1

    def construct_m_value(self,args):
        m = 0
        if args.m:
            m = int(args.m)
        else:
            m = 1
        return m

    def find_dominator(self,dict_of_objects,args):
        """
        Description: Find dominator of node

        Args:
            -

        Returns:
            -
        """
        m = self.construct_m_value(args)

        for i in range(m):
            has_dominator = False
            for node in connected_dominating_set:
                node_obj = dict_of_objects[node]
                if self.name in node_obj.get_N_of_u():
                    if node_obj not in self.dominators:
                        self.dominators.append(node_obj)
                        has_dominator = True
                        break

            self.Nu_xPCIs_list.sort(key=lambda x: x[1],reverse=True)
            if self.Nu_xPCIs_list[i][0] in connected_dominating_set.keys():
                connected_dominating_set[self.Nu_xPCIs_list[i][0]] += 1
            else:
                connected_dominating_set[self.Nu_xPCIs_list[i][0]] = 1

            if dict_of_objects[self.Nu_xPCIs_list[i][0]] not in self.dominators:
                self.dominators.append(dict_of_objects[self.Nu_xPCIs_list[i][0]])

    def all_2_hop_has_dominator(self):
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
                if neighbor in connected_dominating_set.keys() and neighbor in self.N_of_u:
                    has_dominator = True
            if not has_dominator:
                return False
        return True

    def add_node_in_CDS(self,algorithm):
        """
        Description: Check if exists node of N2 of u without dominator as neighbor
                     and if so add as dominator node of N of u this with largest xPCI
                     covers at least one new node in N2 of u.

        Args:
            -

        Returns:
            -
        """
        self.Nu_xPCIs_list.sort(key=lambda x: x[1],reverse=True)
        if not self.all_2_hop_has_dominator():
            for node in self.Nu_xPCIs_list:
                nodeObj = dict_of_objects[node[0]]
                if self.all_2_hop_has_dominator():
                    break
                for _2_hop_neighbor in nodeObj.get_N_of_u():
                    if _2_hop_neighbor in self.N2_of_u:
                        _2_hop_neighborObj = dict_of_objects[_2_hop_neighbor]
                        if nodeObj.get_name() not in connected_dominating_set.keys():
                            connected_dominating_set[nodeObj.get_name()] = 1
                        else:
                            connected_dominating_set[nodeObj.get_name()] += 1
                        if nodeObj not in _2_hop_neighborObj.dominators:
                            _2_hop_neighborObj.dominators.append(nodeObj)
                            if nodeObj not in self.dominators:
                                self.dominators.append(nodeObj)
                            break

    def print_number_of_dominators(self):
        """
        Description: Print the number of dominators for specific node

        Args:
            -

        Returns:
            -
        """
        if self.name not in connected_dominating_set.keys():
            print "Number of dominators for node with name {} is {}".format(self.name,len(self.dominators)) + " and list of names is: [%s]"%", ".join([a.get_name() for a in self.dominators])
        else:
            print "Node with name {} is dominator and number of dominators for this node is {}".format(self.name,len(self.dominators)) + " and list of names is: [%s]"%", ".join([a.get_name() for a in self.dominators])
    
    def __str__(self):
        """
        Description: Change str representation of node object

        Args:
            -

        Returns:
            New representation of str
        """
        string_obj = "Name of node is: " + str(self.name) + "\n" + "Layer of node is: " + str(self.layer) + "\n" + "Intra-layer links are: " + str(self.intralinks) + "\n" + "Inter-layer links are: " + str(self.interlinks) + "\n" + "N(u) is: " + str(self.N_of_u) + "\n" + "N2(u) is: " + str(self.N2_of_u) + "\n" + "xPCI is: " + str(self.xPCI_value) + "\n" + "Unique links are: " + str(self.unique_links) + "\n"
        return string_obj