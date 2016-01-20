from Game_TTT.TTT_MessageHandler import TTT_MessageHandler
from Echo.EchoServer import EchoGameServer
from TickTackToo.TickTackToo import TickTackToo, getCoordinate
import random
import time
import sys


game = TickTackToo()

host = 'localhost'
port = 50015
data_size = 1024
maxPlayers=2
msghand = TTT_MessageHandler()

try:
    server=EchoGameServer(host,port,data_size,msghand,maxPlayers)
except OSError:
    print("Adress already in use")
    sys.exit()


while server.gamersNumber() <2:
    resp = server.handle_connection()
    if resp is tuple:
        server.sendMessage("_error","Waiting on more gamers", resp[1])

print("Start game")

time.sleep(0.1)
server.broadcast_data("_start","Starting the TickTackToo game!")

pl = server.gamersList()
random.shuffle(pl)
players = {"X" : pl[0], "O" : pl[1]}

time.sleep(0.1)
server.broadcast_data("_info","Player <%s> start as X"%pl[0])


continueGame = True
while continueGame :
    if server.gamersNumber() < 2:
        print("There is not enough players to continue the game")
        server.broadcast_data("_stop", "There is not enough players to continue the game")
        continueGame = False
        continue


    ans = server.handle_connection()
    if isinstance(ans,tuple):
        numGam, gamer, msgType, msgText = ans
    else:
        continue
    print("%d - %s - %s - %s"%(numGam, gamer, msgType, msgText))



    if msgType == "_chat":
        msg = "<%s> >> %s"%(gamer,msgText)
        server.broadcast_data("_chat", msg, exceptionName=gamer, addServerPromt=False)



    if msgType == "move":
        try:
            if players['X'] == gamer:
                game.setX(msgText)
                server.broadcast_data("move_X", msgText, addServerPromt=False)
            elif players['O'] == gamer:
                game.setO(msgText)
                server.broadcast_data("move_O", msgText, addServerPromt=False)
            else:
                continue
        except KeyError:
            server.sendMessage("wrong", "Wrong typing code", gamer)
            continue
        except ZeroDivisionError:
            server.sendMessage("wrong", "Place is marked already", gamer)
            continue
        except MemoryError:
            server.sendMessage("wrong", "It is not your turn", gamer)
            continue
    if msgType == "stage":
        server.sendMessage("stage", game.getStage(), gamer, addServerPromt=False)



    if game.checkWin()[0]:
        win = ''
        lost = ''
        line = game.checkWin()[1]
        if game.checkWin()[0] == 1:
            win = 'X'
        else:
            win = 'O'
        msg = "W:%sL:%d%s            Win %s - <%s>!"%(win,line,server.serverPromt(),win,players[win])
        server.broadcast_data("win",msg, addServerPromt=False)
        continueGame = False

    if game.checkDraw():
        print("Draw!")
        server.broadcast_data("draw", "             Draw!")
        continueGame = False

server.closeSocket()


