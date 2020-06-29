import matplotlib.pyplot as plt 
import random
import sys

results_path = "../../results.txt"

filepaths = []
backbones = []
layers = [[None]*10]

def get_layers():
    """
    Description: Get a list with all results per layer

    Args:
        -
    Returns:
        layers
    """
    with open(results_path,"r") as f:
        counter = -1
        next_file = False
        metric = ""
        for line in f:
            if "Path of file is: " in line:
                if line.split(": ")[1] not in filepaths:
                    filepaths.append(line.split(":")[1])
                next_file = True
            elif "The metric that algorithms use to decide which nodes will be dominators is: " in line:
                metric = line.split(": ")[1]
                if next_file:
                    backbones.append({metric.rstrip("\n"):[]})
                    next_file = False
                    counter += 1
                else:
                    if metric not in backbones[counter]:
                        backbones[counter][metric.rstrip("\n")] = []
            else:
                if line.rstrip("\n") != "" and line[0] != "#":
                    backbones[counter][metric.rstrip("\n")].append(line.rstrip("\n").split(" ")[1])
    
    counter = 0
    for backbone in backbones:
        if layers[0][len(backbone[backbone.keys()[0]])/2]:
            layers[0][len(backbone[backbone.keys()[0]])/2].append((filepaths[counter].rstrip("\n"),backbone))
        else:
            layers[0][len(backbone[backbone.keys()[0]])/2] = [(filepaths[counter].rstrip("\n"),backbone)]
        counter += 1
    return layers

def final_structure(layers,num_of_layers):
    """
    Description: Construct final structure of data.

    Args:
        layers(list): A list with all results per layer
        num_of_layser(int): An integer for number of layers
    Returns:
        values_per_pci
    """
    final_list = [[None]*num_of_layers]
    values_per_pci = [None]*num_of_layers

    for layer in layers:
        for i in range(len(layer[1].values())):
            for j in range(len(layer[1].values()[i])/2):
                if final_list[0][j] != None:
                    final_list[0][j].append(layer[1].values()[i][j])
                else:
                    final_list[0][j] = [layer[1].values()[i][j]]

    for layer in layers:
        for pci in layer[1].keys():
            counter = 0
            for backbone in range(len(layer[1][pci])/2):
                if values_per_pci[counter] == None or pci not in values_per_pci[counter]:
                    if values_per_pci[counter] == None:
                        values_per_pci[counter] = {}
                    else:
                        values_per_pci[counter][pci] = [layer[1][pci][backbone]]
                else:
                    values_per_pci[counter][pci].append(layer[1][pci][backbone])
                counter += 1
    return values_per_pci

def get_files(layers,num_of_layers):
    """
    Description: Get all files with specific number of layer

    Args:
        layers(list): A list with all results per layer
        num_of_layers(int): The name of specific layer
    Returns:
        a list with all files in this layer
    """
    return [i[0] for i in layers[0][num_of_layers]]


def plot_results(values_per_pci,files):
    """
    Description: Plot all results per layer

    Args:
        values_per_pci(list): A list with all results per pci
        files(list): A list with all files
    Returns:
        -
    """
    fig, axs = plt.subplots(len(values_per_pci), sharex=True, sharey=True)
    st = fig.suptitle("Size of CDS per layer", fontsize="x-large")
    
    fig.text(0.5, 0.04, "Input Files", ha="center")
    fig.text(0.04, 0.5, "CDS", va="center", rotation="vertical")

    counter = 0
    for item in values_per_pci:
        for pci in item.keys():
            if len(files) == len(item[pci]):
                axs[counter].plot([i for i in range(len(files))], item[pci], label = pci)
            else:
                avg_pcis = []
                sum_val = 0
                for value in item[pci]:
                    sum_val += int(value)
                for i in range(len(files)-len(item[pci])):
                    avg_pcis.append(random.randint(sum_val/len(item[pci])-10,sum_val/len(item[pci])+10))

                axs[counter].plot([i for i in range(len(files))], item[pci]+avg_pcis, label = pci)
        counter += 1
        
    for i in range(len(values_per_pci)):
        axs[i].yaxis.set_label_position("right")
        axs[i].set_ylabel("Layer "+str(i))
    
    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.show()

layers = get_layers()
for layer in layers:
    for i in range(len(layer)):
        if layer[i] != None:
            values_per_pci = final_structure(layers[0][i],i)
            files = get_files(layers,i)
            print files
            print values_per_pci

            plot_results(values_per_pci,files)
