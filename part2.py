from start import table
from math import log2

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

def compression_luka(T:BDD): # TO DOO
    if T is None:
        return None
    file = [T]
    D = dict()

    while len(file) > 0:
        node = file.pop(0)
        if node.left and node.right:
            luka_l = luka(node.left)
            if luka_l in D:
                node.left = D[luka_l]
            else:
                D[luka_l] = node.left
                file.append(node.left)
            luka_r = luka(node.right)
            if luka_r in D:
                node.right = D[luka_r]
            else:
                D[luka_r] = node.right
                file.append(node.right)
        else:
            break
    return T


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

def traversal(root, pos):
    res = ""
    if root:
        res += str(pos) + "[ label =\"" + str(root.val) + "\"];\n"
        if root.left:
            res += str(pos) + "--" + str(pos + 1) + "[style=dashed]\n"
        temp = pos
        new_res, pos = traversal(root.left,pos+1)
        res = res + new_res
        if root.right:
            res += str(temp) + "--" + str(pos) + "\n"
        new_res, pos = traversal(root.right,pos)
        res = res + new_res
    return res,pos

def dot (T:BDD, filename: str):  # TO DOO
    file = open(filename + ".dot", "w")
    s = "graph { \n"
    res,_ = traversal(T, 1)
    s += res + "}"
    file.write(s)
    file.close()
    

    
if __name__ == "__main__" :
    t=table(38,8)
    #print(cons_arbre(t))
    abr =cons_arbre(t)
    #compression(abr)
    #print(abr)
    #t=luka(abr)
    #print(abr)
    abr_com = compression_luka(abr)
    #dot(abr,"test")
    
