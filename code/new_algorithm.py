#from node import *

# Initial state O(nm)
for all nodes in network:
    calculate betweeness centrality
    set a weight for betweeness centrality
    calculate PCI
    set a weight for PCI
    calculate mlPCI
    set a weight for mlPCI

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
