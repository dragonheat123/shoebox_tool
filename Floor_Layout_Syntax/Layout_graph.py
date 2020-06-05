import copy
import csv
import json
import random

import jsonpickle
import matplotlib.colors as colors
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import networkx as nx
from more_itertools import distinct_permutations
from sortedcontainers import SortedSet

import Floor_Layout_Syntax.Cluster as Cluster
import Floor_Layout_Syntax.Constants as Constants
import Floor_Layout_Syntax.Constraint as con
import Floor_Layout_Syntax.Edge as edge
import Floor_Layout_Syntax.Node as node
import Floor_Layout_Syntax.Parcelized_layout_graph as p_layout
import Floor_Layout_Syntax.Unit as p_unit
import Floor_Layout_Syntax.Wall as wall
from LCA import LCADB


class Layout_graph:

    def __init__(self):        
        # dictionaries of id:objects
        self.nodes = {}
        self.edges = {}
        
        self.serviceNodeIds = set()
        self.doorEdgeIds = []   #ORDER MATTERS- used as door position reference by parcelized results
#        self.elevationNodes = ['18','19',-2,'20','21','22',-2,'23','24','25',-2,'26','27'] #rooms facing the outside (-2 are recesses)
        # self.elevationNodes = ['18','19','20','21','22','23','24','25','26','27'] 
        # self.G = nx.Graph()  # initialising empty networkx graph
        # self.drawPos={}
        # self.drawEdges = []
        # self.img=None
        
        self.roomCount={
        'normal':0,
        'toilet':0,
        'storage':0
        }
        
        # self.colorPool=[[1, 0.627, 0.235], [0.031, 0.612, 0.533], [0.643, 0.137, 0.506], [1, 0.773, 0.235], [0.922, 0.329, 0.467], [0.388, 0.647, 0.329]]
        self.unitCombinations={}
        self.combinationResult={}
        self.structuralGwp=0.0

