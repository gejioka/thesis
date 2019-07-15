from network_tools import *
import sys
import os
import re

def testing_function(args):
    _50_nodes_total         = "/home/giorgos/Documents/University/git_projects/thesis/code/root/50_nodes_total/"
    _degree_experiments     = "/home/giorgos/Documents/University/git_projects/thesis/code/root/degree_experiments/"
    _diameter_experiments   = "/home/giorgos/Documents/University/git_projects/thesis/code/root/diameter_experiments/"
    _layer_experiments      = "/home/giorgos/Documents/University/git_projects/thesis/code/root/layer_experiments/"

    # This code is for testing the two algorithms
    result = re.split('_DM|_D',args.path)[1].split("_")[0]
    if not result.isdigit():
        result = re.split('_DM|_D',args.path)[2].split("_")[0]
    
    string_to_write = ""
    if "50 nodes total" in args.path:
        if os.path.isfile(_50_nodes_total+"_"+str(result)+"_degree.txt"):
            try:
                with open(_50_nodes_total+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_50_nodes_total+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
    elif "Layers Experiments" in args.path:
        if os.path.isfile(_layer_experiments+"_"+str(result)+"_degree.txt"):
            try:
                with open(_layer_experiments+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_layer_experiments+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
    elif "Degree Experiments" in args.path:
        if os.path.isfile(_degree_experiments+"_"+str(result)+"_degree.txt"):
            try:
                with open(_degree_experiments+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_degree_experiments+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
    elif "Diameter Experiments" in args.path:
        if os.path.isfile(_diameter_experiments+"_"+str(result)+"_degree.txt"):
            try:
                with open(_diameter_experiments+"_"+str(result)+"_degree.txt", "a") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
        else:
            try:
                with open(_diameter_experiments+"_"+str(result)+"_degree.txt", "w") as f:
                    if int(args.algorithm) == 1:
                        if all_dominees_have_dominators():
                            string_to_write = "milcom algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "milcom algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                    else:
                        if all_dominees_have_dominators():
                            string_to_write = "new algorithm created MCDS with {} number of nodes\n".format(len(connected_dominating_set))
                        else:
                            string_to_write = "new algorithm created MCDS with - number of nodes\n"
                        f.write(string_to_write)
                        f.write("\n")
            except IOError as err:
                write_message(args,err,"ERROR")
                sys.exit(1)
            except Exception as err:
                write_message(args,err,"ERROR")
                sys.exit(1)