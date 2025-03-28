import random
from graph import G


def calc_fitness(Graph):
    # Initialize fitness score counter
    fit_score = 0
    for strNodeKey in Graph.partitionA:
        # Verify node ID matches the key
        if int(strNodeKey) != Graph.dictV[strNodeKey].intId: 
            print("Error, strNodeKey is not the same as the node ID", strNodeKey, Graph.dictV[strNodeKey].intId)
            exit()
        
        # Count connections that cross from partA to partB
        for connection in Graph.dictV[strNodeKey].lstConnections:
            if connection in Graph.partitionB:
                fit_score = fit_score + 1
    return fit_score

def compute_gain(Graph):
    # Dictionary to store gain values for each node
    dictGainA = {}
    dictGainB = {}
    for strNodeKey in Graph.partitionA:
        gain = 0
        # Calculate gain for each node based on its connections
        for connection in Graph.dictV[strNodeKey].lstConnections:
            if connection in Graph.partitionB:
                gain = gain + 1  # Increase gain for connections to other partition
            else:
                gain = gain - 1  # Decrease gain for connections within same partition
        # Only store gain if node is free to move
        if Graph.dictV[strNodeKey].blnIsFree:
            dictGainA[strNodeKey] = gain

    for strNodeKey in Graph.partitionB:
        gain = 0
        # Calculate gain for each node based on its connections
        for connection in Graph.dictV[strNodeKey].lstConnections:
            if connection in Graph.partitionA:
                gain = gain + 1  # Increase gain for connections to other partition
            else:
                gain = gain - 1  # Decrease gain for connections within same partition
        # Only store gain if node is free to move
        if Graph.dictV[strNodeKey].blnIsFree:
            dictGainB[strNodeKey] = gain

    # Return only the node with maximum gain
    return {max(dictGainA, key=dictGainA.get): dictGainA[max(dictGainA, key=dictGainA.get)]}, {max(dictGainB, key=dictGainB.get): dictGainB[max(dictGainB, key=dictGainB.get)]}


def local_search(Graph):

    # Calculate initial gains for both partitions
    Graph.compute_gain()
    
    # Continue swapping while positive gains exist
    while max(Graph.dictGainA.values()) + max(Graph.dictGainB.values()) > 0:
        Graph.swap_nodes()
        if Graph.FM_passes > 10000: break
    return Graph, Graph.calc_fitness()

def multi_start_local_search(objGraph, intMaxPasses):
    # Track best solution found
    
    Graph = objGraph()
    best_fitness = Graph.fitness

    # Run local search multiple times with different random starts
    i = 0
    while Graph.FM_passes < intMaxPasses:
        Graph = objGraph(Graph.FM_passes)
        Graph, fitness = local_search(Graph)
        # Update best solution if current solution is better
        print("Search: ", i, "Fitness: ", fitness, "Best fitness: ", best_fitness)
        i += 1
        if fitness < best_fitness:
            best_fitness = fitness
            best_Graph = Graph
           
    print(f"Best fitness: {best_fitness}")
    print(f"FM passes: {Graph.FM_passes}")
    return best_Graph, best_fitness

def iterative_local_search(objGraph, mutation_rate, max_passes):
    Graph = objGraph()
    Graph, best_fitness = local_search(Graph)
  
    search_count = 0
    while Graph.FM_passes < max_passes:
        Graph = random_perturbation(Graph, mutation_rate)
        
        Graph.free_nodes()
        Graph, fitness = local_search(Graph)
        print(f"Search Count: {search_count}, Fitness: {fitness}, Best fitness: {best_fitness}, Passes: {Graph.FM_passes}")
        if fitness < best_fitness:

            best_fitness = fitness
            best_Graph = Graph
        search_count += 1
    print(f"FM passes: {Graph.FM_passes}")
    return best_Graph, best_fitness

def random_perturbation(Graph, mutation_rate):
   # Get list of nodes in partition B (where dictPart value is 1)
    lstNodePartB = [node for node, part in Graph.dictPart.items() if part == 1]
    lstNodePartA = [node for node, part in Graph.dictPart.items() if part == 0]
    
    # Randomly swap nodes between partitions based on mutation rate
    for NodeKey in lstNodePartA:
        if random.random() < mutation_rate:
            # Swap partition assignments (bit flip)
            Graph.dictPart[NodeKey] = 1 - Graph.dictPart[NodeKey]  # Flips 0 to 1 or 1 to 0
            randomNode = random.choice(lstNodePartB)
            lstNodePartB.remove(randomNode)
            Graph.dictPart[randomNode] = 1 - Graph.dictPart[randomNode]  # Flips 0 to 1 or 1 to 0
            
    return Graph

def genetic_local_search(objGraph, population_size, max_passes, showOutput = True, blnAllowMutation = False, mutation_rate = 0.2):
    population = []
    for i in range(population_size):
        if showOutput:
            print("Growing population: ", i, "of", population_size)
        Graph = objGraph()
        Graph, _ = local_search(Graph)
        population.append({"Graph": Graph, "fitness": Graph.fitness, "FM_passes": Graph.FM_passes})

    intTotalFM_passes = sum([x["FM_passes"] for x in population])
    while intTotalFM_passes < max_passes:
        best_fitness = min(population, key=lambda x: x["fitness"])["fitness"]

        if showOutput:
            print(f"FM_passes: {intTotalFM_passes}, Best fitness: {best_fitness}, Average Fitness: {sum([x['fitness'] for x in population])/len(population)}")
        parent1, parent2 = random.sample(population, 2)
        child = uniform_crossover(parent1["Graph"], parent2["Graph"], objGraph())
        child.free_nodes()
        child, _ = local_search(child)
        if blnAllowMutation:
            child = random_perturbation(child, mutation_rate)
        intTotalFM_passes = child.FM_passes + intTotalFM_passes
        if child.fitness <= max(population, key=lambda x: x["fitness"])["fitness"]:
            population.remove(max(population, key=lambda x: x["fitness"]))
            population.append({"Graph": child, "fitness": child.fitness, "FM_passes": child.FM_passes})

        if sum([x['fitness'] for x in population])/len(population) == best_fitness:
            stop_counter += 1
        else: stop_counter = 0
        if stop_counter == 100: break

    if showOutput: print(f"Max fitness: ", min(population, key=lambda x: x["fitness"])["fitness"])   
    return min(population, key=lambda x: x["fitness"])["Graph"]

def hamming_distance(graph1, graph2):
    # Calculate number of positions where partitions differ between two graphs
    distance = 0
    for node in graph1.lstKeys:
        if graph1.dictPart[node] != graph2.dictPart[node]:
            distance += 1
    return distance

def uniform_crossover(graph1, graph2, child):
    
    h_distance = hamming_distance(graph1, graph2)

    if h_distance > graph1.intTotV/2:
        graph2.invert_bits()
    newValue = None
    for node in graph1.lstKeys:
        if graph1.dictPart[node] == graph2.dictPart[node]:
            child.dictPart[node] = graph1.dictPart[node]
        elif newValue == None: # If no value is stored
            newValue = random.randint(0, 1)  # Randomly choose partition
            child.dictPart[node] = newValue
        else: # If value is stored. Pick the other value
            child.dictPart[node] = 1 - newValue
            newValue = None

    
    partition_sum = sum(child.dictPart.values())  # Sum all values (0s and 1s)
    expected_sum = len(child.dictPart) // 2  # Should be half of total nodes
    
    if partition_sum != expected_sum:
        print(f"Error: Partitions not balanced. Sum of partition B = {partition_sum}, Expected = {expected_sum}")
        exit()
    return child