#--------------------------------------------------------------------------------------------------------------------------------------------------------
#       UTILITY AND IMPORT FUNCTIONS
    def addNode(self, newNodeID, roomtype=None, floorArea=None, floorMaterialID='CP032'):
        if isinstance(newNodeID, str) != True: newNodeID=str(newNodeID)
        self.nodes[newNodeID]=node.Node (id=newNodeID,roomtype=roomtype, floorArea=floorArea, floorMaterialID=floorMaterialID)
        if self.nodes[newNodeID].roomtype=="service":
            self.serviceNodeIds.add(newNodeID)
        elif (self.nodes[newNodeID].roomtype!="outside"):
            self.roomCount[self.nodes[newNodeID].roomtype]+=1


    def addEdgeById (self, edgeId, isAccessible, adjWalls): #node is specified by their name
        nodes = edgeId.split("/")
        nodeId1=nodes[0]
        nodeId2=nodes[1]
        
        # id edge nodes do not yet exist, add to self.nodes
        if nodeId1 not in self.nodes.keys(): 
            self.addNode (newNodeID=nodeId1)
            print("Node "+str(nodeId1)+" not found! Created new node")
        if nodeId2 not in self.nodes.keys(): 
            self.addNode (newNodeID=nodeId2)
            print("Node "+str(nodeId2)+" not found! Created new node")
            
        
        isDoorway = False
        if nodeId1 in self.serviceNodeIds and int(nodeId2) != 0:
            isDoorway = True
            self.nodes[nodeId2].entranceEdge=edgeId #TODO: change to list or set in future if multiple entrances in node
            self.nodes[nodeId2].isEntrance=True
            self.doorEdgeIds.append(edgeId)
        if nodeId2 in self.serviceNodeIds and int(nodeId1) != 0:
            if isDoorway: 
                self.nodes[nodeId2].entranceEdge = None 
                self.nodes[nodeId2].isEntrance = False
                isDoorway = False
                self.doorEdgeIds.pop()
            else:
                isDoorway = True
                self.nodes[nodeId1].entranceEdge=edgeId #TODO: change to list or set in future if multiple entrances in node
                self.nodes[nodeId1].isEntrance=True
                self.doorEdgeIds.append(edgeId)

        e = edge.Edge(self.nodes[nodeId1], self.nodes[nodeId2])
        e.isAccessible=isAccessible
        e.isDoorway=isDoorway
        e.adjWalls=adjWalls
        e.id=edgeId
        
        #TODO: make this definition more robust
        #-traversable means that the nodes (rooms) can be connected to form a unit
        isTraversable=False
        if isAccessible and not isDoorway:
            isTraversable=True
        else:
            traversableWallTypes={"infill"} #TODO: convert to global constant for removable wall types
            for t in traversableWallTypes:
                if t in adjWalls:
                    isTraversable=True
                    break
            
        self.edges[edgeId]=e
        if isTraversable:
            self.nodes[nodeId1].traversableEdgeIds.add(edgeId)
            self.nodes[nodeId2].traversableEdgeIds.add(edgeId)
        else:
            self.nodes[nodeId1].nonTraversableEdgeIds.add(edgeId)
            self.nodes[nodeId2].nonTraversableEdgeIds.add(edgeId)            
        #reference to edges
        self.nodes[nodeId1].connectedEdges.append(e) #update attribute list of edges connected to node1
        self.nodes[nodeId2].connectedEdges.append(e)  #update attribute list of edges connected to node2
        #-------


    def removeNode(self, nodeId):
        del self.nodes[nodeId]

    def removeEdgeByNodes(self, nodeId1, nodeId2):
        #todo: error catching
        if nodeId1 < nodeId2:
            del self.edges[nodeId1+'/'+nodeId2]
        else:
            del self.edges[nodeId2+'/'+nodeId1]

    def removeEdgeByID (self, edgeId):
        del self.edges[edgeId]
        nodes = edgeId.split("/")

    def getEdgeByNodes(self, nodeId1, nodeId2):
        if nodeId1 < nodeId2:
            key=nodeId1+'/'+nodeId2
        else:
            key=nodeId2+'/'+nodeId1
        if key in self.edges:
            return self.edges[key]
        else:
            return None

    def importJSON(self, nodes_JSONfilepath , edges_JSONfilepath, lcaDbPath):
        with open(nodes_JSONfilepath) as nodes_json_file:
            nodesData = json.load(nodes_json_file)

        for n in nodesData:
            #TODO: fix material Id (also in inWall)
            self.addNode(newNodeID=str(n['id']), roomtype=n['roomtype'], floorArea=n['floorArea'], floorMaterialID='CP032')
            for inWall in n['innerWalls']:
                self.nodes[n['id']].innerWalls.append(wall.Wall(vertices=inWall['vertices'], materialID='CP032', thickness=inWall['thickness'],
                          wallType=inWall['wallType'], wallArea=inWall['wallArea'], wallLength=inWall['wallLength']))
        with open(edges_JSONfilepath) as edges_json_file:
            edgesData = json.load(edges_json_file)

        tempDb= LCADB.LCADB(lcaDbPath)
        for e in edgesData:
            adjacentWalls = {}
            #TODO: fix material Id
            for inWall in e['adjWalls']:                    
                if inWall['wallType'] not in adjacentWalls:
                    adjacentWalls[inWall['wallType']]=[wall.Wall(vertices=inWall['vertices'], materialID='CP032', thickness=inWall['thickness'],
                           wallType=inWall['wallType'], wallArea=inWall['wallArea'], wallLength=inWall['wallLength'],lcaDb=tempDb)]
                else:
                    adjacentWalls[inWall['wallType']].append(wall.Wall(vertices=inWall['vertices'], materialID='CP032', thickness=inWall['thickness'],
                           wallType=inWall['wallType'], wallArea=inWall['wallArea'], wallLength=inWall['wallLength'],lcaDb=tempDb))
            # if e['isDoorway']:
            #     self.doorEdgeIds.append(e['edgeId'])
            self.addEdgeById(edgeId=e['edgeId'], isAccessible=e['isAccessible'], adjWalls=adjacentWalls)
        #TODO: following function may be dynamic so consider better lcaDb system and structure hierarchy
        print(self.doorEdgeIds)
        self.getStructuralGwp(tempDb)

    def importResultJson(self,importFilePath):
        f= open(importFilePath,"r")
        obj=jsonpickle.decode(f.read()) 
        f.close()
        return obj
    
    def exportResultJson(self,exportPath,obj):
        f= open(exportPath,"w+")
        f.write(jsonpickle.encode(obj))
        f.close()
        return
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#   CALCULATE EMPTY NODE CLUSTERS    
    '''
    #recusive clustering algorithm to cluster unused spaces
    Clusters with a door edge are not penalized whereas an isolated one is penalized heavily
    
    #Algorithm intuition:
    -from a list of unused nodes, create cluster from first index node [x]
    -unused nodes are checked with one another from left to right in pairs [x] and [x+1]
    -if connected, [x+1] is added to [x] cluster and checked with other unchecked nodes to try add them to the same cluster
    
    leftToCheck: unchecked nodes
    nextToCheck: clustered nodes to be checked with unchecked nodes to add them to the same cluster
    '''
    def recurseCluster(self,nextToCheck,leftToCheck,clusterResults,clusterDoorResults,clusterIndex=-1):
