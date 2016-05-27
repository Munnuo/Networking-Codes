import socket
import socketserver
import sys
import os.path


HOST = 'localhost'

PORT = 8010


def listToStrings(list):
    x = 0
    temp = ""
    for x in range(0, len(list)):
        temp = temp + list[x]

    temp = temp.strip("\n")
    return temp

# This next command creates the socket server for the TCP Connection
# If a socket with this port number already exist, the socket fails to be created

print('- Creating Socket')
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('- Failed to create socket')
    sys.exit()

# This is the while loop controller. It only allows for one request to be process then the connection is closed.
reqNum = 0

# this is where the socket is being attached with the port number and ip address listed above
# If the port number already has a socket assigned, the socket fails to be binded to the port number
try:
    sock.bind((HOST, PORT))
except socket.error as msg:
    print('* bind failed ')
    sys.exit()

print('- Socket bind completed! ')

# socket begins to listen to port here
sock.listen(10)
# the socket will allow a host to try and connect to the socket 10 times before it won't allow any more tries.

print('- Socket is now listening for connections')

# This loop continues to allow socket connections until a requested is processed.
while (reqNum < 1):

    conn, addr = sock.accept()  # here the connection is accepted and established
    print('- socket now connected to ' + addr[0] + ' : ' + str(addr[1]))

    req = conn.recv(4096)
    # the request is received here by the server

    reqUrl = req.split()[1]
    reqUrl = reqUrl[1:]
    # The request is parsed for the file the client is requested.


    try:

        with open(reqUrl) as fn:
            cont = fn.readlines()


        content = listToStrings(cont)

        respProto = 'HTTP/1.1'
        respStatus = '200'
        respText = 'OK'

        respHeadL = respProto + ' ' + respStatus + ' \ ' + respText

        conn.send(respHeadL.encode("UTF-8"))
        # The header command for HTTP is send here to set up the page

        para = '\n'
        conn.send(para.encode("UTF-8"))
        # The header command is split from the actual file data with \n symbol

        conn.send(content.encode("UTF-8"))

        reqNum = reqNum+1
        conn.close()

    except IOError:
        resp = "HTTP/1.1 404 \ Not Found"
        conn.send(resp.encode("UTF-8"))
        para = '\n'
        conn.send(para.encode("UTF-8"))

        conn.close()


print("- Request completed!")
# Data has been successfully sent to the requested host




sock.close()