import socket
import select
import sys
import logging
import time


from Echo.GameList import *
from Echo.MessageHandler import MessageHandler


class EchoGameServer:
    def __init__(self, address, port, recv_buffer, messageHandler, maxNumberOfGamer, timeout=2):
        self.recv_buffer=recv_buffer
        self.messageHandler=messageHandler
        self.maxNumberOfGamers=maxNumberOfGamer
        self._setLogger()
        self._createTcpIpSocket(timeout)
        self._bindSocketToThePort(address,port)
        self._createConnectionList()
        self._setListenForConnection(2)

        self.logger.info("Server: Chat server named %s started on port %s"%(self.gameList.serverName(),str(port)))
        print("Server: Chat server named %s started on port %s"%(self.gameList.serverName(),str(port)))

    def _createTcpIpSocket(self, timeout):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(timeout)

    def _createConnectionList(self):
        game_server = Gamer(self.server_socket, self.server_address)
        game_server.name = "Game Server"
        self.gameList = GameList(game_server)

    def _bindSocketToThePort(self, address, port):
        self.server_address = (address, port)
        self.server_socket.bind(self.server_address)

    def _setListenForConnection(self, backlog):
        self.server_socket.listen(backlog)

    def _setLogger(self):
        self.fh_serv = logging.FileHandler('EchoServer.log')
        self.fh_serv.setLevel(logging.DEBUG)
        self.fh_serv.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
        self.logger = logging.getLogger('EchoServer_log')
        self.logger.addHandler(self.fh_serv)
        self.logger.setLevel(logging.DEBUG)

    def handle_connection(self,info=""):
        read_sockets,write_sockets,error_sockets = select.select(self.gameList.connectedGamersSockets(),[],[])

        for socket in read_sockets:
            if self.gameList.isServerSocket(socket):
                if self.gameList.gamersNamedNumber() + self.gameList.gamersUnnamedNumber() < self.maxNumberOfGamers:
                    self._newConnection()
                    return 1
                else:
                    self._deinedConnection()
                    return -1

            elif self.gameList.unnamedGamer(socket):
                self._addNameToConnection(socket)
                if info:
                    self._send_data("_info",info, socket, True)
                return 2

            elif self.gameList.namedGamer(socket):
                data = self._receive_data(socket)
                if data:
                    gamName = self.gameList.gamerName(socket)
                    gamCurNumbers = self.gameList.gamersNamedNumber()
                    return gamCurNumbers,gamName,data[0],data[1]

        return 0


    def _newConnection(self):
        (socketNew, addresNew) = self.server_socket.accept()
        self.gameList.addGamer(socketNew,addresNew)
        print("Client (%s, %s) connected" % addresNew)
        self._send_data("_name_request","Send your name", socketNew, True)
        self.logger.info("Server - Client (%s, %s) connected"% addresNew)


    def _deinedConnection(self):
        (socketNew, addresNew) = self.server_socket.accept()
        self._send_data("_error","There is too many players on serwer", socketNew, True)
        self.logger.info("Deined acces to client (%s, %s)"% addresNew)

    def _addNameToConnection(self, socket):
        data = self._receive_data(socket)
        if data:
            if data[0] == "_name":
                resp = self.gameList.addGamerName(socket,data[1])
                add = self.gameList.gamerAddress(socket)
                if resp == 1:
                    print("Client (%s, %s) use name <%s>" %(add[0], add[1], data[1]) )
                    self._send_data("_name_accepted","Your name <%s> is accepted" %data[1], socket, True)
                    self.broadcast_data("_info","Player <%s> has joined the game"%data[1],socket, addServerPromt=True)
                    self.logger.info("Server - Client (%s, %s) use name <%s> - socket : %s"%(add[0], add[1], data[1], socket))

                elif resp == -1:
                    self._send_data("_name_request","Name <%s> is already used" %data[1], socket, True)
                    self.logger.info("Server - Unnamed client wanted use name which is already used - socket : %s" %socket)

            else:
                self._send_data("_name_request","Send your name first", socket, True)
                self.logger.info("Server - Unnamed client send message without name - socket : %s" %socket)

    def _receive_data(self, socket):
        try:
            data = socket.recv(self.recv_buffer)
            if data:
                msg = self.messageHandler.decodeMessage(data)
                self.logger.info("Server - receive message - socket : %s\n\tType: %s \tMessage: %s\n"%(socket, msg[0], msg[1]))
                return msg
            else:
                self._removeGamer(socket)
                self.logger.info("Server - message receiving interuppted - socket : %s" %socket)
                return 0

        except (InterruptedError,ConnectionResetError):
            self._removeGamer(socket)
            self.logger.info("Server - message receiving interuppted - socket : %s" %socket)
            return 0

    def _send_data(self, type, message, socket, addServerPromt):
        if addServerPromt:
            mesg = "\\%s\\ %s"%(self.gameList.serverName(),message)
        else:
            mesg = "%s"%message
        msg = self.messageHandler.encodeMessage(type, mesg)
        try :
            socket.send(msg)
            self.logger.info("Server - Send message to client - socket : %s\n\tType: %s \tMessage: %s\n"%(socket, type, message))
        except (InterruptedError,ConnectionResetError):
            self._removeGamer(socket)
            self.logger.info("Server - message sending interuppted - socket : %s" %socket)


    def sendMessage(self,type, message, gamerName, addServerPromt = True):
        self._send_data(type,message,self.gameList.gamerSocket(gamerName), addServerPromt)

    def serverPromt(self):
        return "\\%s\\ "%self.gameList.serverName()

    def broadcast_data(self, type, message, exceptionSocket = 0, exceptionName = 0, addServerPromt = True):
        otherException = self.gameList.gamerSocket(exceptionName)
        for socket in self.gameList.broadcastedGamersSockets():
            if socket != exceptionSocket and socket != otherException:
                self._send_data(type, message,socket, addServerPromt)

    def _removeGamer(self,socket):
        name = self.gameList.gamerName(socket)
        add = self.gameList.gamerAddress(socket)
        msg = "<%s> - (%s, %s) is offline" %( name, add[0], add[1])
        print("Client ",msg)
        msg = "Player " + msg
        if self.gameList.namedGamer(socket):
            self.broadcast_data("_info", msg, socket, addServerPromt = True)

        self.logger.info("Server - Client dissconected - socket : %s" %socket)
        self.gameList.removeGamer(socket)

        socket.close()

    def closeSocket(self):
        self.server_socket.shutdown(socket.SHUT_RDWR)
        self.server_socket.close()
        print("Server closed")
        self.logger.info("Server closed")


    def gamersNumber(self):
        return self.gameList.gamersNamedNumber()

    def gamersList(self):
        return self.gameList.gameNamedList()

if __name__=="__main__":
    host = 'localhost'
    port = 50015
    data_size = 1024
    msghand=MessageHandler()
    maxPlayers=2

    try:
        server=EchoGameServer(host,port,data_size,msghand,maxPlayers)
    except OSError:
        print("Adress already in use")
        sys.exit()

    count = 0
    while count < 10:
        count += 1
        x=server.handle_connection()
        if isinstance(x,tuple):
            print(x)
            msg = "<%s> >> %s"%(x[1],x[3])
            server.broadcast_data(x[2], msg, 0, x[1])
    server.closeSocket()
    time.sleep(5)