#        print('Left to check:')
#        print(leftToCheck)
#        print('Next to check:')
#        print(nextToCheck)
#        print("Clusters:")
#        print(clusterResults)
#        p=input()
        
        if len(nextToCheck)>0:
            nextSetToCheck=set()
            for x in range(0,len(leftToCheck)):
                edge=self.getEdgeByNodes(nextToCheck[0],leftToCheck[x])
                if edge!=None:
                    clusterResults[clusterIndex].add(leftToCheck[x])
                    clusterResults[clusterIndex].addEdge(edge.id)
                    clusterResults[clusterIndex].properties["roomCount"]+=1
                    if self.nodes[leftToCheck[x]].roomtype in clusterResults[clusterIndex].properties:
                        clusterResults[clusterIndex].properties[self.nodes[leftToCheck[x]].roomtype]+=1
                    else:
                        clusterResults[clusterIndex].properties[self.nodes[leftToCheck[x]].roomtype]=1
                    if self.nodes[leftToCheck[x]].entranceEdge!=None:
                        clusterResults[clusterIndex].doorIds.append(self.nodes[leftToCheck[x]].entranceEdge)
                        clusterDoorResults[clusterIndex]+=1
                    nextSetToCheck.add(leftToCheck[x])
                    
            nextToCheck.discard(nextToCheck[0])
            nextToCheck.update(nextSetToCheck)
            leftToCheck-=nextToCheck
            self.recurseCluster(nextToCheck,leftToCheck,clusterResults,clusterDoorResults,clusterIndex)
                    
        elif len(leftToCheck)>0:
