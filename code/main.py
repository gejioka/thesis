from metrics import *
from node import *
from global_variables import *
from network_tools import *
from graph import *
from structures import *
from backbone_algorithms import *
from testing import *
from log import *
import networkx as nx
import network_parser as np
import ml_visualization as mlv
import operator
import argparse
import logging
import time
import sys
import ast
import os
import os.path
import re

sys.setrecursionlimit(150000)

def check_arguments(parser,args):
    """
    Description: Check if all arguments exist and are correct

    Args:
        parser(object): An object which parse arguments
        args: A variable with all arguments of user     
    Returns:
        -
    """
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if not args.path:
        parser.error("Need to give an input network")
        sys.exit(1)
    else:
        if not os.path.isfile(args.path):
            parser.error("Invalid input network. This file doesn't exist "+args.path+" "+os.getcwd())
            sys.exit(1)
    if not args.algorithm:
        parser.error("Need to give an input algorithm")
        sys.exit(1)
    else:
        if not (args.algorithm == "1" or args.algorithm == "2" or args.algorithm == "3"):
            parser.error("Invalid input algorithm. This algorithm doesn't exist.\n\t\t1.MILCOM\n\t\t2.NEW\n\t\t3.ROBUST")
            sys.exit(1)
    if args.pci not in ["cl","x","new","la","al","ml","ls","sl","degree"]:
        parser.error("Invalid PCI. This PCI code doesn't exist.\n\t\tcl:\tCross-Layer PCI\n\t\tx:\tExhaustive PCI\
                        \n\t\tnew:\tNew PCI\n\t\tla:\tLayer-agnostic PCI\n\t\tal:\tAll-Layer PCI\n\t\tml:\tMinimal-Layer PCI\n\t\tls:\tLayer-Symetric\n\t\tsl:\tSingle-Layer PCI\
                            \n\t\tdegree:\tDegree of node")
        sys.exit(1)
    if args.store_log and not args.log_file:
        parser.error("Need to define a filename to store log messages.")
        sys.exit(1)
    if args.log:
        if args.logLevel:
            if args.logLevel.upper() not in [a.upper() for a in LEVELS.keys()]:
                parser.error("There in no log level {}. The list with all log levels is {}".format(args.logLevel.upper(),[name.upper() for name,obj in LEVELS.iteritems()]))
                sys.exit(1)
    else:
        if args.logLevel:
            parser.error("Cannot pass level argument without enable logging.")
            sys.exit(1)
    if args.rmcds:
        if int(args.k) <= 0 or int(args.m) <= 0:
            parser.error("k and m numbers must be greater than zero")
            sys.exit(1)

    if not args.tolerance:
        args.tolerance = TOLERANCE

def get_args():
    """
    Description: Create a parser and parse all arguments program needs to run

    Args:
        -
    Returns:
        args
    """
    # Create argument parser
    parser = argparse.ArgumentParser(description="Robust MCDS for multi-layer Ad hoc Networks")
    parser.add_argument("-fp", "--path", help="Path where network has stored", \
        action="store", dest="path", default=False)
    parser.add_argument("-p", "--pci", help="Algorithm which will use program to calculate PCI value",\
         nargs="?", const="cl", type=str, dest="pci", default="cl")
    parser.add_argument("-a", "--algorithm", help="Which algorithm will use program to calculate robust MCDS", \
        action="store", dest="algorithm", default=False)
    parser.add_argument("-k", help="One of two numbers which represent network", \
        action="store", dest="k", default=False)
    parser.add_argument("-m", help="One of two numbers which represent network", \
        action="store", dest="m", default=False)
    parser.add_argument("-i", "--fid", help="An increament integer which append to filename", \
        action="store", dest="file_id", default=False)
    parser.add_argument("-tol", "--tolerance", help="Tolerance between PCI or and centrality selection", \
        action="store", dest="tolerance", default=False)
    parser.add_argument("-n", "--noc", help="An integer tells us the number of logical cores needed to solve input graphs", \
        action="store", dest="cores_num", default=False)
    parser.add_argument("--merge", help="Merge threads files to main file", \
        action="store_true", dest="merge", default=False)
    parser.add_argument("--centrality", help="Add betweeness centrality as an extra metric for every node", \
        action="store_true", dest="centrality", default=False)
    parser.add_argument("--cds", help="Create a connected dominating set for backbone in network", \
        action="store_true", dest="cds", default=False)
    parser.add_argument("--mcds", help="Create a minimum connected dominating set for backbone in network", \
        action="store_true", dest="mcds", default=False)
    parser.add_argument("--rmcds", help="Create a robust minimum connected dominating set for backbone in network", \
        action="store_true", dest="rmcds", default=False)
    parser.add_argument("--testing", help="Test which algorithm is better for each case", \
        action="store_true", dest="testing", default=False)
    parser.add_argument("--plotting", help="Needs or not to plot network", \
        action="store_true", dest="plotting", default=False)
    parser.add_argument("--clock", help="Track algorithm duration", \
        action="store_true", dest="time", default=False)
    parser.add_argument("--log", help="Check if need to add log messages", \
        action="store_true", dest="log", default=False)
    parser.add_argument("--store_log", help="Check if need store log messages to file", \
        action="store_true", dest="store_log", default=False)
    parser.add_argument("-lf", "--log_file", help="File to store logging", \
        action="store", dest="log_file", default=False)
    parser.add_argument("-lv", "--level", help="An argument for log level", \
        action="store", dest="logLevel", default=False)
    args = parser.parse_args()
    
    check_arguments(parser,args)

    return args

def is_testing(args):
    """
    Description: Check if user run testing

    Args:
        args(Object):   A variable with all arguments of user
    Returns:
        testing
    """
    testing = False
    try:
        if args.testing:
            testing = True
    except Exception:
        pass
    return testing

def check_input_algorithm(user_input):
    """
    Description: Check if user gives correct algorithm as input

    Args:
        args(Object):   A variable with algorithm ID
    Returns:
        -
    """
    if user_input not in [1,2,3]:
        write_message(args,"Wrong input. Type 1 for milcom, 2 for new or 3 for robust algorithm.","ERROR")
        sys.exit(1)

def check_log():
    """
    Description: Check if out.txt exists and remove it

    Args:
        -
    Returns:
        -
    """
    try:
        os.remove("../code/out.txt")
    except Exception as err:
        print "An error occured: " + str(err)

if __name__=="__main__":
    args = get_args()
    testing = is_testing(args)
    
    if args.log or args.time:
        configure_logging(args)
    
    if args.log:
        # Create two format strings 
        alg = "milcom" if args.algorithm == 1 else ("new" if args.algorithm == 2 else "robust")
        backbone = "CDS" if args.cds else ("MCDS" if args.mcds else "RMCDS")    
        
        # Write message
        write_message(args,"[!] Start running {} algorithm to create {} as backbone and path for input file is {}\n".format(alg,backbone,args.path),"INFO")

    # Get user input and check if this input is correct
    user_input = int(args.algorithm)
    check_input_algorithm(user_input)

    # Solve problem with one of three algorithms
    pci = create_structures(user_input,args)
    if user_input == 1:
        milcom_algorithm(pci,user_input,args)
    elif user_input == 2:
        new_algorithm(user_input,args)
    elif user_input == 3:
        robust_algorithm(user_input,args)
    
    # Write results to file
    if testing:
        testing_function(args)
