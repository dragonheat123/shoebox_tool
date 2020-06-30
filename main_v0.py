import Floor_Layout_Syntax.Layout_graph_v2 as Layout
import Floor_Layout_Syntax.Building_v2 as Building
import numpy as np
import os
import copy
import json
import time

#Known issues:
#-a unit type may not be generated if floorRange specified is too small and probability of demand is low
# -> to fix: increase floorRange in Floor_Layout_Syntax.Constants
#-positional demand

#================================PATH VARIABLES=================================
rootPath = os.path.dirname(__file__)
# testcase = "c1n"
# edges_jsonfilepath = os.path.join(rootPath, 'testcases',testcase+'_edges.txt')
# nodes_jsonfilepath = os.path.join(rootPath, 'testcases',testcase+'_nodes.txt')
lcaDbPath = os.path.join(rootPath, 'testcases','testcase_db.csv')
results_directory = os.path.join(rootPath,'saved_results')

           
def createParcelations(nodesJson,edgesJson,floorCount,demandProjection,unitTypes):
    layout = Layout.Layout_graph(unitTypes)
    layout.loadJson(nodesJson, edgesJson, lcaDbPath)
    building=Building.Building(layout)
    
    for year,demand in demandProjection.items():
         print("===processing year "+year+" demands===")
         b=copy.deepcopy(building)
         d={'1-'+str(floorCount):np.array(demand)}
         b.parcelate(d)
         res = b.getBuildingLayoutResults()
         f= open(os.path.join(results_directory,year+'.txt'),"w")
         f.write(json.dumps(res))
         f.close()
         print("---successfully results for year "+year+"---")
         
