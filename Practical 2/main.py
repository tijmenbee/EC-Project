from graph import G
from algorithms import iterative_local_search, multi_start_local_search, local_search, genetic_local_search
import time
import sys
#iterative_local_search(G, 0.2, 10000)
#multi_start_local_search(G, 10000)


GLS = []
i = 0
best_run = 1000
avg_run = 999
pop_size = 70
iteration = 10
while avg_run < best_run:
    GLS_ILS = []
    for j in range(iteration):
        GLS_ILS.append(genetic_local_search(G, pop_size,10000, False, False, 0.2).fitness)
        sys.stdout.write("Run ... %s%%\r" % ((j/iteration)*100))
        sys.stdout.flush()

    #GLS.append(genetic_local_search(G, 50,10000,False ,False, 0.2).fitness)
    print(f"run: {i}, pop_size: {pop_size}, avg: {sum(GLS_ILS)/iteration}, min: {min(GLS_ILS)}")
    pop_size -= 5
    avg_run = sum(GLS_ILS)/10
    i += 1
print(GLS_ILS)
print(GLS)

