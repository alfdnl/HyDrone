import socket
import sys
import time


def setupConnection(HOST, PORT, s):
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
            s.settimeout(2)
        except socket.error as msg:
            s = None
            print(msg)
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            print(canonname)
            s = None
            continue
        return s
    if s is None:
        print("could not open socket")
        


def messageTo40(mess):
    mess = mess + ","
    while len(mess) < 40:
        mess = mess + "X"
    return mess


def sendMessage(mess, s):
    #s = setupConnection(HOST, PORT, s)
    mess = messageTo40(mess)
    try:
        message = bytes(mess, 'utf-8')
        s.send(message)
        data = s.recv(1024)
        return str(data, 'utf-8')
    except:
        #s = setupConnection(HOST, PORT, s)
        return "error"
    #time.sleep(intervalTime)

# print(sendMessage("CONTROL,MOTOR_OFF"))