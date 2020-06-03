import Floor_Layout_Syntax.Layout_graph as Layout
import Floor_Layout_Syntax.UserInput as userInp
import Floor_Layout_Syntax.Constraint as con
import numpy as np
import copy 
from datetime import datetime
import Floor_Layout_Syntax.Building as Building
import random
import jsonpickle
import matplotlib.pyplot as plt
import Floor_Layout_Syntax.Parcelized_layout_graph as PLayout
#--------------replace this with root directoy path
rootPath = 'D:\\repos\\next gen space syntax\\'

edges_jsonfilepath =rootPath+'testcases\\2_edges.txt'
nodes_jsonfilepath =rootPath+'testcases\\2_nodes.txt'

pos_path = rootPath+"floorplan_vectors\\node position_vectors_rot_offsets.txt"
lengths_path = rootPath+"floorplan_vectors\\position_vector_lengths.txt"

savefilePath=rootPath+'saved_results\\test\\'
imageRootPath=rootPath+'images\\floorplan_base3.png'

unitTypes={
            1:{
            "roomCount":4,
            "normal":2,
            "toilet":1,
            "storage":1
            },
            2:{
            "roomCount":5,
            "normal":3,
            "toilet":1,
            "storage":1
            },
            3:{
            "roomCount":7,
            "normal":4,
            "toilet":2,
            "storage":1
            },
            4:{
            "roomCount":8,
            "normal":5,
            "toilet":2,
            "storage":1
            },
            5:{
            "roomCount":10,
            "normal":6,
            "toilet":2,
            "storage":2
            }
        }
unitTypeIndex=[1,2,3,4,5]

doorsImplied={
        'left':['1/14','1/15'],
        'middle':['1/9','1/10'],
        'right':['1/4','1/5']
        }
positions=["left", "middle" ,"right"]
start=datetime.now()

layout = Layout.Layout_graph()
layout.importJSON(nodes_jsonfilepath, edges_jsonfilepath)
layout.loadDrawVectors(pos_path, lengths_path,imageRootPath)

##--------------------<LOAD SAVED FLOOR RESULT>
#f= open(savefilePath+"17_happyDict.txt","r")
#layoutz=jsonpickle.decode(f.read())
#f.close()
#[number of clusters][result index][]
#print(layoutz['0'][0][0].getUnitDemandsFulfilled())
#layoutz['0'].getUnitDemandsFulfilled()
##--------------------</LOAD SAVED FLOOR RESULT>


##--------------------<LOAD SAVED BUILDING PARCELATION>
##floorIndex=4
#bldg=Building.Building(layout)
#bldg.loadBuilding(savefilePath)
#seq,dType=bldg.getElevationPermTypeSequence()
##bldg.drawElevation(seq,dType)
###bldg.drawFloorGraph(floorIndex)
##bldg.drawAllFloorGraphs()
##
#bldg.fillEmptyClusters()
#seq,dType=bldg.getElevationPermTypeSequence()
#bldg.drawElevation(seq,dType)
##bldg.drawFloorGraph(floorIndex)
#bldg.drawAllFloorGraphs()
##-------------------</LOAD SAVED BUILDING PARCELATION>

####Test Draw
#layout.drawTraversedPaths(traversedNodesIds=[1, 3, 4, 19, 18], traversedEdgesIds=['1/4', '4/3', '3/19', '19/18'])
#for wall in layout.nodes['1'].getWalls():
#    print (wall.material)
#for node in layout.nodes:
#    print ('node ',node," --> ",layout.nodes[node].getConnectedEdgeIDs())
#for edge in layout.edges:
#    print ('edge ',edge)

#density = nx.density(layout.G)
#print("Network density:", density)

##=============================fcfs method
#tempFloorplans=set()
##first run
#prefs=con.Constraint(['1/4','1/5','1/10','1/9'],{
#        "roomCount":10,
#        "toilet":0,
#        "kitchen":0,
#        "storeroom":0
#        })
#resultFloorplans=layout.generatePossibleUnits(prefs=prefs)
#print("---first iteration---")
#for res in resultFloorplans:
#    print(res.doorSequence)
#    print(res.unitSequence)
#    print(res.unusedToOverallRatio)
#    
##second run
#prefs=con.Constraint(['1/4','1/5','1/10'],{
#        "roomCount":10,
#        "toilet":0,
#        "kitchen":0,
#        "storeroom":0
#        })
#for floorplan in resultFloorplans:
#    tempFloorplans.update(layout.generatePossibleUnits(prefs=prefs,floorplan=floorplan))
#if len(tempFloorplans)>0:
#    resultFloorplans=set(tempFloorplans)
#else:
#    print("Iteration ended at.. ")
#    
#print("\n---final results---")
#for res in resultFloorplans:
#    print(res.doorSequence)
#    layout.testFloorplanScore(res)
#===================================================
#doorEdges=layout.doorEdgeIds
#prefs=[]
##--test prefs
#prefs.append(con.Constraint(2,0.75,['1/15'],unitTypes[2]))
#prefs.append(con.Constraint(3,0.2,['1/14'],unitTypes[1]))
##prefs.append(con.Constraint(4,0.5,['1/10'],unitTypes[0]))
#happyRes,utilRes=layout.generateParcelizationPermutations(str(0),prefs,savefilePath) #function returns tuple of happy and utiliy result lists

