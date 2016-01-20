import socket, select, sys, logging
from Echo.MessageHandler import MessageHandler

class EchoGameClient:
    def __init__(self, address, port, recv_buffer, messageHandler, timeout=2):
        self.recv_buffer=recv_buffer
        self.messageHandler=messageHandler
        self.name=""
        self._setLogger()
        self.logger.info("Client <%s>: create client"%self.name)

        self._createTcpIpSocket(timeout)
        self._connectToServer(address,port)



    def _createTcpIpSocket(self,timeout):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)

    def _connectToServer(self,address,port):
        server_address = (address, port)
        print('connecting to %s port %s' % server_address)
        self.socketStatus=True
        try:
            self.socket.connect(server_address)
            print('Connected to remote host')
            self.logger.info("Client <%s>: connected to remote host (%s,%s)"%(self.name,address, port))
        except :
            print('Unable to connect')
            self.logger.info("Client <%s>: unable to connect to remote host (%s,%s)"%(self.name,address, port))
            self.socketStatus=False

    def _setLogger(self):
        self.fh_serv = logging.FileHandler('EchoClient.log')
        self.fh_serv.setLevel(logging.DEBUG)
        self.fh_serv.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
        self.logger = logging.getLogger('EchoClient_log')
        self.logger.addHandler(self.fh_serv)
        self.logger.setLevel(logging.DEBUG)

    def status(self):
        return self.socketStatus

    def sendName(self):
        unnamed = True
        while unnamed and self.socketStatus:
            read_sockets, write_sockets, error_sockets = select.select([self.socket], [], [])
            if self.socket in read_sockets:
                data = self._receive_data()
                if data:
                    if data[0] == "_name_request":
                        self.logger.info("Client <%s>: name requested"%self.name)
                        print(data[1])
                        print("\r>Your name: ", end=" ")
                        self.name = sys.stdin.readline().rstrip()
                        self.sendMessage("_name",self.name)
                    if data[0] == "_name_accepted":
                        print("\r%s"%data[1])
                        unnamed=False
                        self.logger.info("Client <%s>: name accepted"%self.name)


        return not unnamed

    def _receive_data(self):
        try:
            data = self.socket.recv(self.recv_buffer)
            if data:
                msg = self.messageHandler.decodeMessage(data)
                self.logger.info("Client <%s>: receive message:\n\tType: %s \tMessage: %s"%(self.name, msg[0], msg[1]))
                return msg
            else:
                self.logger.info("Client <%s>: message receiving interuppted" %self.name)
                self.close()
                return 0

        except (InterruptedError,ConnectionResetError):
            self.logger.info("Client <%s>: message receiving interuppted" %self.name)
            self.close()
            return 0

    def sendMessage(self, type, message):
        msg = self.messageHandler.encodeMessage(type, message)
        try :
            self.socket.send(msg)
            self.logger.info("Client <%s>: send message:\n\tType: %s \tMessage: %s"%(self.name, type, message))
        except (InterruptedError,ConnectionResetError):
            self.logger.info("Client <%s>: message sending interuppted" %self.name)
            self.close()

    def handle_connection(self):
        if self.socketStatus:
            read_sockets, write_sockets, error_sockets = select.select([sys.stdin, self.socket], [], [])

            for sock in read_sockets:
                if sock == self.socket:
                    data = self._receive_data()
                    if data:
                        return "S",data[0],data[1]
                else:
                    msg = sys.stdin.readline()
                    return "D","_____",msg

        return 0


    def close(self):
        if self.socketStatus:
            self.socket.close()
            self.socketStatus=False
            print('\rDisconnected from chat server')
            self.logger.info("Client <%s>: Disconnected from chat server" %self.name)

    def promt(self):
        sys.stdout.write("\r<%s> >> "%self.name)
        sys.stdout.flush()

if __name__=="__main__":
    host = 'localhost'
    port = 50015
    data_size = 1024
    msghand=MessageHandler()
    client=EchoGameClient(host,port,data_size,msghand)
    print(client.status())
    if client.status():
        client.sendName()

    if client.status():
        client.promt()

    while client.status():

        ans = client.handle_connection()
        if ans:
            if ans[0]=="S":
                print("\r",end="")
                print(ans[2])
            else:
                client.sendMessage("_chat",ans[2])
            client.promt()

