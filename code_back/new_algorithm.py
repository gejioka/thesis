#from node import *

# Initial state O(nm)
for all nodes in network:
    #calculate betweeness centrality
    #set a weight for betweeness centrality
    
    # How important is node for it's layer
    calculate PCI
    
    # How important is node for other layers
    calculate xPCI per layer
    for all neighbors per layer:
        xPCI += neighborPCI*((number of layers node has neighbors)/(neighbors per layer))
    
    # How connected are neighbors of interlayer neighbors of node
    nodes_connecticity = 0
    for all interlayer nodes:
        nodes_connecticity += number of layers every neighbor has neighbors

    # Calculate total weight of node
    total_weight_of_node = 0.4*PCI + 0.5*xPCI + 0.1*nodes_connecticity

# 1st Main state (Create CDS) O(nmlog(m))
i = 0
while DS is not connected:
    for all nodes in network:
        sort neighbors in descending order by total weight
        add as candidate dominator the i node
    connected = check if DS is connected
    i += 1

# 2nd Main state (Create MCDS)
sort CDS in ascending order by total weight
while CDS is connected:
    remove temporarily first node from CDS
    check if CDS is connected without this node
    if DS is connected:
        remove first node
