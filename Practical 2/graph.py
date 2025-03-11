
class V:
    def __init__(self,id,loc,connections,vertices):
        self.intId = int(id)
        self.strLoc = loc
        self.intConnections = int(connections)
        self.lstConnections = vertices

class E:
    def __init__(self,v1,v2):
        self.V1 = v1
        self.V2 = v2
        self.intId_V1 = self.V1.intId
        self.intId_V2 = self.V2.intId



class G:
    def __init__(self, strPath = "graph500.txt"):
        f = open(strPath, 'r')
        strNodes = f.read().splitlines()
        lstNodes = []
        dictV = {}
        lstEdges = []
        for node in strNodes:
            lstInfoNode = node.split()
            objNode = V(lstInfoNode[0],lstInfoNode[1],lstInfoNode[2],lstInfoNode[3:])
            dictV[lstInfoNode[0]] = objNode
            lstNodes.append(objNode)
            
        for objNode in lstNodes:
            for edge in objNode.lstConnections:
                if int(edge) > objNode.intId:
                    lstEdges.append(E(objNode,dictV[edge]))

        
        self.dictV = dictV
        self.lstEdges = lstEdges
        self.lstNodes = lstNodes
        self.intTotV = len(lstNodes)



