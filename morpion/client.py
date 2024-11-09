from multiprocessing.connection import Client
try: from morpion.jeu import morpion
except: from jeu import morpion
from tsanap import *
import time, sys

class mouse: click = False
get_case = lambda x, y, m: (int((x-m.p1[0])/dist(m.p1, m.p2)*3), int((y-m.p1[1])/dist(m.p1, m.p3)*3))
def get_mouse(event, x, y, flags, morp) -> None:
    global ID
    if morp.trait == bool(ID):
        if event == cv2.EVENT_LBUTTONDOWN and clicked_in([x, y], [morp.p1, morp.p4]): mouse.case = get_case(x, y, morp)
        elif event == cv2.EVENT_LBUTTONUP and clicked_in([x, y], [morp.p1, morp.p4]) and get_case(x, y, morp) == mouse.case: mouse.click = True
def mouse_replay(event, x, y, flags, params) -> None:
    if clicked_in((x,y), params): mouse.click, mouse.replay = True, True

def request(cli:Client, req:str):
    cli.send(req)
    return cli.recv()
def image_of(m:morpion) -> image:
    global ID
    img = m.image()
    img.nom = f"{img.nom}.{ID}"
    return img
def get_img(cli:Client) -> image:
    global ID
    img:image = request(cli, "IMG")
    img.nom = f"{img.nom}.{ID}"
    return img
def get_game(cli:Client) -> morpion:
    return request(cli, "GET")

def main(ip_port=None):
    try:
        replay = False
        address = ip_port if ip_port else input("Server address: ")
        client = Client((address.split(":")[0], int(address.split(":")[1])) if ":" in address else (address, 1234))
        global ID
        ID = client.recv()
        print(f"Connected as {ID}")
        m = get_game(client)
        img = image_of(m)
        img.montre(1)
        if ip_port: cv2.moveWindow(img.nom, 0 if ID == 0 else 1920, 0)
        cv2.setMouseCallback(img.nom, get_mouse, m)
        fs = True if ip_port else False
        timer = time.time()
        while True:
            wk = img.montre(1, fullscreen=fs)
            if img.is_closed(): break
            match wk:
                case 27: break
                case 32: fs = not fs
                case 114: img = get_img(client)
            if m.ready:
                if mouse.click: ## Play
                    client.send("MOVE")
                    if request(client, mouse.case):
                        m = request(client, "GET")
                        img = image_of(m)
                    mouse.click = False
                if m.trait != bool(ID) and diff(timer, time.time()) > 1: ## While the other plays
                    data = request(client, "STATUS")
                    if len(data) == 2:
                        playable, trait = data
                        if not playable:
                            print("Unplayable game")
                        elif m.trait != trait:
                            m:morpion = request(client, "GET")
                            img = image_of(m)
                            cv2.setMouseCallback(img.nom, get_mouse, m)
                    else: # TODO
                        mouse.click = False
                        img = get_img(cli)
                        img.ecris("Replay?", ct, col.black, 5, 3, cv2.FONT_HERSHEY_SIMPLEX, 2)
                        p1, p2 = ct_cg(cg, ct_sg(ch, ct)), ct_cg(cd, ct_sg(cb, ct))
                        cv2.setMouseCallback(img.nom, mouse_replay, (p1, p2))
                        while not img.is_closed():
                            wk = img.montre(1, fullscreen=fs)
                            match wk:
                                case 27: return
                                case 32: fs = not fs
                            if mouse.click:
                                replay = mouse.replay
                                break
                        break
                    timer = time.time()
            elif diff(timer, time.time()) > 1:
                m:morpion = request(client, "GET")
                timer = time.time()
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