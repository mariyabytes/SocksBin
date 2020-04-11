#!/usr/bin/python3

import os
import socket
import secrets
import sys
import getopt
import re


# Config
def main(theargs):
    # where to serve this page.
    # 127.0.0.1 / localhost => only accessible locally, on this machine
    # 0.0.0.0 => accessible to the internet, by any host
    hostname = "0.0.0.0"

    # which port number to bind to
    # choose a port number > 1000, to prevent interference with system processes
    port = "1234"

    # maximum number of clients this can handle at any given time
    queue_depth = 10

    # directory path
    # default is $HOME i.e. /home/username/sockbin
    output_directory = os.path.expanduser("~") + "sockbin"
    # specify the length of generated filename. multiples of 2 only
    slug_size = 8

    # amount of data transferred at a time, in bytes
    # set between 4096 and 64000.
    buffer_size = 32768

    # path for log file
    log_file = "/tmp/socklog.txt"

    helpmessage = """Welcome to SockBin, the command line pastebin !
    Released under GNU GPL.

    -n --hostname\t\tSet the hostname to listen for. 0.0.0.0 by default.
    -p --port\t\tExternel port number to listen on. 8888 by default
    -q --queue_depth\tMax number of simultaneous connections to accept
    -o --output_directory\tFile storage location. $HOME/sockbin by default
    -s --slug_size\tLength of url to generate.
    -b --buffer_size\tPacket size in bytes. 
    -l --log_file\t\tPath to log file.
    -h --help\t\tDisplay this message

    """

    try:
        opts, args = getopt.getopt(theargs, "n:p:q:o:s:b:l:h:", [
                                   "hostname=", "port=", "queue_depth=", "output_directory=", "slug_size=", "buffer_size=", "log_file=", "help="])
        for opt, arg in opts:
            if opt in ['-n', '--hostname']:
                if arg.find('/') != -1:
                    print("Incorrect hostname. / not allowed. Run with -h for options")
                    sys.exit()
                else:
                    hostname = arg
            elif opt in ['-p', "--port"]:
                if re.match("^ *\d[\d ]*$", arg) is None:
                    print(
                        "Incorrect port format. Choose a number between 0 and 64738. Warning: ports below 1000 could interfere with system processes.")
                    sys.exit()
                elif int(arg) > 64738:
                    print(
                        "Incorrect port format. Choose a number between 0 and 64738. Warning: ports below 1000 could interfere with system processes.")
                    sys.exit()
                elif int(arg) < 1000:
                    choice = input(
                        "Warning: ports below 1000 could interfere with system processes. Do you want to choose a different port ? (y/n): ")

                    if choice.lower() == "y":
                        arg = input("Please enter your new port number: ")
                        if re.match("^ *\d[\d ]*$", arg) is None:
                            print(
                                "Incorrect port format. Choose a number between 1000 and 64738")
                            sys.exit()
                        else:
                            port = arg
                    elif choice.lower() == "n":
                        pass

                port = int(arg)
            elif opt in ['-q', "--queue_depth"]:
                if not arg.isdigit():
                    print(
                        "Queue depth can only be an integer. Run with -h for more options")
                    sys.exit()
                queue_depth = int(arg)
            elif opt in ['-o', "--output_directory"]:
                directory = arg
                if os.path.isdir(directory):
                    permission = (isWritable(directory))

                    if not permission:
                        print(f"You do not have permissions to write to {directory}")
                        sys.exit()
                    else:
                        output_directory = arg
                else:
                    parent_dir = (os.path.abspath(os.path.join(directory, os.pardir)))

                    if not os.path.isdir(parent_dir):
                        print(f"The parent folder {parent_dir} does not exist. Please try again after creating it.")
                        sys.exit()
                    permission = (isWritable(parent_dir))
                    
                    if not permission:
                        print(f"You do not have permissions to write to {directory}, or the parent folder {parent_dir} does not exist")
                        sys.exit()
                    else:
                        try:
                            os.makedirs(directory)
                            print(f"> Directory {directory} created !")
                            output_directory = arg
                        except OSError:
                            print("unable to create directory. Please check your permissions.")
                            sys.exit()                
            elif opt in ['-s', "--slug_size"]:
                slug_size = arg
            elif opt in ['-b', "--buffer_size"]:
                buffer_size = arg
            elif opt in ['-l', "--log_file"]:
                log_file = arg

        print({
            "hostname": hostname,
            "port": port,
            "queue": queue_depth,
            "output": output_directory,
            "slug": slug_size,
            "buff": buffer_size,
            "log": log_file,
        })

    except getopt.GetoptError as err:
        print(err)
        print("Run with -h or --help to see the various options")


#######################################################################################

def server():
    # create the socket
    # AF_INET => IPv4
    # SOCK_STREAM => TCP Connections
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(("0.0.0.0", 1234))

    s.listen(5)

    while True:
        clientSocket, address = s.accept()
        print(f"Connection from {address} has been established")
        filepath = secrets.token_hex(8)
        clientSocket.sendall(
            bytes("https://static.magnum.wtf/"+filepath, "utf-8"))
        clientSocket.shutdown(socket.SHUT_WR)

        full_message = ""
        while True:
            data = clientSocket.recv(4096)
            if len(data) <= 0:

                break
            print("ingesting")
            full_message += data.decode('utf-8')

        with open(filepath+".txt", 'w') as writer:
            writer.write(full_message)




def isWritable(directory):

    try:
        tmp_prefix = "write_tester";
        count = 0
        filename = os.path.join(directory, tmp_prefix)
        while(os.path.exists(filename)):
            filename = "{}.{}".format(os.path.join(directory, tmp_prefix),count)
            count = count + 1
        f = open(filename,"w")
        f.close()
        os.remove(filename)
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    main(sys.argv[1:])
