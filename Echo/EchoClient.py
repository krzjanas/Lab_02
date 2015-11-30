import socket
import sys

class EchoClientTTT:
    def __init__(self, address, port, data_size):
        self.data_size=data_size
        self._createTcpIpSocket()
        self._connectToServer(address,port)

    def sendMsg(self,msg):
        self.sock.send(msg.encode())
        response = self.sock.recv(self.data_size)
        # self.sock.close()
        print('receive %s' % response)

    def _createTcpIpSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _connectToServer(self,address,port):
        server_address = (address, port)
        print('connecting to %s port %s' % server_address)
        self.sock.connect(server_address)


if __name__=="__main__":
    host = 'localhost'
    port = 50005
    data_size = 1024
    client=EchoClientTTT(host,port,data_size)
    client.sendMsg("pp1")
    client.sendMsg("pp2")
    # client.sendMsg("pp3")
    # while True:
    #     ms = input('Your message: ')
    #     print(ms)
    #     client.sendMsg(str(ms))