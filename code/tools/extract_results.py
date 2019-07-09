import matplotlib.pyplot as plt
import argparse
import sys
import os

def get_results(filename):
    """
    Description: Extract results of output files for two algorithms and return it

    Args:
        filename(String): The name of specific file
    Returns:
        milcom_results
        newlalg_results
    """
    try:
        with open(filename,"r") as f:
            for line in f:
                if "milcom algorithm" in line:
                    milcom_results.append(int(line.split(" ")[5]))
                elif "new algorithm" in line:
                    newalg_results.append(int(line.split(" ")[5]))
    except IOError as err:
        print err
        sys.exit(1)

    return milcom_results,newalg_results

# Root folder to extract results of algorithms
_root_folder = "/home/giorgos/Documents/University/git_projects/thesis/code/root/50_nodes_total/"

# Create parser for arguments of program
parser = argparse.ArgumentParser(description="Extract results of two algorithms")
parser.add_argument("-p", "--path", help="Path where output has stored", \
    action="store", dest="path", default=False)
parser.add_argument("--plotting", help="Create plot with all data under root directory", \
        action="store_true", dest="plot", default=False)
args = parser.parse_args()

# Check from which file or files will extract data
listOfFiles = list()
filename = ""
if args.path:
    filename = args.path
else:
    for (dirpath, dirnames, filenames) in os.walk(_root_folder):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

# Initialize lists
milcom_results = []
newalg_results = []

# Get results of all files
if args.path:
    milcom_results,newalg_results = get_results(filename)
else:    
    for filename in listOfFiles:
        milcom_results,newalg_results = get_results(filename)

# Create a string with all results to print it
string_to_print = ""
for result in milcom_results:
	string_to_print += str(result)
	string_to_print += " "
string_to_print += "\n"
string_to_print += "\n"
for result in newalg_results:
	string_to_print += str(result)
	string_to_print += " "
string_to_print += "\n"

print string_to_print

# Calculate some statistic stuff related to results of algorithms
avg_mil = sum(milcom_results)/len(milcom_results)
max_mil = max(milcom_results)
min_mil = min(milcom_results)

avg_new = sum(newalg_results)/len(newalg_results)
max_new = max(newalg_results)
min_new = min(newalg_results)

print "Average MCDS for milcom algorithm is {}, max value is {} and min is {}".format(avg_mil,max_mil,min_mil)
print "Average MCDS for new algorithm is {}, max value is {} and min is {}".format(avg_new,max_new,min_new)

# Points in x axes
x1 = [i for i in range(len(milcom_results))]

# plotting the line 1 points
plt.plot(x1, milcom_results, label = "milcom")

# Points in x axes
x2 = [i for i in range(len(newalg_results))]

# plotting the line 2 points
plt.plot(x2, newalg_results, label = "new")

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
# giving a title to my graph
plt.title('Comparison between milcom and new algorithm')

# show a legend on the plot
plt.legend()

# function to show the plot
plt.show()