import numpy as np
from typing import *
def decomposition(n:int)->list:

    x=[]
    while n != 1:
        x.append(n%2)
        n = n//2
    out = x+[n]
    out = list(map(bool,out)) # converts a list of 0/1 to False/True

    return out

#decomposition(143)

def completion(lis:list, n:int)->list:
    if n <= len(lis):
        return lis[:n]
    else:
        return lis + [False for _ in range(n-len(lis))]

#print(completion([False, True, True, False, False, True], 8))

def table(x:int,n: int)-> list:
    l = decomposition(x)
    return completion(l,n)
if __name__ == "__main__":
    print(table(38,8))
    