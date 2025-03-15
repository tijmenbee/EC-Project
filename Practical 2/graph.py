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

        # Split nodes into two equal partitions
        self.partitionA = self.lstKeys[int(self.intTotV/2):]
        self.partitionB = self.lstKeys[:int(self.intTotV/2)]

        for i in range(len(self.lstKeys)):
            if i in self.partitionA:
                self.lstDictPart.append({i:0})
            else:
                self.lstDictPart.append({i:1})
        

        self.fitness = 0
        
    def free_nodes(self):
        for node in self.lstNodes:
            node.blnIsFree = True
        for i in range(len(self.lstOrdPart)):
            self.dictV[i].blnIsFree = True
       
    
    def compute_gain(self):
        # Dictionary to store gain values for each node
        dictGainA = {}
        dictGainB = {}
        for strNodeKey in self.lstDictPart.keys():
            gain = 0
            # Calculate gain for each node based on its connections
            for connection in self.dictV[strNodeKey].lstConnections:
                if connection in self.partitionB:
                    gain = gain + 1  # Increase gain for connections to other partition
                else:
                    gain = gain - 1  # Decrease gain for connections within same partition
            # Only store gain if node is free to move
            if self.dictV[strNodeKey].blnIsFree:
                dictGainA[strNodeKey] = gain

            for strNodeKey in self.partitionB:
                gain = 0
                # Calculate gain for each node based on its connections
                for connection in self.dictV[strNodeKey].lstConnections:
                    if connection in self.partitionA:
                        gain = gain + 1  # Increase gain for connections to other partition
                    else:
                        gain = gain - 1  # Decrease gain for connections within same partition
                # Only store gain if node is free to move
                if self.dictV[strNodeKey].blnIsFree:
                    dictGainB[strNodeKey] = gain
        
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
        
        # Move node from A to B
        self.partitionA.remove(maxGainNodeA)
        self.partitionB.append(maxGainNodeA)

        # Move node from B to A
        self.partitionB.remove(maxGainNodeB)
        self.partitionA.append(maxGainNodeB)

        # Mark swapped nodes as no longer free
        self.dictV[maxGainNodeA].blnIsFree = False
        self.dictV[maxGainNodeB].blnIsFree = False
        
        # Verify partitions remain balanced
        if len(self.partitionA) != len(self.partitionB):
            print(f"Error, partitionA and partitionB are not the same size: A {len(self.partitionA)} != B {len(self.partitionB)}")
        self.FM_passes += 1
        
    def update_gain(self, node):
        """
        Update gains after a node swap:
        - For nodes in the same partition as the moved node: gain decreases by 2 for connections to moved node
        - For nodes in the opposite partition: gain increases by 2 for connections to moved node
        """
        # Determine which partition the node is in
        if node in self.partitionA:
            source_partition = self.partitionA
            target_partition = self.partitionB
            source_gains = self.dictGainA
            target_gains = self.dictGainB
        else:
            source_partition = self.partitionB
            target_partition = self.partitionA
            source_gains = self.dictGainB
            target_gains = self.dictGainA

        # Update gains for all connected nodes
        for connection in self.dictV[node].lstConnections:
            if self.dictV[connection].blnIsFree:  # Only update if node is free
                if connection in source_partition:
                    # Node in same partition: loses a internal connection (-1) and gains external one (+1)
                    if connection in source_gains:
                        source_gains[connection] += 2
                else:
                    # Node in other partition: gains an internal connection (+1) and loses external one (-1)
                    if connection in target_gains:
                        target_gains[connection] -= 2
        
        # Update the class dictionaries with the modified gains
        if node in self.partitionA:
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
        
    def sort_partition(self):
        self.partitionA.sort()
        self.partitionB.sort()


