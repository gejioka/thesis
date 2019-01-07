Main Program:
    Run:    python create_ml.py <path to network> <pci algorithm> (optional)
    
    Can run python create_ml.py --help to see pci arguments usage

Generate Networks:
    Run:    python generate_network_files.py <type of network> (optional)

    Can run python generate_network_files.py --help to see all options

Generate Network example:
    python generate_network_files.py small
    Create a small network file

Main Program example:
    python create_ml.py networks/static_network.txt cl
    Find and print CDS calculated by cross-layer PCI

networks folder:
    Include a static_network.txt file which represent the network of 
    the MILCOM paper.
    If user want to create and other random networks, program store
    .txt files to networks folder.

