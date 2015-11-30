import socket
import time
import multiprocessing

HOST = '127.0.0.1'
PORT = 50045


class client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        time.sleep(0.1)

    def sndMsg(self,msg):
        self.s.send(msg.encode())
        data = self.s.recv(1024)
        print(data)

    def closeCon(self):
        self.s.send(''.encode())
        self.s.close()

if __name__ == "__main__":

    print('user 1 connect' )
    c = client()
    c.sndMsg("A text11")
    c.sndMsg("A text21")

    time.sleep(10)

    c.sndMsg("A text12")
    c.sndMsg("A text22")