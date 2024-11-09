from multiprocessing.connection import Client
try: from echecs.jeu import echecs
except: from jeu import echecs
from tsanap import *
import time, sys

def main(ip_port=None):
    try:
        address = ip_port if ip_port else input("Server address: ")
        client = Client((address.split(":")[0], int(address.split(":")[1])) if ":" in address else (address, 1234))
        global ID
        ID = client.recv()
        print(f"Connected as {ID}")
        img = ... # TODO
        img.montre(1)
        if ip_port: cv2.moveWindow(img.nom, 0 if ID == 0 else 1920, 0)
        cv2.setMouseCallback(img.nom, get_mouse, m)
        fs = True if ip_port else False
        timer = time.time()
        while True: ## DONE Show image
            wk = img.montre(1, fullscreen=fs)
            if img.is_closed(): break
            match wk:
                case 27: break
                case 32: fs = not fs
                case 114: img = get_img(client)
        print("End of client program.")
        client.send("CLOSE")
        print("Game closed")
    except ConnectionRefusedError: print("Server undisponible.")
    except KeyboardInterrupt: print("\rClient stoped.")
    except EOFError: print("Server didn't respond!")
    finally:
        if replay: return main(ip_port)
        else: print("Connection ended.")

if __name__ == "__main__":
    if len(sys.argv) > 1: main(sys.argv[1])
    else: main()