import time, sys, select
from unittest import TestCase
from mock import patch, MagicMock
from Echo.MessageHandler import MessageHandler
from Echo.EchoServer import EchoGameServer
from Echo.EchoClient import EchoGameClient

host = 'localhost'
port = 50003
data_size = 1024
msghand=MessageHandler()
maxPlayers=2


class TestEchoGameServerClient(TestCase):
    def test___init__(self):
        server=EchoGameServer(host,port,data_size,msghand,maxPlayers)
        self.assertRaises(OSError, EchoGameServer, host,port,data_size,msghand,maxPlayers)

        client1=EchoGameClient(host,port,data_size,msghand)
        self.assertTrue(client1.status())

        client2=EchoGameClient(host,port+1,data_size,msghand)
        self.assertFalse(client2.status())

    def test_NewConnection(self):
        server=EchoGameServer(host,port,data_size,msghand,maxPlayers)

        client=EchoGameClient(host,port,data_size,msghand)
        ansS = server.handle_connection()
        self.assertEqual(ansS,1)
        ansC = client.handle_connection()
        self.assertEqual(ansC,('S', '_name_request', '\\Game Server\\ Send your name'))

        self.assertEqual(server.gameList.gamersUnnamedNumber(),1)

    def test_DeinedConnection(self):
        server=EchoGameServer(host,port,data_size,msghand,0)

        client=EchoGameClient(host,port,data_size,msghand)
        ansS = server.handle_connection()
        self.assertEqual(ansS,-1)
        ansC = client.handle_connection()
        self.assertEqual(ansC,('S', '_error', '\\Game Server\\ There is too many players on serwer'))

        self.assertEqual(server.gameList.gamersUnnamedNumber(),0)

    def test_AddNametoConnection(self):
        server=EchoGameServer(host,port,data_size,msghand,1)

        self.assertEqual(server.gameList.gamersUnnamedNumber(),0)
        self.assertEqual(server.gameList.gamersNamedNumber(),0)
        client=EchoGameClient(host,port,data_size,msghand)
        server.handle_connection()
        self.assertEqual(server.gameList.gamersUnnamedNumber(),1)
        self.assertEqual(server.gameList.gamersNamedNumber(),0)

        def eff():
            client.socketStatus=False
            return "Nick"

        sys.stdin.readline = MagicMock( side_effect =eff)
        client.sendName()
        ansS = server.handle_connection()
        self.assertEqual(ansS,2)

        client.socketStatus=True
        client.sendName()

        self.assertEqual(server.gameList.gamerName(server.gameList.broadcastedGamersSockets()[0]),"Nick")
        self.assertEqual(server.gameList.gamersUnnamedNumber(),0)
        self.assertEqual(server.gameList.gamersNamedNumber(),1)

    def test_sendMessageFromClientToServer(self):

        server=EchoGameServer(host,port,data_size,msghand,1)
        client=EchoGameClient(host,port,data_size,msghand)
        server.handle_connection()
        def eff():
            client.socketStatus=False
            return "Nick"
        sys.stdin.readline = MagicMock( side_effect =eff)
        client.sendName()
        server.handle_connection()
        client.socketStatus=True
        client.sendName()

        client.sendMessage("_info","Message")
        ansS=server.handle_connection()
        self.assertEqual(ansS,(1, 'Nick', '_info', 'Message'))

    def test_sendMessageFromServerToClient(self):

        server=EchoGameServer(host,port,data_size,msghand,1)
        client=EchoGameClient(host,port,data_size,msghand)
        server.handle_connection()
        def eff():
            client.socketStatus=False
            return "Nick"
        sys.stdin.readline = MagicMock( side_effect =eff)
        client.sendName()
        server.handle_connection()
        client.socketStatus=True
        client.sendName()

        server.sendMessage("_info","Message","Nick")
        ansC = client.handle_connection()
        self.assertEqual(ansC,('S', '_info', '\\Game Server\\ Message'))

    def test_GetMessageFromConsole(self):
        server=EchoGameServer(host,port,data_size,msghand,1)
        client=EchoGameClient(host,port,data_size,msghand)

        a = select.select
        select.select = MagicMock(return_value = ([sys.stdin],0,0))
        sys.stdin.readline = MagicMock( return_value = "Message")
        ansC = client.handle_connection()
        self.assertEqual(ansC,('D', '_____', 'Message'))
        select.select = a

    def test_serverPromt(self):
      server=EchoGameServer(host,port,data_size,msghand,1)
      self.assertEqual(server.serverPromt(),'\\Game Server\\ ')

    def test_ClientStatus(self):
        client=EchoGameClient(host,port,data_size,msghand)
        client.socketStatus = False
        self.assertFalse(client.status())
        client.socketStatus = True
        self.assertTrue(client.status())

    def test_broadcast_data(self):
        server=EchoGameServer(host,port,data_size,msghand,3)
        client1=EchoGameClient(host,port,data_size,msghand)
        server.handle_connection()
        client2=EchoGameClient(host,port,data_size,msghand)
        server.handle_connection()

        def eff():
            client1.socketStatus=False
            return "Nick_1"
        sys.stdin.readline = MagicMock( side_effect = eff )
        client1.sendName()
        server.handle_connection()
        client1.socketStatus=True
        client1.sendName()

        def eff():
            client2.socketStatus=False
            return "Nick_2"
        sys.stdin.readline = MagicMock( side_effect = eff )
        client2.sendName()

        server.handle_connection()
        client2.socketStatus=True
        client2.sendName()
        ansC = client1.handle_connection()

        self.assertEqual(ansC,('S', '_info', '\\Game Server\\ Player <Nick_2> has joined the game'))

        server.broadcast_data("_info","Message")
        ansC = client1.handle_connection()
        self.assertEqual(ansC,('S', '_info', '\\Game Server\\ Message'))
        ansC = client2.handle_connection()
        self.assertEqual(ansC,('S', '_info', '\\Game Server\\ Message'))