#            clusterResults.append(set())
            clusterResults.append(Cluster.Cluster())
            clusterDoorResults.append(0)
            clusterIndex+=1
            clusterResults[clusterIndex].add(leftToCheck[0])
            clusterResults[clusterIndex].properties["roomCount"]+=1
            clusterResults[clusterIndex].properties[self.nodes[leftToCheck[0]].roomtype]=1
            
            if self.nodes[leftToCheck[0]].entranceEdge!=None:
                clusterDoorResults[clusterIndex]+=1
                clusterResults[clusterIndex].doorIds.append(self.nodes[leftToCheck[0]].entranceEdge)
            
            nextToCheck=SortedSet()
            for x in range(1,len(leftToCheck)):
                edge=self.getEdgeByNodes(leftToCheck[0],leftToCheck[x])
                if edge!=None:
                    clusterResults[clusterIndex].add(leftToCheck[x])
                    clusterResults[clusterIndex].addEdge(edge.id)
                    clusterResults[clusterIndex].properties["roomCount"]+=1
                    if self.nodes[leftToCheck[x]].roomtype in clusterResults[clusterIndex].properties:
                        clusterResults[clusterIndex].properties[self.nodes[leftToCheck[x]].roomtype]+=1
                    else:
                        clusterResults[clusterIndex].properties[self.nodes[leftToCheck[x]].roomtype]=1
                    
                    if self.nodes[leftToCheck[x]].entranceEdge!=None:
                        clusterResults[clusterIndex].doorIds.append(self.nodes[leftToCheck[x]].entranceEdge)
                        clusterDoorResults[clusterIndex]+=1
                    nextToCheck.add(leftToCheck[x])
                    
            leftToCheck.discard(leftToCheck[0])
            leftToCheck-=nextToCheck
            self.recurseCluster(nextToCheck,leftToCheck,clusterResults,clusterDoorResults,clusterIndex)
        else:
            return
    
    def fillEmptyNodes(self,floorplan):
        leftToCheck=SortedSet(set(self.nodes.keys())-floorplan.occupiedNodes-self.serviceNodeIds)
        leftToCheck.discard('0')    #ignore outside node
        clusters=[]
        clusterDoors=[]
        self.recurseCluster([],leftToCheck,clusters,clusterDoors)
        for cluster in clusters:
            if len(cluster.doorIds)>0:
                if 'normal' in cluster.properties and 'toilet' in cluster.properties and 'storage' in cluster.properties:
                    unit=p_unit.Unit(doorwayId=cluster.doorIds[0],constraint=con.Constraint(roomType=cluster.properties['normal']-1,prefWeight=1,prefDoors=cluster.doorIds,roomConstraints=cluster.properties),
                                     connectedNodeIds=cluster.connectedNodeIds,connectedEdgeIds=cluster.connectedEdgeIds)
                    floorplan.addUnit(unit,self.doorEdgeIds,cluster.doorIds,True)
                    floorplan.occupiedNodes.update(cluster.connectedNodeIds)
                    self.testFloorplanScore(floorplan)
        return floorplan

    #The lower the score the 'better' utility of space
    #[0]- number of clusters, [1]- number of clusters isolated from doors
    def checkClusterScore(self, floorplan):
        leftToCheck=SortedSet(set(self.nodes.keys())-floorplan.occupiedNodes-self.serviceNodeIds)
        leftToCheck.discard('0')    #ignore outside node
        clusters=[]
        clusterDoors=[]
        self.recurseCluster([],leftToCheck,clusters,clusterDoors)
        
        ##penalize based on non-accessibility to doors
        penalty=0
        for doors in clusterDoors:
            if doors==0:
                penalty+=1
        floorplan.clusterPenalty=penalty
        return (len(clusters),penalty)
    
    #generalized, faster approach
    def testFloorplanScore(self, floorplan):
        floorplan.unusedToOverallRatio=float(len(self.nodes)-len(floorplan.occupiedNodes-self.serviceNodeIds))/float(len(self.nodes))
        return floorplan.unusedToOverallRatio
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------
#       TRAVERSAL ALGORITHM
    def traverseDelegateUnitNodes(self,floorplan,occupiedDoorIds,edgeToCurrentNodeId,currentNode,traversedNodeIds,traversedEdgeIds,traversablePaths,traversedPaths,criteria,possibleFloorplans,entrancesOccupied=0):
        #update traversed path list and check if the this is a duplicate combination
        traversedNodeIds.add(currentNode.id)
        traversedEdgeIds.add(edgeToCurrentNodeId)
        hashSet=frozenset(traversedNodeIds)
        
        if hashSet in traversedPaths:
            return #skip this iteration as it is already considered
        
        isUnit=True
        #update the criteria to fulfil of this path combination result
        if currentNode.roomtype in criteria:
            if criteria[currentNode.roomtype]>0:
                criteria['roomCount']-=1
                criteria[currentNode.roomtype]-=1
                if criteria['roomCount']>0:
                    isUnit=False
            else:
                return
        else:
            return
        traversedPaths[hashSet]=criteria
        
        #draw graph
#        self.drawTraversedPaths(layout=floorplan,traversedNodesIds=sorted(traversedNodeIds), traversedEdgesIds=sorted(traversedEdgeIds))
#        print('To fulfil:')
#        print(criteria)
#        p=input()
        
        #index door edge if any
        if currentNode.entranceEdge != None: 
            entrancesOccupied+=1
            c_occupiedDoorIds=copy.deepcopy(occupiedDoorIds)
            c_occupiedDoorIds.append(currentNode.entranceEdge)
        else:
            c_occupiedDoorIds=occupiedDoorIds
        
        #check if roomCount is exceeded, then check its validity as a unit if so
        if isUnit:
            #--Proper unit achieved
            #-connect all edges in the unit:
            for n in traversedNodeIds:
                for e in self.nodes[n].connectedEdges:
#                    print('is '+e.getConnectedNodeById(n)+' in '+traversedNodeIds)
                    if e.getConnectedNodeById(n).id in traversedNodeIds:
                        traversedEdgeIds.add(e.getEdgeId())
            unit=p_unit.Unit(doorwayId=c_occupiedDoorIds[0],constraint=criteria,connectedNodeIds=traversedNodeIds,connectedEdgeIds=traversedEdgeIds)
            newFloorplan=copy.deepcopy(floorplan)
            newFloorplan.addUnit(unit,self.doorEdgeIds,c_occupiedDoorIds)
            newFloorplan.occupiedNodes.update(traversedNodeIds)

