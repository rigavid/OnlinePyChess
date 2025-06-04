from params_pychess import *
from _thread import start_new_thread
import socket, select, time, chess

class Server:
    def new_game_id(self) -> str:
        id = len(self.games)
        while str(id) in self.games.keys():
            id += 1
        return str(id)

    def new_game(self, conn, gameID):
        self.games[gameID] = conn

    def __init__(self, host="", port=PORT) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host, self.port = host, port
        self.clients = []
        self.games = {}
        self.waiting = []

    def start(self, conections=2):
        self.server.bind((self.host, self.port))
        self.server.listen(conections)
        print("Server started. Waiting for connections...")
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            if len(self.clients) < 2:
                start_new_thread(self.client_thread, (conn, self.new_game_id()))
            else:
                gameID = self.waiting.pop(0)
                c1 = self.clients.pop(self.clients.index(self.games[gameID]))
                c2 = self.clients.pop(self.clients.index(conn))
                start_new_thread(self.game_thread, (c1, c2, gameID))
            print(f"{len(self.clients)} players waiting.")

    def close(self) -> None:
        self.server.close()

    def client_thread(self, conn:socket.socket, gameID) -> None:
        self.new_game(conn, gameID)
        self.waiting.append(gameID)
        while gameID in self.waiting: ## Wait for connection
            conn.send("wait".encode())
            time.sleep(0.1)

    def game_thread(self, c1:socket.socket, c2:socket.socket, gameID) -> None:
        for c in (c1, c2): c.send("name".encode())
        nj1, nj2 = (c.recv(BUFS).decode() for c in (c1, c2))
        if nj1 == "_":
            nj1 = "Player1" if nj2 != "Player1" else "Player2"
            c1.send("setname".encode())
            time.sleep(0.01)
            c1.send(nj1.encode())
        if nj2 == "_":
            nj2 = "Player2" if nj1 != "Player2" else "Player1"
            c2.send("setname".encode())
            time.sleep(0.01)
            c2.send(nj2.encode())
        c1.send("setnameadv".encode())
        c2.send("setnameadv".encode())
        time.sleep(0.01)
        c1.send(nj2.encode())
        c2.send(nj1.encode())
        game = chess.Chess(name=f"PyChess - {gameID}", j1=nj1, j2=nj2)
        self.games[gameID] = game
        print(game.__game_info__())
        for c in (c1, c2): c.send("start".encode())
        time.sleep(0.01)
        c1.send("True".encode())
        c2.send("False".encode())
        playing = True
        while playing:
            c = c1 if game.trait else c2
            c.send("move".encode())
            move = eval(c.recv(BUFS).decode())
            game.move(*move)
            readable, writable, in_error = select.select((c1, c2), (c1, c2), (c1, c2), 30)
            for r in readable:
                if not r.recv(BUFS):
                    if r==c1: c2.send(b"quitted")
                    else: c2.send(b"quitted")
                    playing = False
                    break
        c1.close()
        c2.close()

def main() -> None:
    server = Server()
    try: server.start()
    except Exception as e: print(e)
    finally: server.close()

if __name__ == "__main__":
    main()