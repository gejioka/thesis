from struct import *
import server_log as sl
import threading
import pickle
import socket
import time
import sys
import dill
import os

# Root folder of all input networks
_root_folder = "/root/Experiment_Networks1"

# Global variables
BUFFER_SIZE = 10000
MAX_SIZE = 1024
MAX_K = 4
MAX_M = 4
MILCOM_ALG = True
NEW_ALG = True
ROBUST_ALG = True
server_IP = "172.104.249.240"
server_port = 10000
max_size = 0
backlog = 5
offset = 0
fileID = 0
_is_over = False
last_packets = 0

user_interrupt = False
sock = None

list_of_connections = []
list_of_clients = []
listOfFiles = []
list_of_files = [""]*BUFFER_SIZE
incomplete_fds_list = []

lock = threading.Lock()

def init_server():
    """
    Description: Method that use server to create a TCP/IP socket

    Args:
        -
    Returns:
        sock(Obj): A socket object which use to communicate with server
    """
    global max_size

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_address = (server_IP, server_port)
    sl.write_log("[!] Server open TCP/IP socket with IP address {} and port {}!!!".format(server_IP,server_port),"info")
    print "starting up on %s port %s" % server_address

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)

    max_size = find_max_size()

    return sock

def accept_clients(sock):
    """
    Description: Method that use server to accept clients

    Args:
        sock(Obj): A socket object which use to communicate with server
    Returns:
        -
    """
    global list_of_connections
    global list_of_clients
    global user_interrupt
    global lock

    # Listen for incoming connections
    sock.listen(backlog)
    
    print "Waiting for connection..."
    while not user_interrupt:
        try:
            connection, client_address = sock.accept()
            list_of_connections.append((connection,client_address))

            sl.write_log("[+] Server accepted new client and add it to list.","info")

            # Wait to receive number of cores of specific client
            with lock:
                packet = connection.recv(MAX_SIZE)
            number_of_cores = recognize_client_message(packet,0)

            client_thread = threading.Thread(target=client_thread_f,args=(connection,client_address,number_of_cores[0]))
            client_thread.start()

            list_of_clients.append(client_thread)
        except socket.timeout:
            if len(list_of_clients) > 0:
                for i in range(len(list_of_clients)):
                    if not list_of_clients[i].isAlive():
                        list_of_clients[i] = None
                list_of_clients = [client for client in list_of_clients if client != None]

def split_list_to_packets(listOfFiles):
    """
    Description: Split list of files to packets.

    Args:
        listOfFiles(list): A list that contains all input files
    Returns:
        packed_list
    """
    packed_list = []
    
    sl.write_log("[!] Server split list of files to packets.","info")

    temp_list = []
    for filename in listOfFiles:
        temp_list.append(filename)
        if len("".join(temp_list)) >= MAX_SIZE and len("".join(temp_list[:len(temp_list)-1])) < MAX_SIZE:
            packed_list.append(temp_list)
            temp_list = []
    if temp_list:
        packed_list.append(temp_list)
    
    return packed_list

def send_list_to_client(connection):
    """
    Description: Method that use server to send list of files to client

    Args:
        connection(Obj): A socket object which use to communicate with specific client
    Returns:
        -
    """
    global listOfFiles
    global lock

    with lock:
        sl.write_log("[+] Server send list of files to client.","info")
        packed_list = split_list_to_packets(listOfFiles)

        # Send message id to client
        packed_message = create_next_packet(0,0,0,5)
        connection.sendall(packed_message)
        
        # Send list of files to client
        for packet in packed_list:
            try:
                message = dill.dumps(packet)
                connection.sendall(message)
                connection.recv(MAX_SIZE)
            except Exception as err:
                sl.write_log(err,"warning")
        connection.sendall("OK")
        sl.write_log("[!] Server send successfully all files to client","info")
        
def create_list_of_files(_root_folder):
    """
    Description: Method that use server create a list with all input files that clients needs to process

    Args:
        _root_folder(string): The root path where exist all input files server side
    Returns:
        listOfFiles
    """
    # Create all different paths exists under root folder
    sl.write_log("[!] Server create a list with all input files for clients.","info")

    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(_root_folder):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    return listOfFiles