#            print('=====VALID UNIT====')
#            self.drawTraversedPaths(newFloorplan)
            
            self.testFloorplanScore(newFloorplan)
            possibleFloorplans.add(newFloorplan)
            return
        else:
            #update travesable paths by adding them from the current node
            traversablePaths[currentNode.id]=set(currentNode.traversableEdgeIds)
            traversablePaths[currentNode.id].discard(edgeToCurrentNodeId)
            #print(traversablePaths)
            for n, e in traversablePaths.items():   #foreach traversable path n:edgeset
                for traversableEdgeId in e:
                    nextNode=self.edges[traversableEdgeId].getConnectedNodeById(n)
                    #print(nextNode.id)
                    if nextNode.id in traversedNodeIds:
                        continue
                    elif nextNode.id in floorplan.occupiedNodes:
                        continue
                    elif nextNode.roomtype=="service":
                        continue
                    else:
                        #create path copies for other combination recursions
                        c_criteria=copy.deepcopy(criteria)
                        c_traversedNodeIds=traversedNodeIds.copy()
                        c_traversedEdgeIds=traversedEdgeIds.copy()
                        c_traversablePaths=traversablePaths.copy()
                        self.traverseDelegateUnitNodes(floorplan,c_occupiedDoorIds,traversableEdgeId,nextNode,c_traversedNodeIds,c_traversedEdgeIds,c_traversablePaths,traversedPaths,c_criteria,possibleFloorplans,entrancesOccupied)
#       TRAVERSAL ALGORITHM END
#--------------------------------------------------------------------------------------------------------------------------------------------------------    
    
    #this method generates a list of all possible layout results from a demand list irregardless of position
    def generatePossibleLayout(self,demandList):
        if len(demandList)<1:
            print("error: no demand to generate layout from")
            return
        
        allPossibleFloorplans=set()   #container for results after algorithm
        demandListPermutations=distinct_permutations(demandList)
        #minClusterScore=(99,99)
        
        for d in demandListPermutations:
            floorplan=p_layout.Parcelized_layout_graph(self) #fresh empty new floorplan
            possibleFloorplans=set()
            demandIndex=-1        
            #foreach doorway location
            for door in self.doorEdgeIds:
                demandIndex+=1
                if demandIndex>=len(d):
                    break
                
                startNode=self.edges[door].nodeV
                #if starting node belongs to a unit already-- skip
                traversedNodeIds=set()
                traversedEdgeIds=set()
                occupiedDoorIds=[]
                currentNode=startNode
                traversablePaths={}
                criteria=Constants.UNIT_TYPES[d[demandIndex]].copy()
                traversedPaths={} #consists of a frozen key set which shows node combinations and its score as value
                
                if demandIndex==0:
#                    print('-trying demand: '+str(d))
                    self.traverseDelegateUnitNodes(floorplan,occupiedDoorIds,door,currentNode,traversedNodeIds,traversedEdgeIds,traversablePaths,traversedPaths,criteria,possibleFloorplans)
                else:
                    newPossibleFloorplans=set()
                    for fp in possibleFloorplans:
                        if startNode.id in fp.occupiedNodes: 
                            continue                    
                        self.traverseDelegateUnitNodes(fp,occupiedDoorIds,door,currentNode,traversedNodeIds,traversedEdgeIds,traversablePaths,traversedPaths,criteria,newPossibleFloorplans)
                    if len(newPossibleFloorplans)>0:
                        possibleFloorplans=newPossibleFloorplans
                    else:
#                        print("--Door not free. Trying next..")
                        demandIndex-=1
            if demandIndex==len(d):
#                print("Result(s) found!")
                allPossibleFloorplans.update(possibleFloorplans)
#                for fp in possibleFloorplans:
#                    self.drawTraversedPaths(fp)
#                    fp.printAllUnits()
                    #todo: filter results?
