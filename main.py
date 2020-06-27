import Floor_Layout_Syntax.Layout_graph as Layout
import Floor_Layout_Syntax.Building as Building
import Floor_Layout_Syntax.Constants as Constants
import numpy as np
import os
from datetime import datetime
import json
import copy

#Known issues:
#-a unit type may not be generated if floorRange specified is too small and probability of demand is low
# -> to fix: increase floorRange in Floor_Layout_Syntax.Constants
#-positional demand

#================================PATH VARIABLES=================================
rootPath = os.path.dirname(__file__)
edges_jsonfilepath = os.path.join(rootPath, 'testcases','3_edges.txt')  #testfiles
nodes_jsonfilepath = os.path.join(rootPath, 'testcases','3_nodes.txt')
# lcaDbPath = os.path.join(rootPath, 'testcases','Quartz_db_2019_Jan.csv')
# results_directory = os.path.join(rootPath,'saved_results')

'''
-sample inputs:
unitTypes=[{
    "unitTypeIndex":0,
    "color":(0.031, 0.612, 0.533),
    "roomCount":1,
    "normal":1,
    "toilet":0,
    "storage":0
    },
    {
    "unitTypeIndex":1,
    "color":(0.643, 0.137, 0.506),
    "roomCount":5,
    "normal":3,
    "toilet":1,
    "storage":1
    },
    {
    "unitTypeIndex":2,
    "color":(1, 0.773, 0.235),
    "roomCount":7,
    "normal":4,
    "toilet":2,
    "storage":1
    },
    {
    "unitTypeIndex":3,
    "color":(0.922, 0.329, 0.467),
    "roomCount":8,
    "normal":5,
    "toilet":2,
    "storage":1
    },
    {
    "unitTypeIndex":4,
    "color":(0.388, 0.647, 0.329),
    "roomCount":10,
    "normal":6,
    "toilet":2,
    "storage":2
    }]

-demandProjection={'2020':[0.10239081, 0.18119785, 0.38637962, 0.23033209, 0.09969962],
                      '2040':[0.14256652, 0.17999695, 0.35843778, 0.22383094, 0.0951678 ],
                      '2060':[0.18699427, 0.17764625, 0.33543391, 0.21086532, 0.08906024],
                      '2080':[0.22413532, 0.17169741, 0.31204038, 0.2042384 , 0.08788849]}
'''
def parcelateBuilding(nodesJson,edgesJson,floorCount,demandProjection,unitTypes):    
    layout = Layout.Layout_graph(unitTypes)
    layout.loadJson(nodesJson,edgesJson)
    building=Building.Building(layout,floorCount,3,4)
    
    result = dict()
    for year,demand in demandProjection.items():
        print("===processing year "+year+" demands===")
        b=copy.deepcopy(building)
        d={'1-'+str(floorCount):np.array(demand)}
        b.parcelate(d)
        result[year] = b.getResultBuilding()
    return json.dumps(result)

    
if __name__== "__main__":
    #test prog- reads json from test files and constants 
    f= open(nodes_jsonfilepath,"r")
    nodesJson = f.read()
    f.close()
    
    f= open(edges_jsonfilepath,"r")
    edgesJson = f.read()
    f.close()
    
    demandProjection={'2020':[0.10239081, 0.18119785, 0.38637962, 0.23033209, 0.09969962],
                      '2040':[0.14256652, 0.17999695, 0.35843778, 0.22383094, 0.0951678 ],
                      '2060':[0.18699427, 0.17764625, 0.33543391, 0.21086532, 0.08906024],
                      '2080':[0.22413532, 0.17169741, 0.31204038, 0.2042384 , 0.08788849]}
    print("//jsonResult//")
    print(parcelateBuilding(nodesJson,edgesJson,4,demandProjection,Constants.UNIT_TYPES))