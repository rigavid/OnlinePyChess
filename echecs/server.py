from multiprocessing.connection import Listener
try: from jeu import morpion
except: from morpion.jeu import morpion
import socket
from _thread import *

SERVER_IP, SERVER_PORT = socket.gethostbyname(socket.gethostname()), 1234

def threaded_client(conn, p, gameId):
    global games, idCount
    conn.send(p)
    while True:
        try:
            data = conn.recv()
            print(f"Player {gameId}.{p}: {data}")
            if gameId in games:
                game:morpion = games[gameId]
                if not data: break
                elif data == "GET": conn.send(game)
                elif data == "IMG": conn.send(game.image())
                elif data == "MOVE":
                    t = game.trait
                    game.play(conn.recv())
                    conn.send(t != game.trait)
                elif data == "STATUS":
                    if game.playable() and not game.winned():
                        conn.send((True, game.trait))
                    else: conn.send((False, game.winner))
                elif data == "CLOSE":
                    try:
                        del games[gameId]
                        print(f"Game {gameId} closed.")
                    except: pass
            elif data == "STATUS": conn.send([False])
            else: break
        except: break
    print(f"Lost connection {gameId}.{p}")
    idCount -= 1
    conn.close()

def main():
    try:
        server_sock = Listener((SERVER_IP, SERVER_PORT))
        print(f"Server started at {":".join(str(i) for i in server_sock.address)} ...")
        global games, idCount
        games, idCount = {}, 0
        while True:
            conn = server_sock.accept()
            idCount += 1; p = 0
            gameId = (idCount - 1)//2
            if idCount % 2 == 1:
                games[gameId] = morpion(f"Morpion {gameId}")
                print("Creating a new game...")
            else: games[gameId].ready, p = True, 1
            print(f"Player {gameId}.{p} connected.")
            start_new_thread(threaded_client, (conn, p, gameId))
    except KeyboardInterrupt: print("\rStopping server...")
    finally: print("Server stoped.")

if __name__ == "__main__":
    main()