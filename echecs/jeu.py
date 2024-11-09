###################
## Author: David ##
## Date: 9/11/24 ##
###################

from tsanap import *

class mouse: click, case = False, None
def get_mouse(event, x, y, flags, params) -> None:
    echecs = params[0]
    if event == cv2.EVENT_LBUTTONDOWN and clicked_in((x,y), (echecs.p1, echecs.p2)):
        mouse.case = get_case(x, y, echecs)

def new_matrix() -> np.array:
    P = "t._c_f_d_r._f_c_t."
    matrix = [P.split("_")] + [["p"]*8] + [[" "]*8]*4 + [["P"]*8] + [P.upper().split("_")]
    return np.array(matrix, np.str_)

class echecs:
    def __init__(self) -> None:
        self.trait, self.captures, self.matrix = True, [], new_matrix()
        self.resolution()
    def __str__(self) -> str:
        return "┌"+"───┬"*7+"───┐\n│ " + str(" │\n├"+"───┼"*7+"───┤\n│ ").join(" │ ".join(el[0] for el in row) for row in self.matrix) + " │\n└"+"───┴"*7+"───┘"
    def resolution(self, res=screen) -> None:
        o_x, o_y = (res[0]-res[1])/2, 0
        self.p1, self.p2, self.p3, self.p4 = (o_x, o_y), (res[0]-o_x, o_y), (o_x, res[1]-o_y), (res[0]-o_x, res[1]-o_y)
        i = sum(res)/33; o_x += i; o_y += i
        self.pt1,self.pt2,self.pt3,self.pt4= (o_x, o_y), (res[0]-o_x, o_y), (o_x, res[1]-o_y), (res[0]-o_x, res[1]-o_y)
        self.res = res
    def image(self) -> image:
        p1, p2, p3, p4, pt1, pt2, pt3, pt4 = self.p1, self.p2, self.p3, self.p4, self.pt1, self.pt2, self.pt3, self.pt4
        img = image(img=image.new_img(dimensions=self.res, fond=col.cyan))
        img.rectangle(p1, p4, col.new("DEB887"), 0, 2) ## Plateau
        for a, b in ((p1, pt1), (p2, pt2), (p3, pt3), (p4, pt4)): ## Coins du plateau
            img.rectangle(a, b, col.new("80360a"), 0, 2)
            img.rectangle(a, b, col.black, 5, 2)
        img.rectangle(p1, p4, col.black, 6, 2) 
        img.rectangle(pt1, pt4, col.black, 6, 2)
        return img

def main():
    resolutions = [(1920, 1080), (1680, 1050)]; r_i = 0
    jeu = echecs()
    print(jeu)
    img, fs = jeu.image(), False
    img.montre(1)
    cv2.setMouseCallback(img.nom, get_mouse)
    while not img.is_closed():
        wk = img.montre(1, fullscreen=fs)
        match wk:
            case 27: return
            case 32: fs = not fs
            case 8:
                r_i += 1
                jeu.resolution(resolutions[r_i%len(resolutions)])
                img = jeu.image()
            case 65470: cv2.moveWindow(img.nom, 0, 0) # f1
            case 65471: cv2.moveWindow(img.nom, 1920, 0) # f1
            case -1: ...
            case _: print(wk)

if __name__ == "__main__":
    main()