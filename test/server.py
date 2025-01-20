from multiprocessing.connection import Listener
from _thread import *
import socket

SERVER_IP, SERVER_PORT = socket.gethostbyname(socket.gethostname()), 1234

def threaded_client(conn, ID):
    conn.send(f"Connected as {ID}")
    print(f"{ID} has connected")
    while True:
        try:
            data = conn.recv()
            for c in connetions:
                c.send(data)
        except: break
    conn.close()

def main():
    global connetions
    connections = []
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
    try:
        server_sock = Listener((SERVER_IP, SERVER_PORT))
        while True:
            conn = server_sock.accept()
            connections.append(conn)
            start_new_thread(threaded_client, (conn, connections.index(conn)))
    except KeyboardInterrupt: print("\rStopping server...")
    finally: print("Server stoped.")

if __name__ == "__main__":
    main()