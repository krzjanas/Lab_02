class Gamer:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.name = ""

class GameList:
    def __init__(self, game_server):
        self.game_server = game_server
        self.named_list = []
        self.unnamed_list = []

    def isServerSocket(self, socket):
        return self.game_server.socket == socket

    def serverName(self):
        return self.game_server.name

    def namedGamer(self,socket):
        for gamer in self.named_list:
            if gamer.socket == socket:
                return True
        return False

    def unnamedGamer(self,socket):
        for gamer in self.unnamed_list:
            if gamer.socket == socket:
                return True
        return False

    def addGamer(self, socket, address):
        self.unnamed_list.append( Gamer(socket, address) )

    def addGamerName(self,socket, name):
        if self.game_server.name == name:
            return -1
        for gamer in self.named_list:
            if gamer.name == name:
                return -1
        for gamer in self.unnamed_list:
            if gamer.socket == socket:
                gamer.name = name
                self.named_list.append(gamer)
                self.unnamed_list.remove(gamer)
                return 1
        return 0

    def removeGamer(self, socket):
        for gamer in self.named_list:
            if gamer.socket == socket:
                self.named_list.remove(gamer)
                continue
        for gamer in self.unnamed_list:
            if gamer.socket == socket:
                self.unnamed_list.remove(gamer)
                continue

    def gamerName(self, socket):
        for gamer in self.named_list:
            if gamer.socket == socket:
                return gamer.name
        else:
            return ""

    def gamerAddress(self, socket):
        for gamer in self.named_list:
            if gamer.socket == socket:
                return gamer.address
        for gamer in self.unnamed_list:
            if gamer.socket == socket:
                return gamer.address
        return (0,0)

    def gamerSocket(self, name):
        for gamer in self.named_list:
            if gamer.name == name:
                return gamer.socket
        else:
            return 0

    def getGamerAccSocket(self, socket):
        for gamer in self.named_list:
            if gamer.socket == socket:
                return gamer
        for gamer in self.unnamed_list:
            if gamer.socket == socket:
                return gamer
        return 0

    def getGamerAccName(self, name):
        for gamer in self.named_list:
            if gamer.name == name:
                return gamer
        return 0

    def gamersNamedNumber(self):
        return len(self.named_list)

    def gamersUnnamedNumber(self):
        return len(self.unnamed_list)

    def connectedGamersSockets(self):
        socketList = []
        socketList.append(self.game_server.socket)
        for gamer in self.named_list:
            socketList.append(gamer.socket)
        for gamer in self.unnamed_list:
            socketList.append(gamer.socket)
        return socketList

    def broadcastedGamersSockets(self):
        socketList = []
        for gamer in self.named_list:
            socketList.append(gamer.socket)
        return socketList

    def gameNamedList(self):
        nameList=[]
        for gamer in self.named_list:
            nameList.append(gamer.name)
        return nameList