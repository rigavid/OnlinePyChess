from multiprocessing.connection import Client
import time

def main():
    client = Client((input("Server ip: "), input("Server port: ")))
    id = client.recv()
    print(f"Connected as {id}")
    client.send("IMG")
    img = client.recv()
    fs = False
    while True:
        wk = img.montre(1, fullscreen=fs)
        if img.is_closed(): break
        match wk:
            case 27: break
            case 32: fs = not fs
    

if __name__ == "__main__":
    try: main()
    except ConnectionRefusedError:
        print("Server undisponible.")
    # except EOFError:
    #     print("Server disconnected.")