import random
import numpy as np
from random import getrandbits
import more_itertools as mit



def Gen_Pop(N, G): #Create random population
    P = []
    for i in range(N):
        P.append([random.randint(0, 1) for _ in range(G)])
    return P

def Crossover_List(a, b, method): # Crossover of an entire list
    
    if len(a) != len(b):
        print("Error! parents cannot crossover")
        exit()
    children_a = []
    children_b = []
    
    for i in range(len(a)):
        child1, child2 = Crossover(a[i],b[i],method)
        children_a.append(child1)
        children_b.append(child2)
    return children_a , children_b

def Crossover(a, b, method):  #Crossover of two individuals
    child1 = []
    child2 = []
    if method == "UX":
        if bool(random.getrandbits(1)):
            a, b = b, a
        for i in range(len(a)):
            if bool(random.getrandbits(1)):
                child1.append(a[i])
                child2.append(b[i])
            else: 
                child1.append(b[i])
                child2.append(a[i])
    
    elif method == "2X":
        if bool(random.getrandbits(1)):
            a, b = b, a
        cutoff = random.randint(0, len(a))
        cutoff2 = random.randint(cutoff, len(a))
        child1 = b[0:cutoff] + a[cutoff:cutoff2] + b[cutoff2:]
        child2 = a[0:cutoff] + b[cutoff:cutoff2] + a[cutoff2:]

    return child1, child2

def Fitness_CO(a): # Count Fitness
    return sum(a)

def Fitness_TF(a,d,k,blnTgtLnkd): # Trap function, d is fitness deceptiveness, k is lenght of bit string, blnTgtLnkd is either tightly or loosly linked
    
    if blnTgtLnkd:
        l = [list(c) for c in mit.divide(int(len(a)/k), a)]
       
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
