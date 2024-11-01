from vars import SERVER_IP
import socket
from _thread import *
import pickle
from game import Game

server = SERVER_IP
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: s.bind((server, port))
except socket.error as e: str(e)

s.listen(3) ## Specifies the number of unaccepted connections that the system will allow before refusing new connections
print("Server Started...")

games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()
            if gameId in games:
                game = games[gameId]
                if not data: break
                else:
                    if data == "reset": game.resetWent()
                    elif data != "get": game.play(p, data)
                    conn.sendall(pickle.dumps(game))
            else: break
        except: break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closed Game", gameId)
    except: pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    idCount += 1; p = 0
    gameId = (idCount - 1)//2
    
    print("Connected to:", addr)
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else: games[gameId].ready, p = True, 1
    start_new_thread(threaded_client, (conn, p, gameId))