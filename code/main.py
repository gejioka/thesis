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
        parser.error("Need to add an input network")
        sys.exit(1)
    else:
        if not os.path.isfile(args.path):
            parser.error("Invalid input network. This file doesn't exist")
            sys.exit(1)
    if not args.algorithm:
        parser.error("Need to add an input algorithm")
        sys.exit(1)
    else:
        if not (args.algorithm == "1" or args.algorithm == "2"):
            parser.error("Invalid input algorithm. This algorithm doesn't exist")
            sys.exit(1)
    if args.pci not in ["cl","x","new","la","degree"]:
        parser.error("Invalid PCI. This PCI code doesn't exist")
        sys.exit(1)
    if args.log:
        if args.logLevel.upper() not in [a.upper() for a in LEVELS.keys()]:
            parser.error("There in no log level {}. The list with all log levels is {}".format(args.logLevel.upper(),[name.upper() for name,obj in LEVELS.iteritems()]))
            sys.exit(1)
    else:
        if args.logLevel:
            parser.error("Cannot pass level argument without enable logging.")
            sys.exit(1)

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
    parser.add_argument("-lv", "--level", help="An argument for log level", \
        action="store", dest="logLevel", default=False)
    args = parser.parse_args()
    
    check_arguments(parser,args)

    return args

if __name__=="__main__":
    args = get_args()

    testing = False
    try:
        if args.testing:
            testing = True
    except Exception:
        pass
    
    if args.log:
        configure_logging(args)
    
    if args.log:
        # Create two format strings 
        alg = "milcom" if args.algorithm == 1 else "new"
        backbone = "CDS" if args.cds else ("MCDS" if args.mcds else "RMCDS")    
        
        # Write message
        write_message(args,"[!] Start running {} algorithm to create {} as backbone and path for input file is {}\n".format(alg,backbone,args.path),"INFO")

    # Get user input and check if this input is correct
    user_input = int(args.algorithm)
    if user_input not in [1,2]:
        write_message(args,"Wrong input. Type 1 for milcom or 2 for new algorithm.","ERROR")
        sys.exit(1)

    pci = create_structures(user_input,args)
    if user_input == 1:
        milcom_algorithm(pci,user_input,args)
    elif user_input == 2:
        new_algorithm(user_input,args)

    # Write results to file
    if testing:
        testing_function(args)