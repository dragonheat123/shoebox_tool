
class Node:
    def __init__(self, id=None, roomtype="room", floorArea=None, floorMaterialID=None, isEntrance=False):
        self.id=id
        self.roomtype=roomtype
        self.floorArea=float(floorArea) if floorArea!="" else 0
#        self.lcaDb=lcaDb   #bottleneck given how python handles object refereces
        self.floorMaterialID=floorMaterialID
        self.innerWalls= []
        self.connectedEdges=[] #list of edges connected to this node
        self.traversableEdgeIds=set() #accessible or blocked by infill wall
        self.nonTraversableEdgeIds=set()  #outside or blocked by only structural walls
        self.isEntrance=isEntrance
        self.entranceEdge=None

    def getWalls (self):
        walls = []
        # collect inner walls stored in this node
        if self.innerWalls != None:
            for wall in self.innerWalls:
                walls.append(wall)
                print (wall)
        # collect adjacent walls stored in the edges connected to this node
        for edge in self.connectedEdges:
            walls = walls+edge.adjWalls
        return walls # returns a list of walls related to the room

    def getValency (self):
        return self.getWalls().size()

    def getConnectedEdges (self):
        return self.connectedEdges #TODO: see about IDs

    def getConnectedEdgeIDs (self):
        edgeIDs=[]
        for edge in self.connectedEdges:
            edgeIDs.append(edge.id)
        return edgeIDs

    def getTravesableEdgeIds (self):
        edgeIDs=[]
        for edge in self.connectedEdges:
            edgeIDs.append(edge.id)
        return edgeIDs
    
    #TODO: Change in next version
    def getFloorGWP(self,lcaDb=None):
        if (lcaDb!=None):
            GWP=0
            #TODO: currently all walls in node are considered structural, definition may change in future
            #for w in self.innerWalls:
            #    cost+=w.GWP
            GWP+=self.floorArea*0.2*lcaDb.factor(self.floorMaterialID)  # assuming 200mm slab thickness
            return GWP
        else:
            print("lcaDb must be specified!")