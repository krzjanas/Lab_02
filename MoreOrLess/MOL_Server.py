from MoreOrLess.MOL import MOL
from Echo.MessageHandler import MessageHandler
from Echo.EchoServer import EchoGameServer
import time
import sys

mol = MOL(1,100)

host = 'localhost'
port = 50016
data_size = 1024
maxPlayers=2
msghand = MessageHandler()