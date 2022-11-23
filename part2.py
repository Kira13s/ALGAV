from start import table
from math import log2
import os

class BDD:
    counter = 0
    def __init__(self, val ,left=None , right =None) -> None:
        BDD.counter += 1
        self.val = val
        self.left = left
        self.right = right
        self.luka =None
    def __repr__(self) -> str:
        return f"BDD [ val:{self.val}, left: {self.left},right: {self.right}, luka :{self.luka}]"


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

    if not T.left and not T.right :
        T.luka = str(T.val)
        return T.luka
    else:
        T.luka=f"{T.val}({luka(T.left)})({luka(T.right)})"
        return T.luka

def suffix(n, D):
    if n.left and n.right:
        if n.left.luka not in D:
            D = suffix(n.left, D)
        if n.right.luka not in D:
            D = suffix(n.right, D)
        if n.luka not in D:
            D[n.luka] = BDD(n.val, D[n.left.luka], D[n.right.luka])
    return D
        

def compression_luka(T:BDD): # TO DOO
    if T is None:
        return None
    D = {"True": BDD(True), "False": BDD(False)}
    luka_racine = luka(T)
    D = suffix(T, D)
    return D[luka_racine]


def compression(T:BDD,d:dict={},i=-1):  # TO DOO

    if not T.left and not T.right:
        if T.val not in d:
            d[T.val] = i+1
            return T.val
        else:
            T.val = d[T.val]
            return d[T.val]
    else:
        
        ss=(compression(T.left,d),compression(T.right,d),T.val)
        if ss not in d:
            d[ss]=i+1
            return d[ss]
        else:
            T.val =d[ss]
    print(d)
    pass

def traversal(n, D):
    res = ""
    if n:
        if n not in D:
            pos = len(D)
            res += str(pos) + " [ label = \"" + str(n.val) + "\" ];\n"
            D[n] = str(pos)
            if n.left and n.right:
                new_res, D = traversal(n.left, D)
                res += new_res + D[n] + "--" + D[n.left] + " [style=dashed];\n" 
                new_res, D = traversal(n.right, D)
                res += new_res + D[n] + "--" + D[n.right] + ';\n'

    return res, D

def dot (T:BDD, filename: str):  # TO DOO
    file = open(filename + ".dot", "w")
    s = "graph { \n"
    res,_ = traversal(T, dict())
    s += res + "}"
    file.write(s)
    file.close()
    
#générer un fichier pdf du graphe de l'arbre
def show(T:BDD, filename: str):
    dot(T,filename)
    os.system("dot -Tpdf "+filename + ".dot -o " + filename + ".pdf")

    
if __name__ == "__main__" :
    t=table(38,8)
    #print(cons_arbre(t))
    abr =cons_arbre(t)
    #compression(abr)
    #print(abr)
    #t=luka(abr)
    #print(abr)
    abr_com = compression_luka(abr)
    show(abr_com, "test_com")
    show(abr,"test")
    
