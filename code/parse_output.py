with open("output.txt","r") as f:
    all_nodes = 0
    dominators = 0
    for line in f:
        dominators +=1 
        all_nodes += int(line.split(" ")[1].replace(")","").strip())
    print all_nodes + dominators