def find_max_size():
    """
    Description: Method that calculates the size of all combinations should be analyzed

    Args:
       -
    Returns:
        max_size
    """
    global listOfFiles
    global max_size

    if MILCOM_ALG and NEW_ALG and ROBUST_ALG:
        max_size = len(listOfFiles)*9*(2+(MAX_K-1)*(MAX_M-1))*2
    elif MILCOM_ALG and NEW_ALG:
        max_size = len(listOfFiles)*9*2*2
    elif (MILCOM_ALG and ROBUST_ALG) or (NEW_ALG and ROBUST_ALG):
        max_size = len(listOfFiles)*9*(1+(MAX_K-1)*(MAX_M-1))*2
    elif MILCOM_ALG or NEW_ALG:
        max_size = len(listOfFiles)*9*2
    elif ROBUST_ALG:
        max_size = len(listOfFiles)*9*((MAX_K-1)*(MAX_M-1))*2
    
    return max_size
    

def create_next_packet(offset,number_of_cores,fileID,message_id):
    """
    Description: Method that use server to create next packet for client

    Args:
        offset(int): An integer that tells client where to find the next set of input files in list
        number_of_cores(int): An integer that tell the client the end of the next set of input files
        fileID(int): An integer that tell server where to store the results of specific client in list
        message_id(int): An integer which server decide the type of client message
    Returns:
        packed_message
    """
    if message_id == 2:
        sl.write_log("[+] Server create next packet for client.","info")
        sl.write_log("Message ID is 2. Next group of files is from {}-{}. File ID for this group is {}.".format(offset,offset+int(number_of_cores),fileID),"debug")
        
        packed_message = pack("iiii",2,offset,offset+number_of_cores,fileID)

        return packed_message
    if message_id == 4:
        sl.write_log("[-] Server want to close session with client.","info")
        packed_message = pack("i",4)

        return packed_message
    if message_id == 5:
        sl.write_log("[+] Server starts tranfer of files with client.","info")
        packed_message = pack("i",5)

        return packed_message
    if message_id == 6:
        sl.write_log("[!] Server resend packet to client.","info")
        packed_message = pack("iiii",2,offset,offset+number_of_cores,fileID)

        return packed_message
    return None

def recognize_client_message(packed_message,number_of_cores):
    """
    Description: Method that use server recognize client message

    Args:
        packed_message(string): A string with packet message of client
        number_of_cores(int): An integer that tells server how many cores this client offer
    Returns:
        packed_message
    """
    global last_packets
    global listOfFiles
    global max_size
    global _is_over
    global offset
    global fileID

    sl.write_log("[+] Server receive new packet from client.","info")
    message_id = unpack("i",packed_message[0:4])
   
    # Message id for number of cores
    if message_id[0] == 1: 
        message_size = unpack("i", packed_message[4:8])      
        number_of_cores = unpack(str(message_size[0])+"s", packed_message[8:])

        sl.write_log("Message ID is: {}\nNumber of cores that client lend to server is: {}".format(message_id[0],number_of_cores[0]),"info")

        return number_of_cores
    # Message id for request next chunk of files
    elif message_id[0] == 2:
        if offset+number_of_cores <= max_size:
            if incomplete_fds_list:
                info = incomplete_fds_list.pop(0)
                packed_message = create_next_packet(info[1],number_of_cores,info[0],2)
            else:
                packed_message = create_next_packet(offset,number_of_cores,fileID,2)
                offset += number_of_cores
                fileID += 1
        else:
            if incomplete_fds_list:
                info = incomplete_fds_list.pop(0)
                packed_message = create_next_packet(info[1],max_size-offset,info[0],2)
            else:
                packed_message = create_next_packet(offset,max_size-offset,fileID,2)
                offset += max_size-offset
                fileID += 1

        return packed_message
    # Message id for starting transfer file
    elif message_id[0] == 3:
        file_contents = ""

        sl.write_log("Server get results of client. Write results to file and append list of contents.","info")

        file_id = unpack("i", packed_message[4:8])[0]
        message_size = unpack("i", packed_message[8:12])[0]
        unpacked_message = unpack(str(message_size)+"s",packed_message[12:])
        file_contents += unpacked_message[0]
        with open("results.temp","a") as f:
            f.write(unpacked_message[0])
            f.write("\n")

        list_of_files[file_id] += file_contents
        
        sl.write_log("List of contents after new data is: {}".format("".join([i for i in list_of_files if i != ""])),"debug")

        if offset >= max_size:
            _is_over = True
    # Message id for closing session with client because is offline
    elif message_id[0] == 4:
        sl.write_log("Server close session with client because client is offline.","info")
        unpacked_message = unpack("ii",packed_message[4:])
        incomplete_fds_list.append(unpacked_message)

        return "close_session"
    elif message_id[0] == 5:
        sl.write_log("NACK packet from client. Server need to resend packet to client.","info")
        unpacked_message = unpack("ii",packed_message[4:])
        packed_message = create_next_packet(unpacked_message[1],number_of_cores,unpacked_message[0],6)

        return packed_message
    return None

