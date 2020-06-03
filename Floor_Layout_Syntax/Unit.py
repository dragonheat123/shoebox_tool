
class Unit:

    def __init__(self, startNode=None, doorwayId=None, constraint=None, connectedNodeIds=set(), connectedEdgeIds=set()):
        self.connectedNodeIds=connectedNodeIds  #start as empty set
        self.connectedEdgeIds=connectedEdgeIds
        self.startNode=startNode
        self.doorwayId=doorwayId
        self.occupiedDoorwayIds=set()
        self.nonUnitEdges=set()
        self.constraint=constraint
        
    def isNodeInUnit(self,nodeId):
        if nodeId in self.connectedNodeIds:
            return True
        else:
            return False
    
    def getUnitTypeIndex(self):
        return self.constraint['unitTypeIndex']
    
    def getUnitColorType(self):
        return self.constraint['color']