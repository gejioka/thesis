import matplotlib.pyplot as plt
from itertools import groupby
import numpy as np
import pandas as pd 
import random
import sys
import re

# Path of results files
new_results_path = "../results/new_results.txt"
robust_results_path = "../results/robust_results.txt"

### Global variables ###
filepaths = []
backbones = []

robust_results = [[None]*10]
new_results = [[None]*10]
#########################

def get_next_limits(data_list,line_number):
    """
    Description: Return a tuple with the next limits (start_point, end_point) of a list

    Args:
        data_list (list): A list with all results of a specific algorithm
        line_number(int): A variable that tells you from where to start searching the next limits

    Returns:
        next_limits
    """
    return [i+line_number for i, s in enumerate(data_list[line_number:]) if '.txt' in s][:2]

def find_layers_of_file(data_list,results_path,algorithm,line_number,limits):
    """
    Description: Find the number of layers of the input network

    Args:
        data_list (list): A list with all results of a specific algorithm
        results_path(string): The path of the results for a specific algorithm
        line_number(int): A variable that tells you where to start searching for the next input file in the results file
        limits(tuple): A tuple with the limits of the specific chunk (In this implementation the chunk is all the results of a specific input file in the results file)
    Returns:
        number_of_layers
    """
    contains_digit = map(str.isdigit, [i.replace(" ","").strip() for i in data_list[limits[0]:limits[1]]])
    grouped_L = [item for item in [(k, sum(1 for i in g)) for k,g in groupby(contains_digit)] if item[0] == True][0]
    
    return grouped_L[1]/2 if algorithm == "new" else grouped_L[1]

def find_keys(data_list,limits,alg):
    """
    Description: Find the number and the names of keys for a specific algorithm

    Args:
        data_list (list): A list with all results of a specific algorithm
        limits(tuple): A tuple with the limits of the specific chunk (In this implementation the chunk is all the results of a specific input file in the results file)
        alg(string): The name of the algorithm 

    Returns:
        keys
    """
    if alg == "robust":
        return re.findall("..","".join([i.split(": ")[1].strip() for i in data_list[limits[0]:limits[1]] if any(j in i for j in ["k: ","m: "])]))
    elif alg == "new":
        return [i.split(": ")[1].strip() for i in data_list[limits[0]:limits[1]] if "PCI" in i]

def create_structure(results,algorithm,number_of_layers,layer,key):
    """
    Description: Create the structure with all results for all input files for a specific algorithm.

    Args:
        results (dict): A dictionary to store the final structure
        algorithm(string): The name of the algorithm
        number_of_layers(int): A variable that tells you how many layers exists in this input file
        layer(int): A variable that tells you where belong the specific input file. 
        key(string): A variable that tells you the key for the specific input file. (The keys are:  k:1  m:1
                                                                                                    k:1  m:2
                                                                                                    k:1  m:3
                                                                                                    k:2  m:1
                                                                                                    k:2  m:2
                                                                                                    k:2  m:3
                                                                                                    k:3  m:1
                                                                                                    k:3  m:2
                                                                                                    k:3  m:3) 

    Returns:
        -
    """
    if results[0][number_of_layers] == None:
        results[0][number_of_layers] = {}
        results[0][number_of_layers][algorithm] = {}
        
        if algorithm == "new":
            results[0][number_of_layers][algorithm][layer] = {}
            
            results[0][number_of_layers][algorithm][layer]["CDS"] = {}
            results[0][number_of_layers][algorithm][layer]["MCDS"] = {}

        elif algorithm == "robust":
            results[0][number_of_layers][algorithm][key] = {}
            results[0][number_of_layers][algorithm][key][layer] = {}
    else:
        if algorithm == "new":
            if layer not in results[0][number_of_layers][algorithm].keys():
                results[0][number_of_layers][algorithm][layer] = {}
            if "CDS" not in results[0][number_of_layers][algorithm][layer].keys():
                results[0][number_of_layers][algorithm][layer]["CDS"] = {}
            if "MCDS" not in results[0][number_of_layers][algorithm][layer].keys():
                results[0][number_of_layers][algorithm][layer]["MCDS"] = {}
        if algorithm == "robust":
            if key not in results[0][number_of_layers][algorithm].keys():
                results[0][number_of_layers][algorithm][key] = {}
            if layer not in results[0][number_of_layers][algorithm][key].keys():
                results[0][number_of_layers][algorithm][key][layer] = {}

