from multiprocessing.connection import Listener
try: from morpion.jeu import morpion, gameEnded
except: from jeu import morpion, gameEnded
from _thread import *

def threaded_client(conn, p, gameId):
    global games
    global idCount
    conn.send(p)
    while True:
        try:
            data = conn.recv()
            if gameId in games:
                game:morpion = games[gameId]
                if not data: break
                elif data == "IMG":
                    conn.send(game.image())                   
            else: break
        except: break

    print(f"Lost connection {p}")
    try:
        del games[gameId]
        print("Closed Game", gameId)
    except: pass
    idCount -= 1
    conn.close()

def main():
    server_sock = Listener(('localhost', 1234))
    print("Server started...")
    global games
    games = {}
    global idCount
    idCount = 0
    while True:
        conn = server_sock.accept()
        idCount += 1; p = 0
        gameId = (idCount - 1)//2
        print(f"Player{gameId}.{idCount} connected.")
        if idCount % 2 == 1:
            games[gameId] = morpion(f"Morpion {gameId}")
            print("Creating a new game...")
        else: games[gameId].ready, p = True, 1
        start_new_thread(threaded_client, (conn, p, gameId))

if __name__ == "__main__":
    main()