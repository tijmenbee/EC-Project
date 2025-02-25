import random
import numpy as np
from random import getrandbits
import more_itertools as mit



def Gen_Pop(N, G): #Create random population
    P = []
    for i in range(N):
        P.append([random.randint(0, 1) for _ in range(G)])
    return P

def Crossover_List(a, b, method = "UX"): # Crossover of an entire list
    
    if len(a) != len(b):
        print("Error! parents cannot crossover")
        exit()
    children_a = []
    children_b = []
    
    for i in range(len(a)):
        children_a.append(Crossover(a[i],b[i],method))
        children_b.append(Crossover(a[i],b[i],method))
    return children_a , children_b

def Crossover(a, b, method = "UX"):  #Crossover of two individuals
    child = []
    if method == "UX":
        if bool(random.getrandbits(1)):
            a, b = b, a
        for i in range(len(a)):
            if bool(random.getrandbits(1)):
                child.append(a[i])
            else: child.append(b[i])
    
    elif method == "2X":
        if bool(random.getrandbits(1)):
            a, b = b, a
        cutoff = random.randint(0, len(a))
        cutoff2 = random.randint(cutoff, len(a))
        child = b[0:cutoff] + a[cutoff:cutoff2] + b[cutoff2:]

    return child

def Fitness_CO(a): # Count Fitness
    return sum(a)

def Fitness_TF(a,d,k,blnTgtLnkd): # Trap function, d is fitness deceptiveness, k is lenght of bit string, blnTgtLnkd is either tightly or loosly linked
    
    if blnTgtLnkd:
        l = [list(c) for c in mit.divide(k, a)]
    else:
        l = mit.distribute(int(len(a)/k), a)
        l = [list(c) for c in l]
    lst = []
    for i in l:
        lst.append(B(i, d))

    return round(sum(lst),2)

def B(a, d): # Trap function
    k = len(a)
    if sum(a) == k:
        return sum(a)
    else: 
        return k - d - ((k-d)/(k-1))*sum(a)
