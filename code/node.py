from __future__ import division
import math
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

    def find_N2_of_u(self,nodes):
        """
        Description: Find N2(u) where u is specific node

        Args:
            nodes (dictionary): A dictionary with all nodes

        Returns:
            N2(u)
        """
        self.N2_of_u = []
        for neighbor in self.N_of_u:
            for node in nodes[neighbor]["intralinks"]:
                if node not in self.N2_of_u:
                    self.N2_of_u.append(node)
            for node in nodes[neighbor]["interlinks"]:
                self.N2_of_u = self.N2_of_u + nodes[neighbor]["interlinks"][node]
            self.N2_of_u = self.remove_duplicate(self.N2_of_u)
            try:
                self.N2_of_u.remove(self.name)
            except Exception:
                pass
            self.N2_of_u = [x for x in self.N2_of_u if x not in self.N_of_u]
        return self.N2_of_u
    
    def get_N2_of_u(self):
        """
        Description: Return two hopes away neighbors of this node

        Args:
            -

        Returns:
            N2_of_u
        """
        return self.N2_of_u

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
                if pci == "x":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_xPCI()))
                elif pci == "cl":
                    self.Nu_xPCIs_list.append((node_obj.get_name(),node_obj.get_clPCI()))
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

    def find_dominator(self,dict_of_objects):
        """
        Description: Find dominator of node

        Args:
            -

        Returns:
            -
        """
        dominator = self.check_for_dominator(dict_of_objects)
        if self.Nu_xPCIs_list[0][0] in connected_dominating_set: 
            connected_dominating_set[self.Nu_xPCIs_list[0][0]] += 1
        else:
            has_dominator = False
            for node in connected_dominating_set:
                node_obj = dict_of_objects[node]
                if self.name in node_obj.get_N_of_u():
                    has_dominator = True
                    break
            
            if not has_dominator:
                connected_dominating_set[self.Nu_xPCIs_list[0][0]] = 1
    
    def add_node_in_CDS(self):
        """
        Description: Check if exists node of N2 of u without dominator as neighbor
                     and if so add as dominator node of N of u this with largest xPCI
                     covers at least one new node in N2 of u.

        Args:
            -

        Returns:
            -
        """
        # A list with all nodes which doesn't connect with some dominator node
        temp_nodes_list = []

        has_dominator = False
        for item in self.N2_of_u:
            node_obj = dict_of_objects[item]
            for neighbor in node_obj.N_of_u:
                if neighbor in connected_dominating_set:
                    has_dominator = True
            if not has_dominator:
                temp_nodes_list.append(item)
        
        for node in self.Nu_xPCIs_list:
            node_obj = dict_of_objects[node[0]]
            if list(set(node_obj.get_N_of_u()) & set(temp_nodes_list)):
                connected_dominating_set[node_obj.get_name()] = 1
                break

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