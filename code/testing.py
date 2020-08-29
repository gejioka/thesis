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

def write_results(network_type,backbone_type,args,string_to_write):
    metrics_dict = {"degree"        : "Degree",
                        "cl"        : "Cross-Layer PCI",
                        "x"         : "Exhaustive PCI",
                        "new"       : "New PCI",
                        "la"        : "Layer-Agnostic PCI",
                        "al"        : "All-Layer PCI",
                        "ml"        : "Minimal-Layer PCI",
                        "ls"        : "Layer-Symmetric PCI",
                        "sl"        : "Single-Layer PCI"}

    try:
        with open(_root_folder+"/"+network_type+"/STATISTICS/Alg_2_Attempt_"+find_attempt(args.path)+"_Stat."+args.file_id, "w") as f:
            if args.cds:
                if args.pci == "cl":
                    f.write("Path of file is: "+args.path+"\n")
                    f.fmelush()
                f.write("The metric that algorithms use to decide which nodes will be dominators is: {}\n".format(metrics_dict[args.pci]))
                f.write("Type of backbone created is a {}\n".format(backbone_type))
                if(args.algorithm == "3"):
                    f.write("k: {}\nm: {}\n".format(args.k,args.m))
            else:
                f.write("Type of backbone created is a {}\n".format(backbone_type))
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
                f.write(_root_folder+"/"+network_type+"/STATISTICS/")
                f.flush()
                os.fsync(f)
    except IOError as err:
        write_message(args,err,"ERROR")
        sys.exit(1) 
    except Exception as err:
        write_message(args,err,"ERROR")
        sys.exit(1)

def testing_function(args):
    string_to_write = ""
    backbone_type = "CDS" if args.cds else ("MCDS" if args.mcds else "RMCDS")
    
    if "Degree" in args.path:
        write_results("Degree",backbone_type,args,string_to_write)
    elif "Layers" in args.path:
        write_results("Layers",backbone_type,args,string_to_write)
    elif "Diameter" in args.path:
        write_results("Diameter",backbone_type,args,string_to_write)
    elif "Percentage" in args.path:
        write_results("Percentage",backbone_type,args,string_to_write)