####-------------------------------------<MAIN ALORITHM>----------------------------------
##<LOAD DEMAND DISTRIBTUION>
hdbDistribution = [0.133, 0.275, 0.211, 0.124, 0.147, 0.11] # from HDB paper
posDistribution = [0.1, 0.2, 0.7]
floorLevels = [[1,5],[6,10], [11,15], [16,20], [21,25], [26,30]]
u = userInp.User_input(numFloors=30, numDoors=6, positions=positions, unitTypes=unitTypeIndex, levelRanges=floorLevels, positionRanges=[[1, 2],[3,4] ,[5, 6]], floorDistribution=hdbDistribution, positionDistribution=None) # from HDB paper
df=u.genFakeUnitTypePrefs(numPeople=500, binned=True, RAYformat=False, savefilePath=savefilePath)
#binned true-p and f and false-p and f,


prefDf=copy.copy(u.binnedBldg)  #dataframe which contains list of user demands for cells
probDf=u.calcBinnedProb(prefDf) #dataframe which contains probability of unit occurring for cells
#print(probDf)
#print(prefDf)
##</LOAD DEMAND DISTRIBTUION>

floorRanges=prefDf.index.values.tolist()
#print ('rows ' ,floorRanges)
#print ('cols ' ,prefDf.keys())
leftovers={}
buildingResult={}

###<PRETTY PRINT DATAFRAME>
###x=np.arange(len(unitTypes))
##axes = plt.gca()
##width=0.8
##unitTypeLegend=['T1','T2','T3','T4','T5']
##color=[[0.031, 0.612, 0.533], [0.643, 0.137, 0.506], [1, 0.773, 0.235], [0.922, 0.329, 0.467], [0.388, 0.647, 0.329]]
##fig, axs = plt.subplots(ncols=3,nrows=6,subplot_kw={'xticks': [],'yticks': []})
##for row in reversed(range(len(floorRanges))):
##    for col in range(len(positions)):
##        demandCount=[0]*5
##        for n in prefDf.loc[floorRanges[row],positions[col]]:
##            demandCount[n-1]+=1
##        ax=axs[len(floorRanges)-1-row,col]  #plotting in reverse to reflect bottom up structure of a building
##        ax.set_ylim([0,1])
##        unitProbability=probDf.loc[floorRanges[row],positions[col]]
##        rects=ax.bar(unitTypeLegend,unitProbability,width,color=color)
###        if row==len(floorRanges)-1 and col<3:
###            ax.set_title(positions[col])
###        if col==0:
###            ax.set_ylabel(floorRanges[row])
###fig.tight_layout()
###plt.show()
###</PRETTY PRINT DATAFRAME>
#
##<PARCELIZATION>
##run permutation algorithm per floor in the dataframe
for fR in floorRanges:
    floorIndex=fR.split('-',1)  #[0]-> start index; [1]-> end index
    floorLeftovers={}

    #Iterating through floors in range
    #-----------------------------------------------
    for floor in range(int(floorIndex[0]),int(floorIndex[1])+1):
        floorPrefs=[]
        for generalLocation in prefDf.keys():
            for location in doorsImplied[generalLocation]:
                unitPreferences=prefDf.loc[fR,generalLocation]
                #-would be nice to have a switch case here to increase readability
                if len(unitPreferences)<1:
                    #since no demands, check if there are leftover demands in this floor range
                    if generalLocation in floorLeftovers:
                        floorPrefs.append(floorLeftovers[generalLocation][0])
                        if len(floorLeftovers[generalLocation])<1: del floorLeftovers[generalLocation]
                    else:
                        continue
                elif unitPreferences[0]==0:
                    unitPreferences.remove(0)
                    if generalLocation in floorLeftovers:
                        floorPrefs.append(floorLeftovers[generalLocation][0])
                        if len(floorLeftovers[generalLocation])<1: del floorLeftovers[generalLocation]
                    else:
                        continue
                else:
                    unitProbability=probDf.loc[fR,generalLocation]
                    unit=np.random.choice(a=unitTypeIndex,p=unitProbability)
                    floorPrefs.append(con.Constraint(roomType=unit,prefWeight=1,prefDoors=doorsImplied[generalLocation],roomConstraints=unitTypes[unit]))
                    unitPreferences.remove(unit)
                    probDf.loc[fR,generalLocation]=u.calcProbFromPref(unitPreferences)

        #Process permutation for demands on floor
        #-----------------------------------------------
        happyRes,utilRes=layout.generateParcelizationPermutations(str(floor),floorPrefs,savefilePath) #function returns tuple of happy and utiliy result lists

        #Selection of the layout and collating leftovers
        #-----------------------------------------------
        happyRes=random.choice(happyRes) #done randomly for now
        buildingResult[floor]=happyRes[0]

        exportPath=savefilePath+'bldg.txt'
        f= open(exportPath,"w+")
        f.write(jsonpickle.encode(buildingResult))
        f.close()

        #utilRes=random.choice(utilRes) #ignore for now
        #the results are a tuple of (layout,demands,leftover index); so the next line checks if there are leftovers
        if happyRes[2]!=None:
            for i in range(happyRes[2],len(happyRes[1])):
                if generalLocation in floorLeftovers:
                    floorLeftovers[generalLocation].append(happyRes[1][i])
                else:
                    floorLeftovers[generalLocation]=[happyRes[1][i]]
    leftovers[fR]=floorLeftovers
    exportPath=savefilePath+'left.txt'
    f= open(exportPath,"w+")
    f.write(jsonpickle.encode(leftovers))
    f.close()
##</PARCELIZATION>
####-------------------------------------</MAIN ALORITHM>----------------------------------

#layout.printSavedResults(str(1),savefilePath)
#parcelizedLayout=layout.getRandomSavedResultLayout(str(2),savefilePath)
#print(parcelizedLayout.unitSequence)
    
print('Start Time: ')
print(start)
print('End Time: ')
print(datetime.now())