###################
## Author: David ##
## Date: 9/11/24 ##
###################

from tsanap import *

def new_matrix() -> np.array:
    P = "t._c_f_d_r._f_c_t."
    matrix = [P.split("_")] + [["p"]*8] + [[" "]*8]*4 + [["P"]*8] + [P.upper().split("_")]
    return np.array(matrix, np.str_)

class echecs:
    def __init__(self) -> None:
        self.trait = True
        self.matrix = new_matrix()
    def __str__(self) -> str:
        return "┌"+"───┬"*7+"───┐\n│ " + str(" │\n├"+"───┼"*7+"───┤\n│ ").join(" │ ".join(el[0] for el in row) for row in self.matrix) + " │\n└"+"───┴"*7+"───┘"

jeu = echecs()
print(jeu)