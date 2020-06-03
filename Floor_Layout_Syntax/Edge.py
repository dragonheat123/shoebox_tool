class Edge:

    def __init__(self, node1, node2, isAccessible=False, adjWalls={}, color=None):

        self.id = 0
        self.nodeU=node1
        self.nodeV=node2
        self.isAccessible=isAccessible
        self.adjWalls=adjWalls
        self.color=color

    def getEdgeId(self):
        return str(self.nodeU.id)+"/"+str(self.nodeV.id)

    def getConnectedNodeById(self,nodeId):
        if nodeId==self.nodeU.id:
            return self.nodeV
        elif nodeId==self.nodeV.id:
            return self.nodeU
        else:
            print("Node not connected: requested node "+str(nodeId))
    
    #TODO: currently wall states are wholly toggled by wallType 
    #-if further definition required, consider unique wall selector or add new wallType

    def getGWPbyType(self,wallType):
        sumGWP=0
        if wallType in self.adjWalls:
            for w in self.adjWalls[wallType]:
                sumGWP+=w.GWP
        return sumGWP

    def getGWP(self):
        sumGWP=0
        for w in self.adjWalls:
            sumGWP+=w.GWP
        return sumGWP