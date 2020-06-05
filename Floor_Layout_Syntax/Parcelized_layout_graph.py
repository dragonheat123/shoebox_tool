

class Parcelized_layout_graph:

    def __init__(self,layout):
        self.units=[]
        #store ids instead of reference in for future storage and retrieval
        self.occupiedNodes= set()  #occupied nodeIds
        self.occupiedEdges=set()
        self.nonUnitNodes = None
        
        self.unusedToOverallRatio=None
        self.satisfactionScore=0
        self.clusterPenalty=0
        
        #no units so all doors initialized as 0 at first
        self.doorSequence = [0]*len(layout.doorEdgeIds) #ORDERED- with reference to doorway index in layout graph
        self.unitSequence = [-1]*len(layout.doorEdgeIds) #aka. door sequence
        #self.unitElevationSequence = [-1,-1,-2,-1,-1,-1,-2,-1,-1,-1,-2,-1,-1] #-nodes facing outside
        #self.elevationSequence = [-1]*len(layout.elevationNodes)
        
        self.wallState={}   #edgeId:wallType:[wallOn/Off]
        
    def addUnit(self,unit,doorEdgesRef,entrancesOccupied,isCompromise=False):
        unitIndex=unit.getUnitTypeIndex()

        for i in range(len(self.doorSequence)):
            if doorEdgesRef[i] in entrancesOccupied:
                self.unitSequence[i]=unitIndex                
                if unit.doorwayId==doorEdgesRef[i]:
                    self.doorSequence[i]=len(entrancesOccupied)
                    
        # for i in range(len(self.elevationSequence)):
        #     if elevationNodesRef[i] in unit.connectedNodeIds:
        #         self.elevationSequence[i]=unitIndex
        #         self.unitElevationSequence[i]=len(self.units)
        self.units.append(unit)
        self.occupiedEdges=self.occupiedEdges.union(unit.connectedEdgeIds)

    def turnOnUnitSurroundingWalls(self,wallType,layout):
        #TODO: turn on all walls around cluster -OR- turn off all walls in cluster (might be easier)
        for edgeId in layout.edges.keys():
            self.wallState[edgeId]={}
            if edgeId in self.occupiedEdges:
                if wallType in layout.edges[edgeId].adjWalls:
                    #self.wallState[edgeId][wallType]=[False]*len(layout.edges[edgeId].adjWalls[wallType])
                    pass #since we're toggling all walls of certain types, we can ignore individual wall presence for now
            else:
                if wallType in layout.edges[edgeId].adjWalls:
                    self.wallState[edgeId][wallType]=True#[True]*len(layout.edges[edgeId].adjWalls[wallType])
    
    def getTotalGwpOfWallType(self,wallType,layout):
        gwp=0
        for edgeId,wallState in self.wallState.items():
            if wallType in wallState:
                gwp+=layout.edges[edgeId].getGwpCost(wallType)
        return gwp
    
    def compareGwpDifference(self,other,wallType,layout):
        res={
                'added':{'qty':0,'cost':0},
                'removed':{'qty':0,'cost':0},
                'saved':{'qty':0,'cost':0}
                }
        for edgeId in layout.edges.keys():
#            if edgeId in self.occupiedEdges and edgeId in other.occupiedEdges:
#                print("Common edge found: "+edgeId)
            if wallType not in self.wallState[edgeId] and wallType in other.wallState[edgeId]:
                #removal gwp cost
#                print("-"+wallType+" at edge "+edgeId+" removed")
                res['removed']['qty']+=1
                res['removed']['cost']+=layout.edges[edgeId].getGwpCost(wallType)          
            elif wallType in self.wallState[edgeId] and wallType not in other.wallState[edgeId]:
                #addition gwp cost
#                print("+"+wallType+" at edge "+edgeId+" added")
                res['added']['qty']+=1
                res['added']['cost']+=layout.edges[edgeId].getGwpCost(wallType)
            elif wallType in self.wallState[edgeId] and wallType in other.wallState[edgeId]:
                #removal gwp cost
#                print("="+wallType+" at edge "+edgeId+" saved")
                res['saved']['qty']+=1
                res['saved']['cost']+=layout.edges[edgeId].getGwpCost(wallType)
        return res
    
    def getUnitIndexFromNodeId(self,nodeId):
        for i in range(len(self.units)):
            if self.units[i].isNodeInUnit(nodeId):
                return i
        return -1 #no assigned unit
    
    def printAllUnits(self):
        print("Layout consists of:")
        for u in self.units:
            print("-UnitType"+str(u.getUnitTypeIndex())+", nodes: "+str(u.connectedNodeIds))