def close_session_with_all_clients():
    """
    Description: Close session with all clients

    Args:
        -
    Returns:
        -
    """
    global list_of_connections

    sl.write_log("Server try to close session with all clients...","info")

    for connection in list_of_connections:
        message = create_next_packet(0,0,0,4)
        connection[0].sendall(message)
        try:
            connection[0].close()
        except:
            pass
    sl.write_log("Server successfully close all sessions with clients.","info")

def wait_threads(accept_thread,list_of_clients):
    """
    Description: Wait all threads end their jobs

    Args:
        accept_thread(obj): An thread object for accept thread function
        list_of_client(list): A list with all client threads
    Returns:
        -
    """
    sl.write_log("Server wait all client threads to join before terminate.","info")
    accept_thread.join()
    for client in list_of_clients:
        if client != None:
            client.join()

def client_thread_f(connection,client_address,number_of_cores):
    """
    Description: A thread method for client threads
    Args:
        connection(socket): A socket to communicate server with specific client
        client_address(tuple): A tuple with IP and port for specific client
        number_of_cores(int): An integer that tells server how many cores this client offer
    Returns:
        -
    """
    global list_of_connections
    global user_interrupt
    global offset
    global fileID
    global lock

    client_interrupt = False

    print "Try to connect client with IP {} and port {}!!!".format(client_address[0],client_address[1])  
    print "Number of cores is:", number_of_cores

    send_list_to_client(connection)

    # Receive the data in small chunks and retransmit it
    while not user_interrupt and not client_interrupt:
        packet = connection.recv(MAX_SIZE)
        
        packed_message = ""
        with lock:
            try:
                packed_message = recognize_client_message(packet,int(number_of_cores))
                if packed_message != None:
                    if packed_message == "close_session":
                        try:
                            client_interrupt = True
                            
                            print "connections", list_of_connections
                            list_of_connections.remove((connection,client_address))
                            connection.close()
                        except Exception as err:
                            sl.write_log(err,"warning")
                    else:
                        connection.sendall(packed_message)
                else:
                    pass
            except Exception as err:
                if not _is_over:
                    while True:
                        try:
                            for connection1 in list_of_connections:
                                connection1[0].sendall("ON")
                            break
                        except Exception as err1:
                            sl.write_log("Send failed!!!"+str(err1),"warning")
                            time.sleep(1)

def main():
    global user_interrupt
    global list_of_files
    global listOfFiles
    global _root_folder
    global _is_over
    global sock

    listOfFiles = create_list_of_files(_root_folder)

    sock = init_server()
    sock.settimeout(2)

    accept_thread = threading.Thread(target=accept_clients,args=(sock,))
    accept_thread.start()

    try:
        while not user_interrupt:
            if _is_over == True:
                close_session_with_all_clients()

                user_interrupt = True
                wait_threads(accept_thread,list_of_clients)
            
            time.sleep(.1)
    except KeyboardInterrupt:
        print "\nA Ctrl+C signal occured. Program terminated!!!"
        for text in list_of_files:
            if text != "":
                print text
            else:
                break
        close_session_with_all_clients()

        user_interrupt = True
        wait_threads(accept_thread,list_of_clients)
    sock.close()
    
    filename = "results.txt"
    with open(filename,"w") as f:
        for line in list_of_files:
            if line != "":
                f.write(line+"\n")
                f.flush()

if __name__=="__main__":
    main()
    sys.exit(0)
