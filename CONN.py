import socket
import sys
import time


def setupConnection(HOST, PORT, s):
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except socket.error as msg:
            s.close()
            s = None
            continue
        return s
    if s is None:
        print("could not open socket")
        sys.exit(1)


def messageTo40(mess):
    mess = mess + ","
    while len(mess) < 40:
        mess = mess + "X"
    return mess


def sendMessage(mess, HOST, PORT, s, intervalTime):
    s = setupConnection(HOST, PORT, s)
    mess = messageTo40(mess)
    try:
        message = bytes(mess, 'utf-8')
        s.send(message)
        data = s.recv(1024)
        return str(data, 'utf-8')
    except:
        return "error"
        s = setupConnection(HOST, PORT, s)
    time.sleep(intervalTime)

# print(sendMessage("CONTROL,MOTOR_OFF"))