def construct_robust_final_structure(data_list,limits,algorithm,key,layer,backbone,number_of_layers):
    """
    Description: Construct the final structure for results of robust algorithm

    Args:
        data_list (list): A list with all results of a specific algorithm
        limits(tuple): A tuple with the limits of the specific chunk (In this implementation the chunk is all the results of a specific input file in the results file)
        algorithm(string): The name of the algorithm 
        key(string): The variable key contains the k-m pair
        backbone(string): The type of backbone (CDS,MCDS)
        number_of_layers: The number of layers for these files
    Returns:
        -
    """
    next_data = [i.strip() for i in data_list[limits[0]+1:limits[1]-1]]

    try:
        create_structure(robust_results,algorithm,number_of_layers,layer,key)

        index = next_data[0:limits[1]].index([i.strip() for i in next_data[0:limits[1]] if "k: "+str(key[0]) == i.strip()][0])
        next_data = next_data[index+1:limits[1]]
        
        index = next_data[0:limits[1]].index([i.strip() for i in next_data[0:limits[1]] if "m: "+str(key[1]) == i.strip()][0])
        next_data = next_data[index+1:limits[1]]
        
        if backbone == "MCDS":
            index = next_data[index+1:limits[1]].index([i.strip() for i in next_data if "MCDS" in i.strip()][0])
            next_data = next_data[index+1:limits[1]]
        
        if backbone not in robust_results[0][number_of_layers][algorithm][key][layer].keys():
            robust_results[0][number_of_layers][algorithm][key][layer][backbone] = [int(next_data[0:number_of_layers][layer].split(" ")[1])]
        else:
            robust_results[0][number_of_layers][algorithm][key][layer][backbone].append(int(next_data[0:number_of_layers][layer].split(" ")[1]))
    
    except Exception as err:
        print err
    

def construct_new_final_structure(data_list,limits,algorithm,key,layer,number_of_layers):
    """
    Description: Construct the final structure for results of new algorithm

    Args:
        data_list (list): A list with all results of a specific algorithm
        limits(tuple): A tuple with the limits of the specific chunk (In this implementation the chunk is all the results of a specific input file in the results file)
        algorithm(string): The name of the algorithm 
        key(string): The variable key contains the k-m pair
        backbone(string): The type of backbone (CDS,MCDS)
        number_of_layers: The number of layers for these files
    Returns:
        -
    """
    next_data = [i.strip() for i in data_list[limits[0]+1:limits[1]-1]]

    try:
        create_structure(new_results,algorithm,number_of_layers,layer,key)
        next_data = next_data[next_data[0:limits[1]].index([i.strip() for i in next_data[0:limits[1]] if key in i.strip()][0])+1:limits[1]]
        
        if "CDS" not in new_results[0][number_of_layers][algorithm][layer].keys():
            new_results[0][number_of_layers][algorithm][layer]["CDS"] = {}
        if key not in new_results[0][number_of_layers][algorithm][layer]["CDS"].keys():
            new_results[0][number_of_layers][algorithm][layer]["CDS"][key] = [int(next_data[0:number_of_layers][layer].split(" ")[1])]             
        else:
            new_results[0][number_of_layers][algorithm][layer]["CDS"][key].append(int(next_data[0:number_of_layers][layer].split(" ")[1]))
        
        next_data = next_data[number_of_layers:limits[1]]
        
        if "MCDS" not in new_results[0][number_of_layers][algorithm][layer].keys():
            new_results[0][number_of_layers][algorithm][layer]["MCDS"] = {}
        if key not in new_results[0][number_of_layers][algorithm][layer]["MCDS"].keys():
            new_results[0][number_of_layers][algorithm][layer]["MCDS"][key] = [int(next_data[0:number_of_layers][layer].split(" ")[1])]
        else:
            new_results[0][number_of_layers][algorithm][layer]["MCDS"][key].append(int(next_data[0:number_of_layers][layer].split(" ")[1]))
    except Exception as err:
        print err

