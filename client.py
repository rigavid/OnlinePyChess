from dotenv import load_dotenv, dotenv_values
import socket, chess, os, time

load_dotenv()

class Client:
    def __init__(self, host=os.getenv("HOST"), port=int(os.getenv("PORT")), name=os.getenv("NAME")) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host, self.port = host, port
        self.name, self.name_adv = name, None
        self.turn = False

    def connect(self) -> None:
        try: self.client.connect((self.host, self.port))
        except OSError: pass

    def recv(self) -> str:
        data = self.client.recv(chess.BUFS)
        if not data: raise EOFError
        msg = data.decode()
        print(f"Received: <{msg}>")
        return msg

    def send(self, msg:str) -> None:
        self.client.send(msg.encode())
        return print(f"Sent: <{msg}>")

    def move(self) -> None:
        self.game.image()
        while True:
            p1, p2 = self.game.get_move()
            if self.game.can_move(p1, p2):
                self.game.move(p1, p2)
                if chess.Server.new:
                    chess.Server.new = False
                    self.send("promotion")
                    time.sleep(0.1)
                    self.send(str(chess.Server.promotion))
                    time.sleep(0.1)
                return self.send(str((p1, p2)))

    def moved(self) -> None:
        p1, p2 = eval(self.recv())
        return self.game.move(p1, p2)

    def get_name(self) -> str:
        if self.name == None: self.name = self.game.input("Name: ")
        if self.name == "": self.name = "_"
        if self.turn: self.game.n_j1 = self.name
        else: self.game.n_j2 = self.name
        return self.name

    def promotion(self) -> None:
        chess.Server.promotion = self.recv()
        chess.Server.new = True

    def start_(self) -> None:
        self.connect()
        print("Ready to start game!")
        while self.game.img.is_opened():
            self.game.img.show()
            command = self.recv()
            match command:
                case "wait": pass
                case "move": self.move()
                case "moved": self.moved()
                case "promotion": self.promotion()
                case "setname":
                    self.name = self.recv()
                    if self.turn: self.game.n_j1 = self.name
                    else: self.game.n_j2 = self.name
                    self.game.image()
                case "setnameadv":
                    self.name_adv = self.recv()
                    if self.turn: self.game.n_j2 = self.name_adv
                    else: self.game.n_j1 = self.name_adv
                    self.game.image()
                case "name": self.send(self.get_name())
                case "start":
                    turn = eval(self.recv())
                    self.game.turn = turn
                    self.turn = turn
                    self.game.img.img = self.game.new_img()
                    self.game.image()
                case "restart":
                    self.game.restart()
                    self.turn = not self.turn
                case "quitted": return "quit"
                case "exit":
                    self.game.partie_finie()
                    return self.game.cause_fin
                case _: print(command)

    def _start_(self) -> None:
        try: return self.start_()
        except ConnectionRefusedError:
            self.host = self.game.input("Host: ")
            port = self.game.input("Port: ")
            if port.isnumeric(): self.port = int(port)
            return self.start_()

    def start(self, game:chess.Chess) -> None:
        self.game = game
        return self._start_()

    def close(self) -> None:
        self.client.close()
        print("Client closed.")

def main() -> None:
    jeu = chess.Chess()
    jeu.start(Client())

if __name__ == "__main__":
    main()