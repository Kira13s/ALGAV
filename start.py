import numpy as np
from typing import *
def decomposition(n:int)->list:
    return [b=="1" for b in bin(n)[:1:-1]]

#decomposition(143)

def completion(lis:list, n:int)->list:
    if n <= len(lis):
        
        return lis[:n]
    else:
        return lis + [False] * int(n-len(lis))

#print(completion([False, True, True, False, False, True], 8))

def table(x:int,n: int)-> list:
    l = decomposition(x)
    return completion(l,n)
if __name__ == "__main__":
    print(table(4,2**10))

    