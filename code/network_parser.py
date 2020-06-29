from global_variables import *
import structures
from node import *
from log import *
import time
import sys

def parser(user_input,args):
    """
    Description: Parse a file represents a network and create the first structure for this

    Args:
        -

    Returns:
        -
    """
    if len(sys.argv) < 2:
        write_message(args,"Network parser takes exactly 2 arguments (" + str(len(sys.argv)) + " given)","ERROR")
        exit(1)

    line_number = 0     # A variable for number of line in file
    start_time = time.time()
    try:
        filename = args.path
        with open(filename,"r") as f:
            nodes = {}
            number_of_nodes     = 0
            number_of_layers    = 0 
            for line in f:
                item = line.rstrip().split("\t")
                # Parse all different types of lines in file
                if line_number == 0:
                    number_of_nodes = item[0]
                    write_message(args,"Number of nodes is: {}".format(item[0]),"INFO")
                elif line_number == 1:
                    number_of_layers = item[0]
                    write_message(args,"Number of layers is: {}".format(item[0]),"INFO")
                elif line_number == 2:
                    write_message(args,"Names of columns are: " + str(item[0]) + " " + str(item[1]) + " " + str(item[2]) + " " + str(item[3]) + " " + str(item[4]) + " " + str(item[5]) + " ","INFO")
                    if args.time:
                        if args.mcds:
                            write_process_message(args,1,True)
                        else:
                            write_process_message(args,1,False)
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
            if args.time:
                end_time = time.time()
                write_message(args,"Time running process 1: {}".format(end_time-start_time),"INFO",True)
            if args.time:
                if args.mcds:
                    write_process_message(args,2,True)
                else:
                    write_process_message(args,2,False)
                start_time = time.time()
            dict_of_objects = structures.create_objects_of_nodes(nodes,user_input,args)
            if args.time:
                end_time = time.time()
                write_message(args,"Time running process 2: {}".format(end_time-start_time),"INFO",True)
            
            # Release nodes dictionary
            nodes = None
    except IOError as err:
        write_message(args,err,"ERROR")
        sys.exit(1)
    except Exception as err:
        write_message(args,err,"ERROR")