def init(results_path,alg):
    """
    Description: Initialize and construct the final structure

    Args:
        results_path(string): The path with the results files
        algorithm(string): The name of the algorithm 
    Returns:
        keys
    """
    with open(results_path,"r") as f:
        final_structure = {}

        data_list = f.readlines()
        limits = get_next_limits(data_list,0)
        num_of_layers = find_layers_of_file(data_list,new_results_path,alg,0,limits)
        keys = find_keys(data_list,limits,alg)

        while limits[1] <= len(data_list):
            try:
                for layer in range(num_of_layers):
                    for key in keys:
                        if alg == "robust":
                            construct_robust_final_structure(data_list,limits,alg,key,layer,"CDS",num_of_layers)
                        elif alg == "new":
                            construct_new_final_structure(data_list,limits,alg,key,layer,num_of_layers)

                limits = get_next_limits(data_list,limits[1])
                num_of_layers = find_layers_of_file(data_list,new_results_path,alg,0,limits)
                keys = find_keys(data_list,limits,alg)
            
            except Exception:
                break

        return final_structure

def bar_plot(ax, data, fig=None, colors=None, total_width=0.8, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars
    
    # Iterate over all data
    bars = []
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
        bars.append(bar[0])
    
    if fig != None:
        fig.legend(bars,data.keys(), loc='upper right')
    
    return fig

def get_plot_data(backbone,alg,results):
    """
    Description: Return data to plot

    Args:
        backbone(string): The type of backbone (CDS,MCDS)
        algorithm(string): The name of the algorithm 
        results(dict): A dictionary with all the results
    Returns:
        plot_data
    """
    plot_data = {}
    
    if alg == "new":
        for key in results.keys():
            if key not in plot_data.keys():
                plot_data[key] = {}
            for pci in results[key][backbone].keys():
                if pci not in plot_data[key].keys():
                    plot_data[key][pci] = results[key][backbone][pci]
    elif alg == "robust":
        for key in results.keys():
            for layer in results[key].keys():
                if layer not in plot_data.keys():
                    plot_data[layer] = {}
                plot_data[layer]["k: "+key[0]+", m: "+key[1]] = results[key][layer][backbone]
                    
    return plot_data

def plot_results(alg,res):
    """
    Description: Plot the results for a specific algorithm

    Args:
        algorithm(string): The name of the algorithm 
        results(dict): A dictionary with all the results
    Returns:
        -
    """
    for results in res[0]:
        if results != None:
            plot_data = get_plot_data("CDS",alg,results[alg])
            
            fig, axs = plt.subplots(len(plot_data), sharex=True, sharey=False)
            fig.suptitle("Size of CDS per layer", fontsize="x-large")

            fig.text(0.5, 0.04, "Input Files", ha="center")
            fig.text(0.04, 0.5, "CDS", va="center", rotation="vertical")
            
            counter = 0
            for key in plot_data.keys():
                if counter == 0:
                    fig = bar_plot(axs[counter],plot_data[key],fig)
                else:
                    bar_plot(axs[counter],plot_data[key])
                counter += 1

            for j in range(len(plot_data)):
                axs[j].yaxis.set_label_position("right")
                axs[j].set_ylabel("Layer "+str(j))
                axs[j].locator_params(axis="y",tight=True,nbins=10)
                
            plt.show()

def main():
    # init(new_results_path,"new")
    init(robust_results_path,"robust")
    
    plot_results("new",new_results)
    plot_results("robust",robust_results)
                
if __name__=="__main__":
    main()
    sys.exit(1)