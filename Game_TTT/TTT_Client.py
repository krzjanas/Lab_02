from Game_TTT.TTT_MessageHandler import TTT_MessageHandler
from Echo.EchoClient import EchoGameClient
from TickTackToo.TickTackTooStage import TickTackTooStage, getCoordinate
import sys

stage = TickTackTooStage()

adress = 'localhost'
port = 50015
data_size = 1024

msghand = TTT_MessageHandler()

client = EchoGameClient(adress, port, data_size, msghand)

if client.status():
    client.sendName()
else:
    sys.exit()

if client.status():
    client.promt()

while client.status():

    ans = client.handle_connection()
    if ans:
        who, typ, message = ans
    else:
        continue


    if who=="S":
        # chat and information
        if typ in ("_info","_chat","_error","wrong"):
            print("\r",end="")
            print(message)
        if typ == "_start":
            stage.printStage()
            print("\r",end="")
            print(message)

        # moves
        try:
            if typ == "move_X":
                stage.setX(message)
                stage.printStage()
            if typ == "move_O":
                stage.setO(message)
                stage.printStage()
            if typ == "stage":
                stage.setStage(message)
                stage.printStage()

        except (KeyError,TypeError):
            client.sendMessage("stage","Send all stage")

        # stop game
        if typ in ("_stop","draw"):
            print("\r",end="")
            print(message)
            client.close()
            continue

        if typ == "win":
            stage.setWinLine(int(message[5]))
            stage.printStage()
            print("\r",end="")
            print(message[6:])
            client.close()
            continue
    else:
        try:
            #code from player
            code = getCoordinate(message.rstrip())
            client.sendMessage("move",message)
        except KeyError:
            #chat from player
            client.sendMessage("_chat",message)

    client.promt()


print("Finish")