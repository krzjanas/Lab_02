import socket
import multiprocessing


HOST = '127.0.0.1'
PORT = 50045

# you can do your real staff in handler
def handler(conn, addr):
    try:
        print('processing...')
        while 1:
            data = conn.recv(1024)
            if not data:
                break
            print(data)
            conn.sendall(data)
        conn.close()
        print('processing done')
    except:
        pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
processes = []
while True:
    conn, addr = s.accept()
    print(conn, addr)

    [p.terminate() for p in processes] # to disconnect the old connection
    # start process newer connection and save it for next kill
    p = multiprocessing.Process(target=handler, args=(conn, addr))
    processes = [p]
    p.start()

    newest_conn = conn # this is the newest connection object, if you need it