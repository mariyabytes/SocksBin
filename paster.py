#!/usr/bin/python3

import os,sys,socket,secrets

# Config


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
        clientSocket.sendall(bytes("https://static.magnum.wtf/"+filepath, "utf-8"))
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



def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile

if __name__ == "__main__":
   main(sys.argv[1:])