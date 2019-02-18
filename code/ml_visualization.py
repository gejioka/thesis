from pymnet import *
from global_variables import *
from metrics import *
import matplotlib.pyplot as plt

mnet = MultilayerNetwork(aspects=1)

def multilayer_visualization():
    """
    Description: Visualize the multi-layer input network

    Args:
        -

    Returns:
        -
    """
    nodeColorDict = {}      # A dictionary for colors of nodes of network
    for node in list_of_objects:
        for neighbor in node.get_N_of_u():
            neighbor_obj = find_node_obj_by_name(neighbor,list_of_objects)
            if neighbor in [a[0] for a in connected_dominating_set]:
                nodeColorDict[(neighbor_obj.get_name(),neighbor_obj.get_layer())] = "r"                     # Add red color to nodes in CDS otherwise is black by default
            mnet[node.get_name(),node.get_layer()][neighbor_obj.get_name(),neighbor_obj.get_layer()] = 1    # Add all edges between nodes in network
    draw(mnet,nodeColorDict=nodeColorDict,show=True)                                                        # Draw multi-layer network
    plt.show()