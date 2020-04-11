import socket

port = 1234
url = "https://static.magnum.wtf/"


# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# reserve and litsen for requests on $port
s.bind((socket.gethostname(), 1234))

# set a queue depth of 10, since we can handle just one connection at a time



# Listen indefinetly
while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    clientsocket.send(bytes("Hey there!!!","utf-8"))
    clientsocket.close()    