#            else:
#                print("No Result found!")
        return list(allPossibleFloorplans)
    
    #returns true if combination is possible; otherwise false
    def parcelizeForCombinationIndex(self,combinationIndex):
        isParcelizable = False 
        if combinationIndex not in self.combinationResult:
            unitCombination = self.unitCombinations[combinationIndex]['countVector'].copy()
            demandList = []
            for unitIndex in range(len(unitCombination)):
                if unitCombination[unitIndex]>0:
                    for i in range(unitCombination[unitIndex]):
                        demandList.append(unitIndex)
            #print("Result not found. Attempting to fulfil layout: "+str(demandList))
            result=self.generatePossibleLayout(demandList)
            if (len(result)>0):
                print("+Result(s) found for combinationIndex: "+str(combinationIndex)+", "+str(demandList))
                self.combinationResult[combinationIndex] = result
                isParcelizable = True
            else:
                print("-No result found for combinationIndex: "+str(combinationIndex)+", "+str(demandList))
                isParcelizable =  False
        else:
            print("Result already exists!")
            isParcelizable = True
        return isParcelizable
    
    def generateParcelationDb(self,emptySpaceThreshold,saveParcelationDbPath=None):
        unitCombiResults = {}
        for i in range(0,len(Constants.UNIT_TYPES)):
            checkSolutionSpace(self.roomCount.copy(),Constants.UNIT_TYPES,emptySpaceThreshold,i,[],unitCombiResults)
        
        i=0
        for unitCombination, emptySpace in unitCombiResults.items():
            countVector = []
            for unitType in range(len(Constants.UNIT_TYPES)):
                countVector.append(unitCombination.count(str(unitType)))
            self.unitCombinations[i]={
                    'countVector':countVector,
                    'emptySpace':emptySpace
                    }
            i+=1
            
        entriesToRemove=set()
        #check validity of combinations and generate parcelations from them
        for combinationIndex in self.unitCombinations.keys():
            if not self.parcelizeForCombinationIndex(combinationIndex):
                entriesToRemove.add(combinationIndex)
        
        #remove invalid combinations
        for key in entriesToRemove:
            self.unitCombinations.pop(key)
#        f= open(parcelationDbPath,"w+")
#        f.write(jsonpickle.encode(self.combinationResult))
#        f.close()
        if len(self.unitCombinations)<1:
            raise ValueError('No possible layout found! Try increasing empty space threshold or redefining units.')
                
    def getRandomParcelation(self,combinationIndex):
        if combinationIndex not in self.combinationResult:
            print("Error: combination does not exist!")
        else:
            fp=self.combinationResult[combinationIndex][random.randrange(0,len(self.combinationResult[combinationIndex]))]
#            self.drawTraversedPaths(fp)
            fp.printAllUnits()
            return fp
    
    #Layout result with all walls turned on
    def getDefaultLayout(self):
        return p_layout.Parcelized_layout_graph(self)
    
    def loadParcelationDb(self,parcelationDbPath):
        try:
            f= open(parcelationDbPath,"r")
            print("Parcelation database found- loading results")
            self.combinationResult=jsonpickle.decode(f.read()) 
            f.close()
            return True
        except IOError:
            return False
        
#--------------------------------------------------------------------------------------------------------------------------------------------------------

#     def loadDrawVectors(self,posPath,vecLengthsPath,imageRootPath):
#         self.drawPos = {}
#         self.drawEdges = []
#         #==========================================================================================================
#         #### INSTRUCTIONS FOR LOADING BASE FLOOR-PLAN .PNG IMAGE
#         #### image needs to have following dims: 3852pixels(widtth) * 1186 pixels(height)
#         #### scale at 1:150 on sheet size A3 when printing to PDF from Rhino then export to PNG from PDF in preview
#         #### sometimes the image might need rotating by 180 deg
#         # ==========================================================================================================
# #        fig, ax = plt.subplots(figsize=(2 * 12.83, 2 * 3.94))
#         self.img = mpimg.imread(imageRootPath)
#         height, width = self.img.shape[:2]
#         origin = [height/2, width/2]
#         with open(posPath) as csvpos :
#             csv_reader = csv.reader(csvpos, delimiter=',')
#             positions=[]
#             for row in csv_reader:
#                 coord = []
#                 for s in row:
#                     coord.append(s.translate({ord('{'):None, ord('}'):None}))
#                 positions.append([float(x) for x in coord])
#         for i, node in enumerate (positions):
#             self.drawPos[str(i+1)] = [origin[1]+node[0]/12.8, origin[0]+node[1]/12.8]

#         # adds outside node
#         self.drawPos['0'] = [0, self.drawPos['1'][1]] # TODO: replace this hardcoded position for Node 0
#         for e in self.G.edges:
#             if ('0' in e) == False:
#                 self.drawEdges.append(e)

