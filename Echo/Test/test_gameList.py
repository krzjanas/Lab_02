from unittest import TestCase
from Echo.GameList import GameList, Gamer


servSocket="SocketServer"
servAdr=("AddServ_1","Port_Serv")
servName="Game Server"

ngamSocket="NamedGamerSocket"
ngamAdr=("NamedGamerAdr", "NamedGamer_Port")
ngamName="NamedGamerName"

ungamSocket="UnNamedGamerSocket"
ungamAdr=("UnNamedGamerAdr", "UnNamedGamer_Port")

def prepareGameList():
    game_server = Gamer(servSocket, servAdr)
    game_server.name = servName
    gameList = GameList(game_server)
    return gameList

def addNamedGamer(gameList):
    gameList.addGamer(ngamSocket, ngamAdr)
    gameList.addGamerName(ngamSocket, ngamName)

def addUnNamedGamer(gameList):
    gameList.addGamer(ungamSocket, ungamAdr)


class TestGameList(TestCase):
    def test_isServerSocket(self):
        gameList = prepareGameList()
        self.assertTrue(gameList.isServerSocket(servSocket))

    def test_serverName(self):
        gameList = prepareGameList()
        self.assertEqual(gameList.serverName(),servName)

    def test_namedGamer(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertTrue(gameList.namedGamer(ngamSocket))
        self.assertFalse(gameList.namedGamer("SS"))
        self.assertFalse(gameList.namedGamer(ungamSocket))



    def test_unnamedGamer(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertFalse(gameList.unnamedGamer(ngamSocket))
        self.assertFalse(gameList.unnamedGamer("SS"))
        self.assertTrue(gameList.unnamedGamer(ungamSocket))

    def test_addGamer(self):
        gameList = prepareGameList()
        gameList.addGamer(ngamSocket, ngamAdr)
        self.assertFalse(gameList.namedGamer(ngamSocket))
        self.assertTrue(gameList.unnamedGamer(ngamSocket))

    def test_addGamerName(self):
        gameList = prepareGameList()
        gameList.addGamer(ngamSocket, ngamAdr)

        self.assertEqual(gameList.addGamerName(ngamSocket, ngamName), 1)
        self.assertEqual(gameList.gamerName(ngamSocket), ngamName)

        self.assertEqual(gameList.addGamerName(ngamSocket, ngamName), -1)
        self.assertEqual(gameList.addGamerName(ngamSocket, servName), -1)

        self.assertEqual(gameList.addGamerName(ungamSocket, "L"), 0)


    def test_removeGamer(self):
        gameList = prepareGameList()
        gameList.removeGamer("Nic")
        addNamedGamer(gameList)
        self.assertTrue(gameList.namedGamer(ngamSocket))
        gameList.removeGamer(ngamSocket)
        self.assertFalse(gameList.namedGamer(ngamSocket))
        addUnNamedGamer(gameList)
        self.assertTrue(gameList.unnamedGamer(ungamSocket))
        gameList.removeGamer(ungamSocket)
        self.assertFalse(gameList.unnamedGamer(ungamSocket))


    def test_gamerName(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertEqual(gameList.gamerName(ngamSocket), ngamName)
        self.assertEqual(gameList.gamerName(ungamSocket), "")
        self.assertEqual(gameList.gamerName("DDD"), "")


    def test_gamerAddress(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertEqual(gameList.gamerAddress(ngamSocket), ngamAdr)
        self.assertEqual(gameList.gamerAddress(ungamSocket), ungamAdr)
        self.assertEqual(gameList.gamerAddress("DDD"), (0,0))

    def test_gamerSocket(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertEqual(gameList.gamerSocket(ngamName), ngamSocket)
        self.assertEqual(gameList.gamerSocket("DDD"), 0)

    def test_getGamerAccSocket(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        g = Gamer(ngamSocket,ngamAdr)
        g.name = ngamName
        self.assertEqual(gameList.getGamerAccSocket(ngamSocket).socket, g.socket)
        self.assertEqual(gameList.getGamerAccSocket(ngamSocket).address, g.address)
        self.assertEqual(gameList.getGamerAccSocket(ngamSocket).name, g.name)

        ug = Gamer(ungamSocket,ungamAdr)
        self.assertEqual(gameList.getGamerAccSocket(ungamSocket).socket, ug.socket)
        self.assertEqual(gameList.getGamerAccSocket(ungamSocket).address, ug.address)
        self.assertEqual(gameList.getGamerAccSocket(ungamSocket).name, ug.name)

        self.assertEqual(gameList.getGamerAccSocket("L:L"), 0)

    def test_getGamerAccName(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)

        g = Gamer(ngamSocket,ngamAdr)
        g.name = ngamName

        self.assertEqual(gameList.getGamerAccName(ngamName).socket, g.socket)
        self.assertEqual(gameList.getGamerAccName(ngamName).address, g.address)
        self.assertEqual(gameList.getGamerAccName(ngamName).name, g.name)

        self.assertEqual(gameList.getGamerAccName("kkk"), 0)


    def test_gamersNamedNumber(self):
        gameList = prepareGameList()
        self.assertEqual(gameList.gamersNamedNumber(),0)
        addNamedGamer(gameList)
        self.assertEqual(gameList.gamersNamedNumber(),1)

    def test_gamersUnnamedNumber(self):
        gameList = prepareGameList()
        self.assertEqual(gameList.gamersUnnamedNumber(),0)
        addUnNamedGamer(gameList)
        self.assertEqual(gameList.gamersUnnamedNumber(),1)

    def test_connectedGamersSockets(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertEqual(gameList.connectedGamersSockets(),[servSocket,ngamSocket,ungamSocket])

    def test_broadcastedGamersSockets(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertEqual(gameList.broadcastedGamersSockets(),[ngamSocket])

    def test_gameNamedList(self):
        gameList = prepareGameList()
        addNamedGamer(gameList)
        addUnNamedGamer(gameList)
        self.assertEqual(gameList.gameNamedList(),[ngamName])
