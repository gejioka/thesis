import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import sys

milcom_results = "../milcom_results.txt"
thesis_results = "../my_results.txt"

def get_results_list(results,n):
    """
    Description: Get a list with all results of algorithms

    Args:
        results(string): A path for a file with the results
        n(int): An integer which is the number of layers
    Returns:
        results_list
    """
    results_list = [0]*n

    with open(results,"r") as f:
        for line in f:
            try:
                results_list[int(line.split(" ")[0])] += (line.replace("\n","").split(" ")[1],)
            except Exception as err:
                results_list[int(line.split(" ")[0])] = (line.replace("\n","").split(" ")[1],)
    return results_list

def plot_results(milcom_results_list,thesis_results_list,layer):
    """
    Description: Plot results for two different algorithms.
                 For MILCOM and THESIS algorithm
    Args:
        milcom_results(list): A list with milcom results
        thesis_results(list): A list with thesis results
        layer(int): An integer with the name of layer
    Returns:
        -
    """
    fig, axs = plt.subplots(len(milcom_results_list[layer]), sharex=True, sharey=True)
    st = fig.suptitle("Size of CDS per layer", fontsize="x-large")
    
    fig.text(0.5, 0.04, "Input Files", ha="center")
    fig.text(0.04, 0.5, "CDS", va="center", rotation="vertical")

    
    # fig = plt.figure()
    # ax = plt.axes()

    # plt.plot([i for i in range(len(milcom_results_list[layer]))],milcom_results_list[layer],label="MILCOM")
    # plt.plot([i for i in range(len(thesis_results_list[layer]))],thesis_results_list[layer],label="THESIS")

    # plt.legend()
    # plt.show()

def main():
    milcom_results_list = get_results_list(milcom_results,4)
    thesis_results_list = get_results_list(thesis_results,4)

    plot_results(milcom_results_list,thesis_results_list,3)

if __name__=="__main__":
    main()
    sys.exit(1)
