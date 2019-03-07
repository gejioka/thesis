from global_variables import *
from node import *
import time
import sys

def parser(user_input):
    """
    Description: Parse a file represents a network and create the first structure for this

    Args:
        -

    Returns:
        -
    """
    if len(sys.argv) < 2:
        print "Network parser takes exactly 2 arguments (" + str(len(sys.argv)) + " given)" 
        exit(1)

    line_number = 0     # A variable for number of line in file
    start_time = time.time()
    try:
        filename = sys.argv[1]
        with open(filename,"r") as f:
            nodes = {}
            number_of_nodes     = 0
            number_of_layers    = 0 
            for line in f:
                item = line.rstrip().split("\t")
                # Parse all different types of lines in file
                if line_number == 0:
                    number_of_nodes = item[0]
                    print "Number of nodes is:", item[0]
                elif line_number == 1:
                    number_of_layers = item[0]
                    print "Number of layers is:", item[0]
                elif line_number == 2:
                    print "Names of columns are: " + str(item[0]) + " " + str(item[1]) + " " + str(item[2]) + " " + str(item[3]) + " " + str(item[4]) + " " + str(item[5]) + " "
                    print "\nProcess 1 of 3"
                else:
                    if item[2] not in nodes:
                        nodes[item[2]] = {}
                        nodes[item[2]]["layer"] = item[0]
                        nodes[item[2]]["intralinks"] = []
                        nodes[item[2]]["interlinks"] = {}

                    if item[0] == item[1]:
                        nodes[item[2]]["intralinks"].append(item[3])
                    else:
                        try:
                            nodes[item[2]]["interlinks"][int(item[1])].append(item[3])
                        except:
                            nodes[item[2]]["interlinks"][int(item[1])] = []
                            nodes[item[2]]["interlinks"][int(item[1])].append(item[3])

                line_number += 1
            end_time = time.time()
            print "Time running process 1:", end_time-start_time
            
            print "Process 2 of 3"
            start_time = time.time()
            dict_of_objects = create_objects_of_nodes(nodes,user_input)
            end_time = time.time()
            print "Time running process 1:", end_time-start_time
            
            # Release nodes dictionary
            nodes = None
    except Exception as err:
        print err
        exit(1)