from start import table
from math import log2
import os

class BDD:
    def __init__(self, val ,left=None , right =None, luka = None) -> None:
        self.val = val
        self.left = left
        self.right = right
        self.luka = luka
    def __repr__(self) -> str:
        return f"BDD [ val:{self.val}, left: {self.left},right: {self.right}, luka :{self.luka}]"
    #retourne true si je suis une fueille
    def leaf(self):
        return self.right is None and self.left is None


def cons_arbre(T:list)->BDD:
    if len(T)==0:
        return None
    mid =len(T)//2
    height= log2(len(T))
    if height == 0:
        return BDD(T[0])
    else:
        return BDD(f'x{int(height)}',cons_arbre(T[:mid]),cons_arbre(T[mid:]))

def luka (T:BDD)->str:
    if T.leaf() :
        T.luka = str(T.val)
        return T.luka
    else:
        T.luka=f"{T.val}({luka(T.left)})({luka(T.right)})"
        return T.luka

#Parcours suffix compression
def suffix_compression(n, D):
    if n:
        D = suffix_compression(n.left, D)
        D = suffix_compression(n.right, D)
        if n.luka not in D:
            if n.leaf():
                D[n.luka] = BDD(n.val)
            else:
                D[n.luka] = BDD(n.val, D[n.left.luka], D[n.right.luka])
    return D
        
#hypothèse: luka a déjà été appelé sur T
def compression(T:BDD):
    if T is None:
        return None
    luka(T)
    D = suffix_compression(T, dict())
    return D[T.luka]

def suffix_bdd(n,D):
    if n:
        if n.leaf():
            if n.luka not in D:
                D[n.luka] = BDD(n.val)
        else:
            D = suffix_bdd(n.left, D)
            D = suffix_bdd(n.right, D)
            if D[n.left.luka] == D[n.right.luka]:
                D[n.luka] = D[n.left.luka]
            elif n.luka not in D:
                D[n.luka] = BDD(n.val, D[n.left.luka], D[n.right.luka])
    return D

def compression_bdd(T:BDD):
    if T is None:
        return None
    luka(T)
    D = suffix_bdd(T, dict())
    return D[T.luka]

#traverse l'abre pour la fonction dot
def traversal(n, D):
    res = ""
    if n:
        if n not in D:
            pos = len(D)
            res += str(pos) + " [ label = \"" + str(n.val) + "\" ];\n"
            D[n] = str(pos)
            if not(n.leaf()):
                new_res, D = traversal(n.left, D)
                res += new_res + D[n] + "--" + D[n.left] + " [style=dashed];\n" 
                new_res, D = traversal(n.right, D)
                res += new_res + D[n] + "--" + D[n.right] + ';\n'

    return res, D

def dot (T:BDD, filename: str):  # TO DOO
    file = open("graphe/"+filename + ".dot", "w")
    s = "graph { \n"
    res,_ = traversal(T, dict())
    s += res + "}"
    file.write(s)
    file.close()
    
#générer un fichier pdf du graphe de l'arbre
def show(T:BDD, filename: str):
    dot(T,filename)
    os.system("dot -Tpdf "+"graphe/"+filename + ".dot -o " + "graphe/"+filename + ".pdf")

    
if __name__ == "__main__" :
    t=table(38,8)
    #print(cons_arbre(t))
    abr =cons_arbre(t)
    luka(abr)
    #print(abr)
    abr_com = compression(abr)
    abr_bdd = compression_bdd(abr)
    show(abr_com, "test_com")
    show(abr,"test")
    show(abr_bdd, "test_bdd")
    
