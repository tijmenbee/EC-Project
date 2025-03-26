from graph import G
from algorithms import iterative_local_search, multi_start_local_search, local_search, genetic_local_search

iterative_local_search(G, 0.2, 10000)
#multi_start_local_search(G, 10000)
genetic_local_search(G, 25 ,10000)