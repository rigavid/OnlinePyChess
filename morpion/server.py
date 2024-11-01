try: from morpion.jeu import morpion, gameEnded
except: from jeu import morpion, gameEnded
import socket, pickle
from _thread import *
from tsanap import *

class mouse: click = False
get_case = lambda x, y, m : (int((x-m.p1[0])/dist(m.p1, m.p2)*3), int((y-m.p1[1])/dist(m.p1, m.p3)*3))
def get_mouse(event, x, y, flags, param) -> None:
    if event == cv2.EVENT_LBUTTONDOWN and clicked_in([x, y], [param.p1, param.p4]): mouse.case = get_case(x, y, param)
    elif event == cv2.EVENT_LBUTTONUP and clicked_in([x, y], [param.p1, param.p4]) and get_case(x, y, param) == mouse.case: mouse.click = True

def main_():
    m = morpion()
    img = m.image()
    fs = False
    img.montre(1)
    cv2.setMouseCallback(img.nom, get_mouse, m)
    while not img.is_closed():
        wk = img.montre(1, fullscreen=fs)
        match wk:
            case 27: return
            case 32: fs = not fs
        if mouse.click:
            try:
                m.play(mouse.case)
                img = m.image()
            except gameEnded:
                img = m.image()
                img.ecris("Tied game!" if m.winner == None else f"Player {m.winner} won!", ct_sg(m.p1, m.p4), col.black, 10, 3, cv2.FONT_HERSHEY_SIMPLEX, 2)
                mouse.click = False
                while not img.is_closed():
                    wk = img.montre(1, fs)
                    match wk:
                        case 27: return
                        case 32: fs = not fs
                        case -1: ...
                        case _: break
                    if mouse.click: break
                m.restart()
                img = m.image()
            mouse.click = False

def main(SERVER_IP, port) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: s.bind((server, port))
    except socket.error as e: str(e)
    s.listen(3)
    print("Server started...")
    games = {}
    id_count = 0
    while True:
        conn, addr = s.accept()
        idCount += 1; p = 0
        gameId = (idCount - 1)//2
        
        print("Connected to:", addr)
        if idCount % 2 == 1:
            games[gameId] = morpion(f"Morpion {gameId}")
            print("Creating a new game...")
        else: games[gameId].ready, p = True, 1
        start_new_thread(threaded_client, (conn, p, gameId))
    return

if __name__ == "__main__":
    #main_()
    SERVER_IP = "10.52.4.144"
    port = 5555
    main(SERVER_IP, port)
    ...