#     def drawTraversedPaths(self, layout=None, traversedEdgesIds=None, traversedNodesIds=None):
#         fig, ax = plt.subplots(figsize=(2 * 12.83, 2 * 3.94))
        
#         plt.imshow(self.img, aspect='equal', origin='lower')
#         plt.subplots_adjust(left = 0.03)
#         fig.tight_layout(pad = 0)
        
#         labels = {}
#         for i in range (0, len(self.G.nodes)):
#             if i==0: labels[str(i)]=''
#             else:labels[str(i)]=str(i)

#         nodes = nx.draw_networkx_nodes(self.G, nodelist=[str(x) for x in range(1,self.G.number_of_nodes())] ,pos=self.drawPos,  node_color='grey', alpha=0.8, edge_color='b')
#         edges = nx.draw_networkx_edges(self.G, self.drawPos, edgelist=self.drawEdges, width=1, alpha=0.5)

#         nx.draw_networkx_labels(self.G, pos=self.drawPos, labels=labels, font_size=8, font_weight='bold')
        

#         if traversedEdgesIds!=None:
#             travEdgeIds_G = []
#             for i, travEdge in enumerate(traversedEdgesIds):
#                 nodeId1 = travEdge.split("/")[0]
#                 nodeId2 = travEdge.split("/")[1]
#                 e_G = [str(nodeId1), str(nodeId2)]
#                 travEdgeIds_G.append(e_G)
#                 a = abs(0.8-(1/(i+1)))
#                 nx.draw_networkx_edges(self.G, self.drawPos, edgelist=[e_G ], width=3, edge_color='r', alpha=1)
#                 #plt.pause(0.5)

#             #nx.draw_networkx_edges(self.G, pos, edgelist=travEdgeIds_G, width=2, edge_color='r')
#         if traversedNodesIds != None:
#             #make sure supplied node indices are string format
#             travNodeIds_G=[]
#             for tNode in traversedNodesIds:
#                 travNodeIds_G.append(str(tNode))

#             nx.draw_networkx_nodes(self.G, pos=self.drawPos, nodelist=travNodeIds_G, font_size=8, node_color='r', alpha=1, edge_color='black',node_size=670)

#         if layout!=None:
# #            poolLength=len(self.colorPool)
#             for unit in layout.units:
#                 n=unit.connectedNodeIds
#                 e=unit.connectedEdgeIds
#                 edgesToDraw=[]
#                 for pair in e:
#                     edgesToDraw.append(pair.split('/',1))
#                 c=colors.to_hex(unit.getUnitColorType())
#                 nx.draw_networkx_nodes(self.G, pos=self.drawPos, nodelist=n, font_size=8, node_color=c, alpha=1, edge_color='black',node_size=670)
#                 nx.draw_networkx_edges(self.G, self.drawPos, edgelist=edgesToDraw, width=3, edge_color=c, alpha=1)
#         plt.show()
#         return nodes, edges
    
    def getStructuralGwp (self,lcaDb=None): # returns total GWP for structural walls and floor in layout #
        if lcaDb!=None:
            self.structuralGwp = 0.0
            for e in self.edges.values():
                self.structuralGwp+=e.getGwpCost('structural')
            for n in self.nodes.values():
                self.structuralGwp+=n.getFloorGWP(lcaDb)
        return self.structuralGwp


def checkSolutionSpace(layoutRoomCount,unitTypesList,emptySpaceThreshold,it,branchRes,result):
    layoutRoomCount['normal']-=unitTypesList[it]['normal']
    layoutRoomCount['toilet']-=unitTypesList[it]['toilet']
    layoutRoomCount['storage']-=unitTypesList[it]['storage']
    
    if(layoutRoomCount['normal']<0 or layoutRoomCount['toilet']<0 or layoutRoomCount['storage']<0):
        emptySpace = layoutRoomCount['normal']+unitTypesList[it]['normal']+layoutRoomCount['toilet']+unitTypesList[it]['toilet']+layoutRoomCount['storage']+unitTypesList[it]['storage']
        if emptySpace <= emptySpaceThreshold:
            branchRes.sort()
            result[str(branchRes)] = emptySpace
    else:
        branchRes.append(it)
        for i in range(0,len(unitTypesList)):
            checkSolutionSpace(layoutRoomCount.copy(),unitTypesList,emptySpaceThreshold,i,branchRes.copy(),result)