#==================================MAIN PROGRAM==================================
def main():
#    #**NOTE: Either generate new -OR- load parcelation
#    #=================================================
#    #---generate and save new building parcelation---
#    #=================================================
    inputs = '[[{"id": "0", "roomType": "outside", "floorArea": 0, "floorMatId": "CP032", "innerWalls": []}, {"id": "1", "roomType": "service", "floorArea": 0, "floorMatId": "CP032", "innerWalls": []}, {"id": "2", "roomType": "normal", "floorArea": 21.6, "floorMatId": "CP032", "innerWalls": []}, {"id": "3", "roomType": "toilet", "floorArea": 8.640000000000335, "floorMatId": "CP032", "innerWalls": []}, {"id": "4", "roomType": "storage", "floorArea": 8.63999999999979, "floorMatId": "CP032", "innerWalls": []}, {"id": "5", "roomType": "toilet", "floorArea": 8.6400000000002, "floorMatId": "CP032", "innerWalls": []}, {"id": "6", "roomType": "normal", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": []}, {"id": "7", "roomType": "normal", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": []}, {"id": "8", "roomType": "toilet", "floorArea": 8.640000000000231, "floorMatId": "CP032", "innerWalls": []}, {"id": "9", "roomType": "storage", "floorArea": 8.63999999999982, "floorMatId": "CP032", "innerWalls": []}, {"id": "10", "roomType": "toilet", "floorArea": 8.640000000000363, "floorMatId": "CP032", "innerWalls": []}, {"id": "11", "roomType": "normal", "floorArea": 21.60000000000008, "floorMatId": "CP032", "innerWalls": []}, {"id": "12", "roomType": "normal", "floorArea": 21.600000000000072, "floorMatId": "CP032", "innerWalls": []}, {"id": "13", "roomType": "toilet", "floorArea": 8.640000000000496, "floorMatId": "CP032", "innerWalls": []}, {"id": "14", "roomType": "storage", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": []}, {"id": "15", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "16", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "17", "roomType": "normal", "floorArea": 15.120000000000315, "floorMatId": "CP032", "innerWalls": []}, {"id": "18", "roomType": "normal", "floorArea": 15.120000000000339, "floorMatId": "CP032", "innerWalls": []}, {"id": "19", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "20", "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": []}, {"id": "21", "roomType": "normal", "floorArea": 15.119999999999484, "floorMatId": "CP032", "innerWalls": []}, {"id": "22", "roomType": "normal", "floorArea": 15.11999999999985, "floorMatId": "CP032", "innerWalls": []}, {"id": "23", "roomType": "normal", "floorArea": 21.60000000000002, "floorMatId": "CP032", "innerWalls": []}, {"id": "24", "roomType": "toilet", "floorArea": 8.640000000000335, "floorMatId": "CP032", "innerWalls": []}, {"id": "25", "roomType": "storage", "floorArea": 8.639999999999782, "floorMatId": "CP032", "innerWalls": []}, {"id": "26", "roomType": "toilet", "floorArea": 8.640000000000192, "floorMatId": "CP032", "innerWalls": []}, {"id": "27", "roomType": "normal", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": []}, {"id": "28", "roomType": "normal", "floorArea": 15.119999999999939, "floorMatId": "CP032", "innerWalls": []}, {"id": "29", "roomType": "normal", "floorArea": 15.119999999999969, "floorMatId": "CP032", "innerWalls": []}, {"id": "30", "roomType": "normal", "floorArea": 15.120000000000317, "floorMatId": "CP032", "innerWalls": []}, {"id": "31", "roomType": "storage", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": []}, {"id": "32", "roomType": "toilet", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": []}, {"id": "33", "roomType": "normal", "floorArea": 21.6, "floorMatId": "CP032", "innerWalls": []}, {"id": "34", "roomType": "normal", "floorArea": 15.119999999999488, "floorMatId": "CP032", "innerWalls": []}, {"id": "35", "roomType": "normal", "floorArea": 15.119999999999488, "floorMatId": "CP032", "innerWalls": []}], [{"isAccessible": true, "edgeId": "2/3", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "2/15", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "2/27", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "3/4", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "3/15", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "3/16", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "4/5", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "4/16", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "5/6", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "5/16", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "5/17", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "6/7", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "6/17", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "7/8", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "7/18", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "8/9", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "8/18", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "8/19", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "9/10", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "9/19", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "10/11", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "10/19", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "10/20", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "11/12", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "11/20", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "12/13", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "12/21", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "13/14", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "13/21", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "13/22", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "14/22", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "15/16", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "16/17", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "18/19", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "19/20", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "21/22", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "23/24", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "23/28", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "23/33", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "24/25", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "24/28", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "24/29", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "25/26", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "25/29", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "26/27", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "26/29", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "26/30", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "27/30", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "28/29", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "29/30", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "31/32", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "31/35", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "32/33", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "32/34", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "32/35", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "33/34", "adjWalls": [], "isDoorway": false}, {"isAccessible": true, "edgeId": "34/35", "adjWalls": [], "isDoorway": false}, {"edgeId": "1/12", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/11", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/7", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/6", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/2", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/27", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/33", "isAccessible": true, "adjWalls": [], "isDoorway": true}, {"edgeId": "1/23", "isAccessible": true, "adjWalls": [], "isDoorway": true}]]'
    inputs = json.loads(inputs)
    
    demandProjection={'2020':[0.10239081, 0.18119785, 0.38637962, 0.23033209, 0.09969962],
               '2040':[0.14256652, 0.17999695, 0.35843778, 0.22383094, 0.0951678 ],
               '2060':[0.18699427, 0.17764625, 0.33543391, 0.21086532, 0.08906024],
               '2080':[0.22413532, 0.17169741, 0.31204038, 0.2042384 , 0.08788849]}
    
    unitTypes=[{
    "unitTypeIndex":0,
    "color":(0.031, 0.612, 0.533),
    "roomCount":3,
    "normal":1,
    "toilet":1,
    "storage":1
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
    
    createParcelations(inputs[0],inputs[1],30,demandProjection,unitTypes)

    
    
if __name__== "__main__":
    tic = time.time()
    main()
    print("timetaken: ",time.time()-tic,"s")