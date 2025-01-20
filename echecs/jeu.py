###################
## Author: David ##
## Date: 9/11/24 ##
###################

from pyimager import *

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
        img = new_img(self.res, COL.cyan, "PyChess")
        img.rectangle(p1, p4, COL.new("DEB887"), 0, 2) ## Plateau
        for a, b in ((p1, pt1), (p2, pt2), (p3, pt3), (p4, pt4)): ## Coins du plateau
            img.rectangle(a, b, COL.new("80360a"), 0, 2)
            img.rectangle(a, b, COL.black, 5, 2)
        img.rectangle(p1, p4, COL.black, 6, 2) 
        img.rectangle(pt1, pt4, COL.black, 6, 2)
        return img

def main():
    resolutions = [(1920, 1080), (1680, 1050)]; r_i = 0
    jeu = echecs()
    print(jeu)
    img = jeu.image()
    img.build()
    img.setMouseCallback(get_mouse, [jeu])
    while img.is_opened():
        wk = img.show(1)
        match wk:
            case 8:
                r_i += 1
                jeu.resolution(resolutions[r_i%len(resolutions)])
                img, fs = jeu.image(), img.fullscreen
                img.fullscreen = fs

if __name__ == "__main__":
    main()