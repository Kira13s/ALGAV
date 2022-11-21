from start import table
from math import log2

class BDD:
    def __init__(self, val ,left=None , right =None) -> None:
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

def compression_luka(T:BDD):
    if T.left.luka == T.right.luka:
        T.left = T.right
    else:
        if T.left:
            compression_luka(T.left)
        if T.right:
            compression_luka(T.right)
    pass


def compression(T:BDD,d:dict={},i=-1):

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
def dot (T:BDD,result = None):
    if result is None:
        result='graph {\n'
    if not T.left and not T.right:
        return ""
    else:
        result += f"{T.val}--{T.left.val}" + dot(T.left,result)
        dot(T.left,result)
    
        result.append(f"{T.val}--{T.right.val}")
        dot(T.right,result)
    
    return result
    

if __name__ == "__main__" :
    t=table(38,8)
    #print(cons_arbre(t))
    abr =cons_arbre(t)
    compression(abr)
    print(abr)
    t=luka(abr)
    #print(abr)
    #print(dot(abr))
    
