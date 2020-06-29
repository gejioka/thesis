from os import listdir
import subprocess
import sys
import ast
import os
import re

MAX_K = 4
MAX_M = 4

def execute_command(filename,metric,algorithm,backbone,pool,counter,k,m,number_of_cores,merge=False):
    """
    Description: Run thesis for specific input file with specific arguments

    Args:
        filename(String): The name of specific file
        metric(string): The name of PCI metric
        algoprithm(int): An integer that match to an algorithm (1-->MILCOM,2-->NEW,3-->ROBUST)
        backbone(string): Backbone has two values, CDS or MCDS
        pool(list): A list with all processes running the same time
        counter(int): A counter for the processes
        k(int): The first value for robust algorithm
        m(int): The second value for robust algorithm
        number_of_cores(int): The number of cores which specific machine can offer
        merge(boolean): A value for merge results
    Returns:
        pool
    """
    proc = None

    if k == 0 and m == 0:
        if merge:
            proc = subprocess.Popen(["python", "../../code/main.py", "-fp", filename, "-a", algorithm, "-p", metric, "-lf", "../../code/out.txt", "-i", str(counter), "-n", str(number_of_cores), "--store_log", "--clock", "--testing", backbone, "--merge"])
        else:
            proc = subprocess.Popen(["python", "../../code/main.py", "-fp", filename, "-a", algorithm, "-p", metric, "-lf", "../../code/out.txt", "-i", str(counter), "-n", str(number_of_cores), "--store_log", "--clock", "--testing", backbone])
    else:
        if merge:
            proc = subprocess.Popen(["python", "../../code/main.py", "-fp", filename, "-a", algorithm, "-p", metric, "-k", str(k), "-m", str(m), "-lf", "../../code/out.txt", "-i", str(counter), "-n", str(number_of_cores), "--store_log", "--clock", "--testing", backbone, "--merge"])
        else:
            proc = subprocess.Popen(["python", "../../code/main.py", "-fp", filename, "-a", algorithm, "-p", metric, "-k", str(k), "-m", str(m), "-lf", "../../code/out.txt", "-i", str(counter), "-n", str(number_of_cores), "--store_log", "--clock", "--testing", backbone])
    pool.append(proc)
    pid  = proc.pid

    return pool

def wait_processes(pool):
    """
    Description: Wait all processes to finish their jobs

    Args:
        pool(list): A list with all processes running the same time
    Returns:
        -
    """
    exit_codes = [p.wait() for p in pool]

def create_list_of_arguments(filename,metric,pool,counter,list_of_arguments):
    """
    Description: Create a list with all arguments which processes needs

    Args:
        filename(String): The name of specific file
        metric(string): metric(string): The name of PCI metric
        pool(list): A list with all processes running the same time
        counter(int): A counter which for processes
        list_of_arguments(list): A list with all arguments
    Returns:
        counter,list_of_arguments
    """
    list_of_arguments.append([filename,metric,"2","--cds",None,counter,0,0])
    counter += 1
    list_of_arguments.append([filename,metric,"2","--mcds",None,counter,0,0])
    counter += 1
    
    return counter,list_of_arguments

def add_merge_field(list_of_arguments,number_of_cores):
    """
    Description: Add merge field where it needed

    Args:
        list_of_arguments(list): A list with all arguments
        number_of_cores(int): An integer with number of cores for specific machine
    Returns:
        -
    """
    for i in range(len(list_of_arguments)):
        try:
            if i % number_of_cores == 0 and len(list_of_arguments[i-1]) == 8:
                list_of_arguments[i-1].append(True)
        except:
            pass

def delete_files(_root_folder,offset,number_of_cores):
    """
    Description: Delete all files when all processes finish their jobs

    Args:
        _root_folder(string): The root folder for the input files
        offset(int): An integer that tells every process where is the start in root folder
        number_of_cores(int): An integer with number of cores for specific machine 
    Returns:
        -
    """
    list_of_files=[]
    for (dirpath, dirnames, filenames) in os.walk(_root_folder):
        list_of_files += [os.path.join(dirpath, file) for file in filenames]
    
    for filename in list_of_files:
        try:
            if not filename.endswith(".txt") and int(filename.split(".")[1]) >= int(offset) and int(filename.split(".")[1]) < int(offset)+int(number_of_cores):
                os.remove(filename)
        except Exception as err:
            pass

