import socket
import sys

class EchoServerTTT:
    def __init__(self, address, port, data_size):
        self.data_size=data_size
        self._createTcpIpSocket()
        self._bindSocketToThePort(address,port)

    def handle_connection(self):
        self.sock.listen(1)
        while True:
            connection, client_address = self.sock.accept()
            data = connection.recv(self.data_size)
            print(client_address, data.decode())
            connection.send(data)

    def _createTcpIpSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _bindSocketToThePort(self,address,port):
        server_address = (address, port)
        print('bind to %s port %s' % server_address)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(server_address)

    def closeSocket(self):
        self.sock.close();

if __name__=="__main__":
    host = 'localhost'
    port = 50005
    data_size = 1024
    server=EchoServerTTT(host,port,data_size)
    server.handle_connection()
    server.closeSocket()
