#!/usr/bin/env python 3.4.3
#-*- coding:utf-8 –*-
#-----------------------------------------------------------------------------
# The short script is a example that open a socket, sends a query to return a
# value, and closes the socket.
#
# Currently tested on SDS1000X-E,2000X-E, and 5000X models
#
# No warranties expressed or implied
#
# SIGLENT/JAC 03.2019
#
# Modified by Arsein Lupin
#
#-----------------------------------------------------------------------------
import socket # for sockets
import sys # for exit
import time # for sleep
#-----------------------------------------------------------------------------

remote_ip = "192.168.0.11" # should match the instrument’s IP address
port = 5025 # the port number of the instrument service
count = 0

def SocketConnect():
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Failed to create socket.')
        sys.exit();
    try:
        #Connect to remote server
        s.connect((remote_ip , port))
    except socket.error:
        print ('failed to connect to ip ' + remote_ip)
    return s

def SocketQuery(Sock, cmd):
    try :
        #Send cmd string
        Sock.sendall(cmd)
        Sock.sendall(b'\n') #Command termination
        time.sleep(1)
    except socket.error:
        #Send failed
        print ('Send failed')
        sys.exit()
    reply = Sock.recv(4096)
    return reply

def SocketClose(Sock):
    #close the socket
    Sock.close()
    time.sleep(.300)

def main():
    global remote_ip
    global port
    global count

    cmd = "*IDN?"

    print ("Commands: [q] - quit | [Enter] - redo | [XXXX] - send new Command")
    print ()

    while True:
        s = SocketConnect()

        cmd_bytes = cmd.encode("ascii")

        #qStr = SocketQuery(s, b'PAVA? STAT1')
        qStr = SocketQuery(s, cmd_bytes)
        print (str(count) + ":: " + str(qStr))
        print ()

        SocketClose(s)
        keyx = input('-> ')
        if keyx == 'q' :
            break
        elif len(keyx) > 1:
            cmd = keyx


    SocketClose(s)
    sys.exit

if __name__ == '__main__':
    proc = main()
