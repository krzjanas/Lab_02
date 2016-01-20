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

try:
    server=EchoGameServer(host,port,data_size,msghand,maxPlayers)
except OSError:
    print("Adress already in use")
    sys.exit()


startMsg = "More Or Less Game: number can be found from %d to %d!"%(mol.minV,mol.maxV)

continueGame = True
while continueGame :
    ans = server.handle_connection(startMsg)
    if isinstance(ans,tuple):
        numGam, gamer, msgType, msgText = ans
    else:
        continue
    print("%d - %s - %s - %s"%(numGam, gamer, msgType, msgText))

    if msgType == "_number":
        try:
            num = int(msgText)
        except ValueError:
            continue

        res = mol.guess(num)

        if res == 0:
            server.broadcast_data("_stop", "Player <%s> win! Correct number %d"%(gamer,mol.curr))
            continueGame = False
        elif res == 1:
            server.broadcast_data("_info", "The number %d is too big"%num)
        else:
            server.broadcast_data("_info", "The number %d is too small"%num)

server.closeSocket()



