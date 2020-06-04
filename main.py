import Floor_Layout_Syntax.Constants as Constants
import Floor_Layout_Syntax.Layout_graph as Layout
import Floor_Layout_Syntax.Building as Building
import numpy as np
import os
from datetime import datetime
import pprint
import copy

#Known issues:
#-a unit type may not be generated if floorRange specified is too small and probability of demand is low
# -> to fix: increase floorRange in Floor_Layout_Syntax.Constants
#-positional demand

#================================PATH VARIABLES=================================
#--replace rootPath with root directory path
#--windows ver
rootPath = 'D:\\repos\\shoebox_tool\\'
edges_jsonfilepath =rootPath+'testcases\\2_edges.txt'
nodes_jsonfilepath =rootPath+'testcases\\2_nodes.txt'
lcaDbPath=rootPath+'testcases\\Quartz_db_2019_Jan.csv'
imageRootPath=rootPath+'images\\floorplan_base3.png'

pos_path = rootPath+"floorplan_vectors\\node position_vectors_rot_offsets.txt"
lengths_path = rootPath+"floorplan_vectors\\position_vector_lengths.txt"

results_directory=rootPath+'saved_results\\'
parcelation_db=results_directory+'parcelation_db'
saveFilePath=results_directory+datetime.now().strftime("%Y-%m-%d_%H%M")+'\\'
#loadFilePath=results_directory+"2020-03-23_1208"+"\\"
#--------------------------------------------------------------------------------
#--mac ver
# rootPath = '/Users/zack_sutd/Dropbox (Personal)/SUTD/PostDoc/Space Syntax/next-gen-space-syntax/'
# edges_jsonfilepath =rootPath+'testcases/2_edges.txt'
# nodes_jsonfilepath =rootPath+'testcases/2_nodes.txt'
# lcaDbPath=rootPath+'testcases/Quartz_db_2019_Jan.csv'
# imageRootPath=rootPath+'images/floorplan_base3.png'

# pos_path = rootPath+"floorplan_vectors/node position_vectors_rot_offsets.txt"
# lengths_path = rootPath+"floorplan_vectors/position_vector_lengths.txt"

# results_directory=rootPath+'saved_results/'
# saveFilePath=results_directory+datetime.now().strftime("%Y-%m-%d_%H%M")+'/'
# loadFilePath=results_directory+"2020-03-23_1208"+"/"
#--------------------------------------------------------------------------------



#==================================MAIN PROGRAM==================================
def main():
    #**NOTE: Either generate new -OR- load parcelation
    #=================================================
    #---generate and save new building parcelation---
    #=================================================
    demandProjection={'2020':[0.10239081, 0.18119785, 0.38637962, 0.23033209, 0.09969962],
                      '2040':[0.14256652, 0.17999695, 0.35843778, 0.22383094, 0.0951678 ],
                      '2060':[0.18699427, 0.17764625, 0.33543391, 0.21086532, 0.08906024],
                      '2080':[0.22413532, 0.17169741, 0.31204038, 0.2042384 , 0.08788849]}
    
    layout = Layout.Layout_graph()
    layout.importJSON(nodes_jsonfilepath, edges_jsonfilepath,lcaDbPath)
    layout.loadDrawVectors(pos_path, lengths_path,imageRootPath)
    building=Building.Building(layout)
    
    for year,demand in demandProjection.items():
        print("===processing year "+year+" demands===")
        b=copy.deepcopy(building)
        d={'1-30':np.array(demand)}
        b.parcelate(d)
    
        saveFilePath=saveFilePath+year+'/'
        os.makedirs(saveFilePath, exist_ok=True) #creates a new folder at saveFilePath for results
        b.save(saveFilePath)
        print("---successfully saved results for year "+year+"---")
    
    #=================================================
    #---load parcelated building---
    #=================================================
    # building=Building.loadBuilding(loadFilePath)
    
    ##=================DRAW RESULTS====================
    building.drawDemographicModelChart()   #plot of demographic demand for unit types
    building.drawComparisonChart()  #compares unit distribution to demographic demand
    building.drawElevation()
    building.drawFloorGraph(3)
    building.drawAllFloorGraphs()
    
    ##====================COMPARISON===================
    b1=Building.loadBuilding(results_directory+"2020\\")
    b2=Building.loadBuilding(results_directory+"2040\\")
    b1.drawComparisonChart()
    b2.drawComparisonChart()
    pp = pprint.PrettyPrinter(indent=4)
    
    floor=12
    print("--Floor "+str(floor)+" changes:")
    pp.pprint(b1.compareFloorWallChanges(b2,floor))
    b1.drawFloorGraph(floor)
    b2.drawFloorGraph(floor)
    
    ##--Cumulative floor changes of the entire building
    print("--Cumulative changes:")
    pp.pprint(b1.compareBuildingWallChanges(b2))
    
if __name__== "__main__":
    main()