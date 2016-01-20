from Echo.MessageHandler import MessageHandler
from Echo.EchoClient import EchoGameClient
import sys

adress = 'localhost'
port = 50016
data_size = 1024

msghand = MessageHandler()

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
        if typ in ("_info","_start"):
            print("\r",end="")
            print(message)

        if typ =="_stop":
            print("\r",end="")
            print(message)
            client.close()
            continue

    else:
        client.sendMessage("_number",message)

    client.promt()


print("Finish")