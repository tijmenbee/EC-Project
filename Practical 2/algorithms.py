import random
from graph import G

Graph = G()

def local_search(Graph):

    random.shuffle(Graph.lstNodes)

    partitionA = Graph.lstNodes[int(Graph.intTotV/2):]
    partitionB = Graph.lstNodes[:int(Graph.intTotV/2)]