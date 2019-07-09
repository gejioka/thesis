import sys

filename = sys.argv[1]
milcom_results = []
newalg_results = []
with open(filename,"r") as f:
    for line in f:
        if "milcom algorithm" in line:
            milcom_results.append(int(line.split(" ")[5]))
        elif "new algorithm" in line:
            newalg_results.append(int(line.split(" ")[5]))
print "milcom results:"
for result in milcom_results:
    print result

print "new algorithm results:"
for result in newalg_results:
    print result
