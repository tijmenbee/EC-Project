"""
Assume an undirected graph with the set of vertices V and set of
edges E. The number of vertices |V| = n is even. The graph
bipartitioning problem is to find a partitioning of the set of vertices V
into 2 subsets A and B of equal size (|A| = |B|), such that the number of
edges between vertices of A and B is minimal.

"""
from graph import G
from algorithms import iterative_local_search, multi_start_local_search, local_search, genetic_local_search

#iterative_local_search(G, 0.2, 10000)
#multi_start_local_search(G, 10)
genetic_local_search(G, 10000, 4)