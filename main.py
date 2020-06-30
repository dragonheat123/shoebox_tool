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

inputs = '[[{"id": "0", "roomType": "outside", "floorArea": 0, "floorMatId": "CP032", "innerWalls": []}, {"id": "1", "roomType": "service", "floorArea": 0, "floorMatId": "CP032", "innerWalls": []}, {"id": "2", "roomType": "normal", "floorArea": 15.119999999999488, "floorMatId": "CP032", "innerWalls": []}, {"id": "3", "roomType": "normal", "floorArea": 15.119999999999488, "floorMatId": "CP032", "innerWalls": []}, {"id": "4", "roomType": "normal", "floorArea": 21.6, "floorMatId": "CP032", "innerWalls": []}, {"id": "5", "roomType": "toilet", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": []}, {"id": "6", "roomType": "storage", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": []}, {"id": "7", "roomType": "normal", "floorArea": 15.120000000000317, "floorMatId": "CP032", "innerWalls": []}, {"id": "8", "roomType": "normal", "floorArea": 15.119999999999969, "floorMatId": "CP032", "innerWalls": []}, {"id": "9", "roomType": "normal", "floorArea": 15.119999999999939, "floorMatId": "CP032", "innerWalls": []}, {"id": "10", "roomType": "normal", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": []}, {"id": "11", "roomType": "toilet", "floorArea": 8.640000000000192, "floorMatId": "CP032", "innerWalls": []}, {"id": "12", "roomType": "storage", "floorArea": 8.639999999999782, "floorMatId": "CP032", "innerWalls": []}, {"id": "13", "roomType": "toilet", "floorArea": 8.640000000000335, "floorMatId": "CP032", "innerWalls": []}, {"id": "14", "roomType": "normal", "floorArea": 21.60000000000002, "floorMatId": "CP032", "innerWalls": []}, {"id": "15", "roomType": "normal", "floorArea": 15.11999999999985, "floorMatId": "CP032", "innerWalls": []}, {"id": "16", "roomType": "normal", "floorArea": 15.119999999999484, "floorMatId": "CP032", "innerWalls": []}, {"id": "17", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "18", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "19", "roomType": "normal", "floorArea": 15.120000000000339, "floorMatId": "CP032", "innerWalls": []}, {"id": "20", "roomType": "normal", "floorArea": 15.120000000000315, "floorMatId": "CP032", "innerWalls": []}, {"id": "21", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "22", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "23", "roomType": "storage", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": []}, {"id": "24", "roomType": "toilet", "floorArea": 8.640000000000496, "floorMatId": "CP032", "innerWalls": []}, {"id": "25", "roomType": "normal", "floorArea": 21.600000000000072, "floorMatId": "CP032", "innerWalls": []}, {"id": "26", "roomType": "normal", "floorArea": 21.60000000000008, "floorMatId": "CP032", "innerWalls": []}, {"id": "27", "roomType": "toilet", "floorArea": 8.640000000000363, "floorMatId": "CP032", "innerWalls": []}, {"id": "28", "roomType": "storage", "floorArea": 8.63999999999982, "floorMatId": "CP032", "innerWalls": []}, {"id": "29", "roomType": "toilet", "floorArea": 8.640000000000231, "floorMatId": "CP032", "innerWalls": []}, {"id": "30", "roomType": "normal", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": []}, {"id": "31", "roomType": "normal", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": []}, {"id": "32", "roomType": "toilet", "floorArea": 8.6400000000002, "floorMatId": "CP032", "innerWalls": []}, {"id": "33", "roomType": "storage", "floorArea": 8.63999999999979, "floorMatId": "CP032", "innerWalls": []}, {"id": "34", "roomType": "toilet", "floorArea": 8.640000000000335, "floorMatId": "CP032", "innerWalls": []}, {"id": "35", "roomType": "normal", "floorArea": 21.6, "floorMatId": "CP032", "innerWalls": []}], [{"isAccessible": true, "edgeId": "2/3", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "2/5", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "2/6", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "3/4", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "3/5", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "4/5", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "4/14", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "5/6", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "7/8", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "7/10", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "7/11", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "8/9", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "8/11", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "8/12", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "8/13", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "9/13", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "9/14", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "10/11", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "10/35", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "11/12", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "12/13", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "13/14", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "15/16", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "15/23", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "15/24", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "16/24", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "16/25", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "17/18", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "17/26", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "17/27", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "18/19", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "18/27", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "18/28", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "18/29", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "19/29", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "19/30", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "20/21", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "20/31", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "20/32", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "21/22", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "21/32", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "21/33", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "21/34", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "22/34", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "22/35", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "23/24", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "24/25", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "25/26", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "26/27", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "27/28", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "28/29", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "29/30", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "30/31", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "31/32", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "32/33", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "33/34", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "34/35", "adjWalls": [], "isDoorway": false}, {"edgeId": "1/25", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/26", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/31", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/30", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/35", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/10", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/14", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/4", "isAccessible": true, "adjWalls": [], "isDoorway": true}]]'

inputs = json.loads(inputs)

#sample inputs:
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

demandProjection={'2020':[0.10239081, 0.18119785, 0.38637962, 0.23033209, 0.09969962],
                      '2040':[0.14256652, 0.17999695, 0.35843778, 0.22383094, 0.0951678 ],
                      '2060':[0.18699427, 0.17764625, 0.33543391, 0.21086532, 0.08906024],
                      '2080':[0.22413532, 0.17169741, 0.31204038, 0.2042384 , 0.08788849]}

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

nodesJson = json.dumps(inputs[0])
edgesJson = json.dumps(inputs[1])

output = parcelateBuilding(nodesJson, edgesJson, 10, demandProjection, unitTypes)

    
# if __name__== "__main__":
#     #test prog- reads json from test files and constants 
#     f= open(nodes_jsonfilepath,"r")
#     nodesJson = f.read()
#     f.close()
    
#     f= open(edges_jsonfilepath,"r")
#     edgesJson = f.read()
#     f.close()
    
#     demandProjection={'2020':[0.10239081, 0.18119785, 0.38637962, 0.23033209, 0.09969962],
#                       '2040':[0.14256652, 0.17999695, 0.35843778, 0.22383094, 0.0951678 ],
#                       '2060':[0.18699427, 0.17764625, 0.33543391, 0.21086532, 0.08906024],
#                       '2080':[0.22413532, 0.17169741, 0.31204038, 0.2042384 , 0.08788849]}
#     print("//jsonResult//")
#     print(parcelateBuilding(nodesJson,edgesJson,4,demandProjection,Constants.UNIT_TYPES))