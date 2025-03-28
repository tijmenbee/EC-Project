from graph import G
from algorithms import iterative_local_search, multi_start_local_search, local_search, genetic_local_search
import time
import sys
#iterative_local_search(G, 0.2, 10000)
#multi_start_local_search(G, 10000)
GLS = genetic_local_search(G, 50, 10000, False)
GLS_ILS = genetic_local_search(G, 8, 10000, False, True, 0.2)
print(GLS.fitness)
print(GLS_ILS.fitness)



