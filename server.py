from dotenv import load_dotenv, dotenv_values
import socket, select, time, chess, os
from _thread import start_new_thread

load_dotenv()
PORT = int(os.getenv("PORT"))
BUFS = chess.BUFS
WAIT = 0.1

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
        print(f"Server started on port {self.port}. Waiting for connections...")
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

    def start_game(self, game, c1, c2, turn=True) -> str:
        print("Starting game turn's:", turn)
        told = False
        playing = True
        try:
            while playing:
                readable, writable, in_error = select.select((c1, c2), (c1, c2), (c1, c2), 2)
                for r in readable:
                    if not r.recv(BUFS):
                        if r==c1: c2.send("quitted".encode())
                        else: c1.send("quitted".encode())
                        playing = False
                        break
                if told:
                    try:
                        if turn: c = c1 if game.trait else c2
                        else: c = c2 if game.trait else c1
                        data = c.recv(BUFS)
                        move = eval(data.decode())
                        print(f"Received: <{move}>")
                        game.move(*move)
                        c = c1 if c2==c else c2
                        c.send("moved".encode())
                        time.sleep(WAIT)
                        c.send(data)
                        time.sleep(WAIT)
                        told = False
                        if game.partie_finie():
                            raise chess.EndGame
                    except TimeoutError:
                        if turn: c = c2 if game.trait else c1
                        else: c = c1 if game.trait else c2
                        print("Timeout:", turn, game.trait)
                        c.send("wait".encode())
                        continue
                else:
                    time.sleep(WAIT)
                    if turn: c = c1 if game.trait else c2
                    else: c = c2 if game.trait else c1
                    c.send("move".encode())
                    told = True
        except chess.EndGame: return game.cause_fin
        raise chess.StopGame

    def game_thread(self, c1:socket.socket, c2:socket.socket, gameID) -> None:
        for c in (c1, c2): c.send("start".encode())
        time.sleep(WAIT)
        c1.send("True".encode())
        c2.send("False".encode())
        time.sleep(WAIT)
        for c in (c1, c2): c.send("name".encode())
        nj1, nj2 = (c.recv(BUFS).decode() for c in (c1, c2))
        if nj1 == "_":
            nj1 = "Player1" if nj2 != "Player1" else "Player2"
            c1.send("setname".encode())
            time.sleep(WAIT)
            c1.send(nj1.encode())
        if nj2 == "_":
            nj2 = "Player2" if nj1 != "Player2" else "Player1"
            c2.send("setname".encode())
            time.sleep(WAIT)
            c2.send(nj2.encode())
        time.sleep(0.1)
        c1.send("setnameadv".encode())
        c2.send("setnameadv".encode())
        time.sleep(WAIT)
        c1.send(nj2.encode())
        c2.send(nj1.encode())
        game = chess.Chess(name=f"PyChess - {gameID}", j1=nj1, j2=nj2)
        self.games[gameID] = game
        time.sleep(WAIT)
        c1.setblocking(False)
        c2.setblocking(False)
        c1.settimeout(1)
        c2.settimeout(1)
        games = 0
        while True:
            try:
                cause_end = self.start_game(game, c1, c2, games%2==0)
                time.sleep(WAIT)
                for c in (c1, c2): c.send("exit".encode())
                c1.settimeout(60)
                c2.settimeout(60)
            except (ConnectionResetError, BrokenPipeError) as e:
                try: c2.send("quitted".encode())
                except: pass
                try: c1.send("quitted".encode())
                except: pass
            try:
                r1, r2 = eval(c1.recv(BUFS).decode()), eval(c2.recv(BUFS).decode())
                replay = r1 and r2
                if not replay:
                    if r1: c1.send("False".encode())
                    if r2: c2.send("False".encode())
                    break
                for c in (c1, c2): c.send("True".encode())
                time.sleep(WAIT)
                c1.settimeout(1)
                c2.settimeout(1)
                game.restart()
            except TimeoutError: break
            games += 1
        c1.close()
        c2.close()

def main() -> None:
    server = Server()
    try: server.start()
    except Exception as e: print(e)
    finally: server.close()

if __name__ == "__main__":
    main()