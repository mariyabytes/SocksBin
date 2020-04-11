#!venv/bin/python

import os
import socket
import secrets
import sys
import getopt
import re
from time import gmtime, strftime

# Config


def main(theargs):
    # where to serve this page.
    # 127.0.0.1 / localhost => only accessible locally, on this machine
    # 0.0.0.0 => accessible to the internet, by any host
    hostname = "0.0.0.0"

    # which port number to bind to
    # choose a port number > 1000, to prevent interference with system processes
    port = 8888

    # maximum number of clients this can handle at any given time
    queue_depth = 10

    # directory path
    # default is $HOME i.e. /home/username/socksbin
    output_directory = os.path.join(os.path.expanduser("~"), "socksbin")
    # specify the length of generated filename. multiples of 2 only
    slug_size = 8

    # amount of data transferred at a time, in bytes
    # set between 4096 and 64000.
    buffer_size = 32768

    log = False
    # path for log file
    log_file = "/tmp/socklog.txt"

    # base url where the file will be served to the user
    base_url = "https://socksbin.magnum.wtf/"

    helpmessage = """
    Welcome to SocksBin, the command line pastebin !
    Released under GNU GPL.

    -n --hostname\tSet the hostname to listen for. 0.0.0.0 by default.
    -p --port\tExternel port number to listen on. 8888 by default
    -q --queue_depth\tMax number of simultaneous connections to accept
    -o --output_directory\tFile storage location. $HOME/socksbin by default
    -s --slug_size\tLength of url to generate.
    -b --buffer_size\tPacket size in bytes. 
    -l --log_file\t\tPath to log file.
    -h --help\t\tDisplay this message
    """
    try:
        if theargs[0] == "-h" or theargs[0] == "--help":
            print(helpmessage)
            sys.exit()
    except IndexError:
        pass
    try:
        opts, args = getopt.getopt(theargs, "n:p:q:o:s:b:l:u:", [
                                   "hostname=", "port=", "queue_depth=", "output_directory=", "slug_size=", "buffer_size=", "log_file=", "url="])
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
                            port = int(arg)
                    elif choice.lower() == "n":
                        pass

                port = int(arg)
            elif opt in ['-q', "--queue_depth"]:
                if not arg.isdigit():
                    print(
                        "Queue depth can only be an integer. Run with -h for more options")
                    sys.exit()
                elif int(arg) > 1000 or int(arg) < 2:
                    print("Queue depth has to be between 2 and 1000")
                    sys.exit()

                queue_depth = int(arg)
            elif opt in ['-o', "--output_directory"]:
                directory = arg
                if os.path.isdir(directory):
                    permission = (isWritable(directory))

                    if not permission:
                        print(
                            f"You do not have permissions to write to {directory}")
                        sys.exit()
                    else:
                        output_directory = arg
                else:
                    parent_dir = (os.path.abspath(
                        os.path.join(directory, os.pardir)))

                    if not os.path.isdir(parent_dir):
                        print(
                            f"The parent folder {parent_dir} does not exist. Please try again after creating it.")
                        sys.exit()
                    permission = (isWritable(parent_dir))

                    if not permission:
                        print(
                            f"You do not have permissions to write to {directory}, or the parent folder {parent_dir} does not exist")
                        sys.exit()
                    else:
                        try:
                            os.makedirs(directory)
                            print(f"> Directory {directory} created !")
                            output_directory = arg
                        except OSError:
                            print(
                                "unable to create directory. Please check your permissions.")
                            sys.exit()
            elif opt in ['-s', "--slug_size"]:
                if not arg.isdigit():
                    print("slug length can only be a integer, between 4 and 20")
                    sys.exit()
                elif int(arg) > 20 or int(arg) < 2:
                    print("Slug length has to be between 4 and 20")
                    sys.exit()
                else:
                    slug_size = int(arg)
            elif opt in ['-b', "--buffer_size"]:

                if not arg.isdigit():
                    print("buffer length can only be a integer, between 1024 and 60000")
                    sys.exit()
                elif int(arg) > 60000 or int(arg) < 1024:
                    print("buffer length has to be between 1024 and 60000")
                    sys.exit()
                else:
                    buffer_size = int(arg)
            elif opt in ['-l', "--log_file"]:
                try:
                    parent_dir = (os.path.abspath(
                        os.path.join(arg, os.pardir)))
                except:
                    print("Error while creating log file. Incorrect format.")
                    sys.exit()

                if not os.path.isdir(parent_dir):
                    print(
                        f"The parent folder {parent_dir} does not exist. Please try again after creating it.")
                    sys.exit()
                permission = (isWritable(parent_dir))

                if not permission:
                    print(
                        f"You do not have permissions to write to {arg}, or the parent folder {parent_dir} does not exist")
                    sys.exit()
                log_file = arg
                log = True
            elif opt in ['-h', '--help']:
                print(helpmessage)
                sys.exit()
            elif opt in ['-u', '--url']:
                base_url = arg

        constants = ({
            "hostname": hostname,
            "port": port,
            "queue_depth": queue_depth,
            "output_directory": output_directory,
            "slug_size": slug_size,
            "buffer_size": buffer_size,
            "log": log,
            "log_file": log_file,
            "base_url": base_url
        })

    except getopt.GetoptError as err:
        print(err)
        print("Run with -h or --help to see the various options")

    server(constants)
#######################################################################################


def server(config):
    # create the socket
    # AF_INET => IPv4
    # SOCK_STREAM => TCP Connections
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((config['hostname'], config['port']))

    s.listen(config['queue_depth'])

    while True:
        try:
            clientSocket, address = s.accept()
            print(f"Connection from {address} has been established")
            filepath = secrets.token_hex(config['slug_size'])
            filepath = filepath[:config['slug_size']]
            clientSocket.sendall(
                bytes(config['base_url']+filepath+"\n", "utf-8"))
            clientSocket.shutdown(socket.SHUT_WR)

            full_message = ""
            while True:
                data = clientSocket.recv(config['buffer_size'])
                if len(data) <= 0:

                    break
                full_message += data.decode('utf-8')

            with open(os.path.join(config['output_directory'], filepath), 'w') as writer:
                writer.write(full_message)

            with open(os.path.join(config['output_directory'], filepath + "_color"), 'w') as writer:
                received_code = full_message
                try:
                    from pygments.formatters.html import HtmlFormatter
                    from pygments import highlight
                    from pygments.lexers import guess_lexer
                    lexer = guess_lexer(received_code)
                    fmter = HtmlFormatter(
                        noclasses=True, style="colorful", linenos=True)

                    result = highlight(received_code, lexer, fmter)

                    writer.write(result)
                except Exception as e:
                    print("unable to format")
                    print(e)
                if config['log']:
                    showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    with open(config['log_file'], 'a') as logFile:
                        logFile.write(f"Time: {showtime}\t")
                        logFile.write(f"Address: {address} \t")
                        logFile.write(f"file: {filepath} \n")
        except Exception as e:
            if config['log']:
                with open(config['log_file']+"_e.txt", 'a') as logFile:
                    logFile.write(f"# Address: {address}\t")
                    logFile.write(f"message: {full_message}\t")
                    logFile.write(f"Error: {e}")


def isWritable(directory):

    try:
        tmp_prefix = "write_tester"
        count = 0
        filename = os.path.join(directory, tmp_prefix)
        while(os.path.exists(filename)):
            filename = "{}.{}".format(
                os.path.join(directory, tmp_prefix), count)
            count = count + 1
        f = open(filename, "w")
        f.close()
        os.remove(filename)
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    main(sys.argv[1:])