def merge_files(number_of_cores,offset):
    """
    Description: Merge all output files of processes to one

    Args:
        number_of_cores(int): An integer with number of cores for specific machine 
        offset(int): An integer that tells every process where is the start in root folder
    Returns:
        -
    """
    root_path  = ""
    _to_write  = ""
    total_data = ""

    with open("../../tools/path","r") as f:
        for line in f:
            root_path += line
             
    list_of_files = [None]*int(number_of_cores)
    for filename in listdir(root_path):
        try:
            if not filename.endswith(".txt") and int(filename.split(".")[1]) >= int(offset) and int(filename.split(".")[1]) < int(offset)+int(number_of_cores):
                list_of_files[int(filename.split(".")[1])%int(number_of_cores)] = filename
        except Exception as err:
            pass
    
    try:
        list_of_files.sort(key=lambda x : x.split(".")[1])
    except:
        pass
    
    for filename in list_of_files:
        try:
            _to_write = ""
            with open(root_path+filename,"r") as f:
                for line in f:
                    total_data += line
                    _to_write += line
            with open(root_path+filename.split(".")[0]+".txt", "a") as f:
                f.write(_to_write)
                f.flush()
                os.fsync(f)
        except:
            pass

    delete_files(root_path,offset,number_of_cores)

    sys.stdout.write(total_data)
    sys.stdout.flush()

def print_arguments(list_of_arguments):
    """
    Description: Print list of arguments

    Args:
        list_of_arguments(list): A list with all arguments
    Returns:
        -
    """
    for argument in list_of_arguments:
        print argument

def run_tests(list_of_arguments,offset,number_of_cores,list_of_metrics):
    """
    Description: Run all tests

    Args:
        list_of_argument(list): A list with all arguments
        offset(int): An integer that tells every process where is the start in root folder
        number_of_cores(int): An integer with number of cores for specific machine 
        list_of_metrics(list): A list with all metrics
    Returns:
        -
    """
    try:
        pool=[]
        for i in range(int(offset),int(offset)+int(number_of_cores)-1):
            pool = execute_command(list_of_arguments[i][0],list_of_arguments[i][1],list_of_arguments[i][2],list_of_arguments[i][3],pool,list_of_arguments[i][5],list_of_arguments[i][6],list_of_arguments[i][7],number_of_cores)
        pool = execute_command(list_of_arguments[int(offset)+int(number_of_cores)-1][0],list_of_arguments[int(offset)+int(number_of_cores)-1][1],list_of_arguments[int(offset)+int(number_of_cores)-1][2],list_of_arguments[int(offset)+int(number_of_cores)-1][3],pool,list_of_arguments[int(offset)+int(number_of_cores)-1][5],list_of_arguments[int(offset)+int(number_of_cores)-1][6],list_of_arguments[int(offset)+int(number_of_cores)-1][7],number_of_cores,True)
        wait_processes(pool)
        
        merge_files(number_of_cores,offset)
    except KeyboardInterrupt:
        print "An Ctrl+C interrupt occured!!! Program terminated!!!"
        for process in pool:
            process.terminate()
        sys.exit(0)

def main():
    list_of_metrics = ["cl","x","new","la","al","ml","ls","sl","degree"]
    list_of_arguments=[]
    pool = []
    counter = 0

    number_of_cores = sys.argv[1]
    offset = sys.argv[2]
    chunk_end = sys.argv[3]
    argument = sys.argv[4].replace("\"","")
    listOfFiles = ast.literal_eval(argument)

    for i in range(len(listOfFiles)):
        for metric in list_of_metrics:
            counter,list_of_arguments = create_list_of_arguments(listOfFiles[i],metric,[],counter,list_of_arguments)
        add_merge_field(list_of_arguments,int(number_of_cores))
    run_tests(list_of_arguments,int(offset),int(number_of_cores),list_of_metrics)

if __name__=="__main__":
    main()
    sys.exit(0)