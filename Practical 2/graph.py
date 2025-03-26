import os 
import random
dir_path = os.path.dirname(os.path.realpath(__file__))


class V:
    def __init__(self,id,loc,connections,vertices):
        self.intId = int(id)
        self.strLoc = loc
        self.intConnections = int(connections)
        self.lstConnections = vertices
        self.blnIsFree = True

class E:
    def __init__(self,v1,v2):
        self.V1 = v1
        self.V2 = v2
        self.intId_V1 = self.V1.intId
        self.intId_V2 = self.V2.intId



class G:
    def __init__(self, FM_passes = 0, strPath = "graph500.txt"):
        f = open(dir_path+"\\\\"+strPath, 'r')
        strNodes = f.read().splitlines()
        lstNodes = []
        dictV = {}
        
        for node in strNodes:
            lstInfoNode = node.split()
            objNode = V(lstInfoNode[0],lstInfoNode[1],lstInfoNode[2],lstInfoNode[3:])
            dictV[lstInfoNode[0]] = objNode
            lstNodes.append(objNode)
        """
        lstEdges = []  
        for objNode in lstNodes:
            for edge in objNode.lstConnections:
                if int(edge) > objNode.intId:
                    lstEdges.append(E(objNode,dictV[edge]))
        self.lstEdges = lstEdges
        """
        
        self.dictV = dictV
        self.lstKeys = list(dictV.keys())
        
        self.lstNodes = lstNodes
        self.FM_passes = FM_passes
        self.intTotV = len(lstNodes)
        

        # Randomly shuffle nodes before partitioning
        random.shuffle(self.lstKeys)
        # Partition nodes into two equal partitions
        self.dictPart = {} # 0 for A, 1 for B   
        # Assign first half of nodes to partition A (0)
        for node in self.lstKeys[:int(self.intTotV/2)]:
            self.dictPart[node] = 0
        # Assign second half of nodes to partition B (1)
        for node in self.lstKeys[int(self.intTotV/2):]:
            self.dictPart[node] = 1
        # Sort nodes by ID
        self.lstKeys.sort(key=lambda x: int(x))
    
        self.fitness = 1000
        
    def free_nodes(self):
        for node in self.lstNodes:
            node.blnIsFree = True
        for i in self.lstKeys:
            self.dictV[i].blnIsFree = True
       
    
    def compute_gain(self): 
        # Dictionary to store gain values for each node
        dictGainA = {}
        dictGainB = {}
        for strNodeKey in self.lstKeys:
            if self.dictPart[strNodeKey] == 0:
                dictGainA[strNodeKey] = 0
            else:
                dictGainB[strNodeKey] = 0
        for strNodeKey in self.lstKeys:
            gain = 0
            # Calculate gain for each node based on its connections
            for connection in self.dictV[strNodeKey].lstConnections:
                if self.dictPart[connection] == self.dictPart[strNodeKey] and self.dictV[strNodeKey].blnIsFree:
                    if self.dictPart[strNodeKey] == 0: # Node is in partition A
                        dictGainA[strNodeKey] -= 1  # Decrease gain for connections within same partition
                    else: # Node is in partition B
                        dictGainB[strNodeKey] -= 1  # Decrease gain for connections within same partition
                else:
                    if self.dictPart[strNodeKey] == 0: # Node is in partition A
                        dictGainA[strNodeKey] += 1  # Increase gain for connections to other partition
                    else: # Node is in partition B
                        dictGainB[strNodeKey] += 1  # Increase gain for connections to other partition
        
        # Return only the node with maximum gain
        self.dictGainA = dictGainA
        self.dictGainB = dictGainB  
        return {max(dictGainA, key=dictGainA.get): dictGainA[max(dictGainA, key=dictGainA.get)]}, {max(dictGainB, key=dictGainB.get): dictGainB[max(dictGainB, key=dictGainB.get)]}

    def swap_nodes(self): 
        # Find nodes with maximum gain in each partition
        maxGainNodeA = max(self.dictGainA, key=self.dictGainA.get)
        maxGainNodeB = max(self.dictGainB, key=self.dictGainB.get)
   
        #update the gain of the nodes connected to the swapped nodes
        self.update_gain(maxGainNodeA)
        self.update_gain(maxGainNodeB)
        
       
        
        # Swap partition assignments (bit flip)
        self.dictPart[maxGainNodeA] = 1 - self.dictPart[maxGainNodeA]  # Flips 0 to 1 or 1 to 0
        self.dictPart[maxGainNodeB] = 1 - self.dictPart[maxGainNodeB]

        # Mark swapped nodes as no longer free
        self.dictV[maxGainNodeA].blnIsFree = False
        self.dictV[maxGainNodeB].blnIsFree = False
        

        # Verify partitions remain balanced using dictPart sum
        partition_sum = sum(self.dictPart.values())  # Sum all values (0s and 1s)
        expected_sum = len(self.dictPart) // 2  # Should be half of total nodes
        
        if partition_sum != expected_sum:
            print(f"Error: Partitions not balanced. Sum of partition B = {partition_sum}, Expected = {expected_sum}")
        
        self.FM_passes += 1
        
    def update_gain(self, node):
        """
        Update gains after a node swap:
        - For nodes in the same partition as the moved node: gain decreases by 2 for connections to moved node
        - For nodes in the opposite partition: gain increases by 2 for connections to moved node
        """
        # Determine which partition the node is in
        if not self.dictPart[node]: #If nod in partition A, Partition A = 0
            source_partition = 0
            target_partition = 1
            source_gains = self.dictGainA
            target_gains = self.dictGainB
        else:
            source_partition = 1
            target_partition = 0
            source_gains = self.dictGainB
            target_gains = self.dictGainA

        # Update gains for all connected nodes
        for connection in self.dictV[node].lstConnections:
            if self.dictV[connection].blnIsFree:  # Only update if node is free
                if self.dictPart[connection] == source_partition:
                    # Node in same partition: loses a internal connection (-1) and gains external one (+1)
                    if connection in source_gains:
                        source_gains[connection] += 2
                else:
                    # Node in other partition: gains an internal connection (+1) and loses external one (-1)
                    if connection in target_gains:
                        target_gains[connection] -= 2
        
        # Update the class dictionaries with the modified gains
        if not self.dictPart[node]:
            self.dictGainA = source_gains
            self.dictGainB = target_gains
        else:
            self.dictGainB = source_gains
            self.dictGainA = target_gains

        # Remove the moved node from the gain dictionaries since it's no longer free
        if node in self.dictGainA:
            del self.dictGainA[node]
        if node in self.dictGainB:
            del self.dictGainB[node]
        
    def calc_fitness(self):
        # Initialize fitness score counter
        fit_score = 0
        for strNodeKey in self.lstKeys:

            if self.dictPart[strNodeKey]: continue # if connection is not in part A, part B = 1

            # Count connections that cross from partA to partB
            for connection in self.dictV[strNodeKey].lstConnections:
                if self.dictPart[connection]:
                    fit_score = fit_score + 1
        self.fitness = fit_score
        return fit_score
    def invert_bits(self):

        for node in self.lstKeys:
            self.dictPart[node] = 1 - self.dictPart[node]