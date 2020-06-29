from network_tools import *
from metrics import *
from os import listdir
import shutil
import sys
import os
import re

_root_folder = "Experiment Networks"

def append_file_to_file(src_file,dest_file):
    file_data=""
    with open(src_file,"r") as f:
        for line in f:
            file_data += line
    with open(dest_file,"a") as f:
        f.write(file_data)
        f.write("\n")
        f.flush()
        os.fsync(f)

def find_attempt(filename):
    return filename[filename.find("NETWORKS_REPOSITORY_")+20]



def testing_function(args):
    metrics_dict = {"degree"        : "Degree",
                        "cl"        : "Cross-Layer PCI",
                        "x"         : "Exhaustive PCI",
                        "new"       : "New PCI",
                        "la"        : "Layer-Agnostic PCI",
                        "al"        : "All-Layer PCI",
                        "ml"        : "Minimal-Layer PCI",
                        "ls"        : "Layer-Symmetric PCI",
                        "sl"        : "Single-Layer PCI"}
    
    string_to_write = ""
    format_string = "CDS" if args.cds else ("MCDS" if args.mcds else "RMCDS")
    if "Degree" in args.path:
        try:
            with open(_root_folder+"/"+"Degree"+"/STATISTICS/Alg_2_Attempt_"+find_attempt(args.path)+"_Stat."+args.file_id, "w") as f:
                if args.cds:
                    if args.pci == "cl":
                        f.write("Path of file is: "+args.path+"\n")
                        f.flush()
                    f.write("The metric that algorithms use to decide which nodes will be dominators is: {}\n".format(metrics_dict[args.pci]))
                    f.flush()
                if all_dominees_have_dominators():
                    list_of_layers = dominators_per_layer(connected_dominating_set)
                    for i in range(len(list_of_layers)):
                        string_to_write += str(i) + " " + str(list_of_layers[i]) + "\n"
                f.write(string_to_write)
                f.flush()
                os.fsync(f)
            if args.merge:
                with open("../../tools/path","w") as f:
                    f.write(_root_folder+"/"+"Degree/STATISTICS/")
                    f.flush()
                    os.fsync(f)
        except IOError as err:
            write_message(args,err,"ERROR")
            sys.exit(1) 
        except Exception as err:
            print err
            write_message(args,err,"ERROR")
            sys.exit(1)
    elif "Layers" in args.path:
        try:
            with open(_root_folder+"/"+"Layers/STATISTICS/Alg_2_Attempt_"+find_attempt(args.path)+"_Stat."+args.file_id, "w") as f:
                if args.cds:
                    if args.pci == "cl":
                        f.write("Path of file is: "+args.path+"\n")
                        f.flush()
                    f.write("The metric that algorithms use to decide which nodes will be dominators is: {}\n".format(metrics_dict[args.pci]))
                    f.flush()
                if all_dominees_have_dominators():
                    list_of_layers = dominators_per_layer(connected_dominating_set)
                    for i in range(len(list_of_layers)):
                        string_to_write += str(i) + " " + str(list_of_layers[i]) + "\n"
                f.write(string_to_write)
                f.flush()
                os.fsync(f)
            if args.merge:
                with open("../../tools/path","w") as f:
                    f.write(_root_folder+"/"+"Layers/STATISTICS/")
                    f.flush()
                    os.fsync(f)
        except IOError as err:
            write_message(args,err,"ERROR")
            sys.exit(1)
        except Exception as err:
            write_message(args,err,"ERROR")
            sys.exit(1)
    elif "Diameter" in args.path:
        try:
            with open(_root_folder+"/"+"Diameter/STATISTICS/Alg_2_Attempt_"+find_attempt(args.path)+"_Stat."+args.file_id, "w") as f:
                if args.cds:
                    if args.pci == "cl":
                        f.write("Path of file is: "+args.path+"\n")
                        f.flush()
                    f.write("The metric that algorithms use to decide which nodes will be dominators is: {}\n".format(metrics_dict[args.pci]))
                    f.flush()
                if all_dominees_have_dominators():
                    list_of_layers = dominators_per_layer(connected_dominating_set)
                    for i in range(len(list_of_layers)):
                        string_to_write += str(i) + " " + str(list_of_layers[i]) + "\n"
                f.write(string_to_write)
                f.flush()
                os.fsync(f)
            if args.merge:
                with open("../../tools/path","w") as f:
                    f.write(_root_folder+"/"+"Diameter/STATISTICS/")
                    f.flush()
                    os.fsync(f)
        except IOError as err:
            write_message(args,err,"ERROR")
            sys.exit(1)
        except Exception as err:
            write_message(args,err,"ERROR")
            sys.exit(1)
    elif "Percentage" in args.path:
        try:
            with open(_root_folder+"/"+"Percentage/STATISTICS/Alg_2_Attempt_"+find_attempt(args.path)+"_Stat."+args.file_id, "w") as f:
                if args.cds:
                    if args.pci == "cl":
                        f.write("Path of file is: "+args.path+"\n")
                        f.flush()
                    f.write("The metric that algorithms use to decide which nodes will be dominators is: {}\n".format(metrics_dict[args.pci]))
                    f.flush()
                if all_dominees_have_dominators():
                    list_of_layers = dominators_per_layer(connected_dominating_set)
                    for i in range(len(list_of_layers)):
                        string_to_write += str(i) + " " + str(list_of_layers[i]) + "\n"
                f.write(string_to_write)
                f.flush()
                os.fsync(f)
            if args.merge:
                with open("../../tools/path","w") as f:
                    f.write(_root_folder+"/"+"Percentage/STATISTICS/")
                    f.flush()
                    os.fsync(f)
        except IOError as err:
            write_message(args,err,"ERROR")
            sys.exit(1)
        except Exception as err:
            write_message(args,err,"ERROR")
            sys.exit(1)