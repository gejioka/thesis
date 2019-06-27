import os
import re

# Root folder of all input networks
_root_folder = "/home/giorgos/Documents/University/subjects/thesis/network_samples/EXPERIMENT_NETWORKS_L-CSS"

# Create all different paths exists under root folder
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(_root_folder):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

# Run MILCOM and NEW algorithms for same input
counter = 0
for filename in listOfFiles:
    os.system('python ../create_ml.py -fp "%s" -a "%s" --testing' % (filename,"1"))
    os.system('python ../create_ml.py -fp "%s" -a "%s" --testing' % (filename,"2"))
    counter += 1
    if counter == 4:
        break
