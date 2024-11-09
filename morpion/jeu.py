from tsanap import *

class morpion:
    p1, p2, p3, p4 = [screen[0]/2-screen[1]/2, 0], [screen[0]/2+screen[1]/2, 0], [screen[0]/2-screen[1]/2, screen[1]], [screen[0]/2+screen[1]/2, screen[1]]
    def __init__(self, name="Morpion") -> None:
        self.name, self.trait, self.scores, self.n_parties = name, True, [0, 0], 0
        self.matrix = np.array([[0 for _ in range(3)] for _ in range(3)])
        self.ready = False
    def restart(self) -> None:
        self.n_parties += 1
        self.trait = self.n_parties%2 == 0
        self.matrix = np.array([[0 for _ in range(3)] for _ in range(3)])
    def image(self) -> image:
        p1, p2, p3, p4 = self.p1, self.p2, self.p3, self.p4
        img = image(nom=self.name, img=image.new_img(fond=col.green, dimensions=screen))
        X, Y = ([p1[i]+(p4[i]-p1[i])/3*n for n in range(3)] + [p4[i]] for i in (0, 1))
        for n, x in enumerate(X): img.ligne([x, p1[1]], [x, p4[1]], col.noir, 10 if n in range(0, 10, 3) else 3, 2)
        for n, y in enumerate(Y): img.ligne([p1[0], y], [p4[0], y], col.noir, 10 if n in range(0, 10, 3) else 3, 2)
        img.ecris(f"A {"X" if self.trait else "O"} de\njouer", ct_sg([0, 0], p3), col.blue if self.trait else col.red, 3, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
        for s, c in [[f"X: {self.scores[0]}\n", col.blue], [f"\nO: {self.scores[1]}", col.red]]: img.ecris(s, ct_sg(p2, screen), c, 3, 2, cv2.FONT_HERSHEY_SIMPLEX, 2)
        for x in range(3):
            for y in range(3):
                match self.matrix[x, y]:
                    case 1:
                        offset = dist([X[x],Y[y]],[X[x+1],Y[y]])*0.1
                        for pt1, pt2 in [[[X[x]+offset,Y[y]+offset], [X[x+1]-offset,Y[y+1]-offset]], [[X[x+1]-offset,Y[y]+offset], [X[x]+offset,Y[y+1]-offset]]]: img.ligne(pt1, pt2, col.blue, 10, 2)
                    case 2: img.cercle(ct_sg([X[x],Y[y]],[X[x+1],Y[y+1]]),dist([X[x],Y[y]],[X[x+1],Y[y]])*0.4, col.red, 10, 2)
        return img
    def winned(self) -> bool:
        possibles = [set(self.matrix[0:3, i]) for i in range(3)] + [set(self.matrix[i, 0:3]) for i in range(3)] + [set(self.matrix[i, i] for i in range(3))] + [set(self.matrix[i, 2-i] for i in range(3))]
        for cas in possibles:
            if not 0 in cas and len(cas)==1:
                self.winner = 1 if 1 in cas else 2
                self.scores[self.winner-1] += 1
                return True
        return False
    def playable(self) -> bool:
        if 0 in [c for r in self.matrix for c in r]: return True
        self.winner = None
        return False
    def play(self, pos) -> None:
        if self.matrix[pos[0],pos[1]] == 0:
            self.matrix[pos[0],pos[1]] = 1 if self.trait else 2
            self.trait = not self.trait