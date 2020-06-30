class Cluster:

    def __init__(self):
        self.connectedNodeIds=set()  #start as empty set
        self.connectedEdgeIds=set()
        self.doorIds=[]
        self.properties={"roomCount":0}
        
    def add(self,nodeId):
        self.connectedNodeIds.add(nodeId)
        
    def addEdge(self,edgeId):
        self.connectedEdgeIds.add(edgeId)