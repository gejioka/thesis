from struct import *
import subprocess
import threading
import pickle
import socket
import time
import dill
import ast
import sys

### Global variables ### 
MAX_SIZE = 4096

MAX_K = 4
MAX_M = 4

serverIP = "172.104.249.240"
server_port = 10000

server_interrupt = False
user_interrupt = False

number_of_cores = 0

offset = 0

global_list = [i for i in range(MAX_SIZE)]
list_of_files = []

last_fd = 0

def connect_to_server(number_of_cores):
    """
    Description: Client create a connection with server

    Args:
        number_of_cores(int): Number of cores which server can use for this client
    Returns:
        connection socket
    """

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (serverIP, server_port)
    print "connecting to %s port %s" % server_address
    sock.connect(server_address)

    # Send packet with number of cores to server
    packed_message = create_message(1,number_of_cores,0,0,0)
    if packed_message != None:
        sock.sendall(packed_message)

    return sock

def create_message(message_id,number_of_cores,file_id,file_text,offset):
    """
    Description: Client create a connection with server

    Args:
        number_of_cores(int): Number of cores which server can use for this client
    Returns:
        connection socket
    """
    global last_fd
    
    # Tell to server the number of cores
    if message_id == 1:
        packed_message = pack("ii"+str(len(number_of_cores))+"s",1,len(number_of_cores),number_of_cores)
        
        return packed_message
    # Ask from server next input files
    elif message_id == 2:
        packed_message = pack("i",2)

        return packed_message
    # Tell server that wanna start file trasfer
    elif message_id == 3:
        packed_message = pack("iii"+str(len(file_text))+"s",3,file_id,len(file_text),file_text)

        return packed_message
    # Tell server to close session
    elif message_id == 4:
        packed_message = pack("iii",4,last_fd,offset)

        return packed_message
    return None

def recognize_server_packet(packed_message):
    """
    Description: Method that client recognize server packet

    Args:
        packed_message(string): A packed message that server send to client
    Returns:
        packed_message
    """
    global list_of_files
    global global_list
    global offset
    global last_fd

    # Unpack message ID that server sends
    message_id = unpack("i", packed_message[0:4])[0]

    # Server message with new chunk of files and file ID
    if message_id == 2:
        offset = unpack("i", packed_message[4:8])[0]
        chunk_end = unpack("i", packed_message[8:12])[0]
        file_id = unpack("i", packed_message[12:16])[0]
        last_fd = file_id
        
        print "Start point in list is:", offset
        print "End point in list is:", chunk_end
        print "File ID is:", file_id

        proc = subprocess.Popen(["python", "../../tools/test_algorithms.py", str(number_of_cores), str(offset), str(chunk_end), str(list_of_files)],stdout=subprocess.PIPE)
        proc.wait()
        result = proc.communicate()[0]
        
        packed_message = create_message(3,0,file_id,result,0)
    
        return packed_message
    
    # Close session with server and terminate client
    if message_id == 4:
        return "close_session"
    # Server want to send list of files to client
    if message_id == 5:
        return "list_of_files"
    return None

def create_relative_paths():
    """
    Description: Create a list with all relative paths of input files

    Args:
        -
    Returns:
        list_of_files
    """
    global list_of_files

    for i in range(len(list_of_files)):
        list_of_files[i] = list_of_files[i][list_of_files[i].find("Experiment Networks"):]
    return list_of_files

def send_message(sock):
    """
    Description: Method that use client to send message to server

    Args:
        sock(Obj): A socket object which use to communicate with server
    Returns:
        -
    """
    global server_interrupt
    global number_of_cores 
    global user_interrupt
    global list_of_files

    while not server_interrupt and not user_interrupt:
        try:
            # Receive packet from server
            packet = sock.recv(MAX_SIZE)
            message = recognize_server_packet(packet)
            
            if message != None:
                # Close session with server
                if message == "close_session":
                    server_interrupt = True
                    sock.close()
                # Receive list of files from server
                elif message == "list_of_files":
                    packet = sock.recv(MAX_SIZE)
                    packet = dill.loads(packet)

                    list_of_files += packet
                    sock.sendall("OK")
                    while "OK" not in packet:
                        try:
                            packet = sock.recv(MAX_SIZE)

                            if "OK" in packet:
                                if packet != "OK":
                                    packet = dill.loads(packet.rstrip())
                                    
                                    packet = packet[:len(packet)-2]
                                    list_of_files += packet
                                    sock.sendall("OK")
                                    break
                                else:
                                    break
                            else:
                                packet = dill.loads(packet.rstrip())
                                sock.sendall("OK")
                            list_of_files += packet
                        except Exception as err:
                            print "First error"
                            print err
                    list_of_files = create_relative_paths()
                    
                    message = create_message(2,0,0,0,0)
                    sock.sendall(message)
                else:
                    sock.sendall(message)
                    message = create_message(2,0,0,0,0)
                    sock.sendall(message)
            time.sleep(1)
        except Exception as err:
            server_interrupt = True
            user_interrupt = True
            

def close_session_with_server(sock):
    """
    Description: Close session with server

    Args:
        sock(Obj): A socket object which use to communicate with server
    Returns:
        -
    """
    global offset
    
    message = create_message(4,0,0,0,offset)
    user_interrupt = True
    sock.sendall(message)
    sock.close()
    print "\nClient is terminated by Ctrl+C signal!!!"
    sys.exit(1)

def main():
    global server_interrupt
    global number_of_cores
    global user_interrupt

    # number_of_cores = raw_input("Give number of cores: ")
    number_of_cores = sys.argv[1]

    sock = connect_to_server(number_of_cores)

    send_message_thread = threading.Thread(target=send_message,args=(sock,))
    send_message_thread.start()

    while not user_interrupt and not server_interrupt:
        try:
            time.sleep(0.1)
            # number_of_cores = raw_input("Give number of cores: ")
        except KeyboardInterrupt:
            close_session_with_server(sock)
    print "Server is closed!!!"

if __name__=="__main__":
    main()
    sys.exit(0)
