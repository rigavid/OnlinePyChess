from params_pychess import *
import socket, chess

class Client:
    def __init__(self, host="localhost", port=PORT, name=None) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host, self.port = host, port
        self.name, self.name_adv = name, None

    def recv(self) -> str:
        data = self.client.recv(BUFS)
        if not data: raise EOFError
        msg = data.decode()
        print(f"Received: <{msg}>")
        return msg

    def send(self, msg:str) -> None:
        self.client.send(msg.encode())
        print(f"Sent: <{msg}>")

    def move(self) -> None: ## TODO Your turn
        self.send(input(f"<{self.name}> Move: "))

    def moved(self) -> None: ## TODO Opponent's move
        ...

    def get_name(self) -> str:
        if self.name == None: self.name = input("Name: ")
        if self.name == "": self.name = "_"
        return self.name

    def start(self, game:chess.Chess) -> None:
        ## Define game correctly for yourself ##
        self.client.connect((self.host, self.port))
        while True:
            command = self.recv()
            match command:
                case "wait": pass
                case "move": self.move()
                case "moved": self.moved()
                case "setname": self.name = self.recv()
                case "setnameadv": self.name_adv = self.recv()
                case "name": self.send(self.get_name())
                case "start": self.turn = bool(self.recv())
                case "quitted": self.close() ## Opponent has quited -> Victory
                case "exit": return
                case _: print(command)
    def close(self) -> None:
        self.client.close()
        print("Client closed.")

def main() -> None:
    jeu = chess.Chess()
    jeu.start(Client())

if __name__ == "__main__":
    main()