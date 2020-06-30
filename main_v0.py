import Floor_Layout_Syntax.Layout_graph_v2 as Layout
import Floor_Layout_Syntax.Building_v2 as Building
import numpy as np
import os
import copy
import json

#Known issues:
#-a unit type may not be generated if floorRange specified is too small and probability of demand is low
# -> to fix: increase floorRange in Floor_Layout_Syntax.Constants
#-positional demand

#================================PATH VARIABLES=================================
rootPath = os.path.dirname(__file__)
testcase = "c1n"
edges_jsonfilepath = os.path.join(rootPath, 'testcases',testcase+'_edges.txt')
nodes_jsonfilepath = os.path.join(rootPath, 'testcases',testcase+'_nodes.txt')
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
    inputs = '[[{"id": "0", "roomType": "outside", "floorArea": 0, "floorMatId": "CP032", "innerWalls": []}, {"id": "1", "roomType": "service", "floorArea": 0, "floorMatId": "CP032", "innerWalls": []}, {"id": 2, "roomType": "normal", "floorArea": 15.119999999999488, "floorMatId": "CP032", "innerWalls": [], "center": [40.54284228736569, 6.883198095944001, 0]}, {"id": 3, "roomType": "normal", "floorArea": 15.119999999999488, "floorMatId": "CP032", "innerWalls": [], "center": [36.942842287365806, 6.883198095944001, 0]}, {"id": 4, "roomType": "storage", "floorArea": 21.6, "floorMatId": "CP032", "innerWalls": [], "center": [35.59284228736577, 2.383198095943989, 0]}, {"id": 5, "roomType": "toilet", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": [], "center": [38.74284228736582, 2.383198095943982, 0]}, {"id": 6, "roomType": "storage", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": [], "center": [40.542842287365914, 2.383198095943982, 0]}, {"id": 7, "roomType": "normal", "floorArea": 15.120000000000317, "floorMatId": "CP032", "innerWalls": [], "center": [22.542842287365662, 6.883198095944001, 0]}, {"id": 8, "roomType": "normal", "floorArea": 15.119999999999969, "floorMatId": "CP032", "innerWalls": [], "center": [26.142842287365706, 6.883198095944001, 0]}, {"id": 9, "roomType": "normal", "floorArea": 15.119999999999939, "floorMatId": "CP032", "innerWalls": [], "center": [29.742842287365697, 6.883198095944001, 0]}, {"id": 10, "roomType": "storage", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": [], "center": [21.192842287365703, 2.3831980959439885, 0]}, {"id": 11, "roomType": "toilet", "floorArea": 8.640000000000192, "floorMatId": "CP032", "innerWalls": [], "center": [24.342842287365723, 2.3831980959439876, 0]}, {"id": 12, "roomType": "storage", "floorArea": 8.639999999999782, "floorMatId": "CP032", "innerWalls": [], "center": [26.142842287365717, 2.383198095943987, 0]}, {"id": 13, "roomType": "toilet", "floorArea": 8.640000000000335, "floorMatId": "CP032", "innerWalls": [], "center": [27.942842287365725, 2.3831980959439867, 0]}, {"id": 14, "roomType": "storage", "floorArea": 21.60000000000002, "floorMatId": "CP032", "innerWalls": [], "center": [31.09284228736577, 2.383198095943989, 0]}, {"id": 15, "roomType": "normal", "floorArea": 15.11999999999985, "floorMatId": "CP032", "innerWalls": [], "center": [-17.057157712634385, 6.883198095944008, 0]}, {"id": 16, "roomType": "normal", "floorArea": 15.119999999999484, "floorMatId": "CP032", "innerWalls": [], "center": [-13.457157712634459, 6.8831980959440076, 0]}, {"id": 17, "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": [], "center": [-6.257157712634356, 6.883198095944008, 0]}, {"id": 18, "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": [], "center": [-2.657157712634362, 6.883198095944008, 0]}, {"id": 19, "roomType": "normal", "floorArea": 15.120000000000339, "floorMatId": "CP032", "innerWalls": [], "center": [0.9428422873656748, 6.883198095944005, 0]}, {"id": 20, "roomType": "normal", "floorArea": 15.120000000000315, "floorMatId": "CP032", "innerWalls": [], "center": [8.142842287365607, 6.883198095944008, 0]}, {"id": 21, "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": [], "center": [11.742842287365644, 6.883198095944008, 0]}, {"id": 22, "roomType": "normal", "floorArea": 15.119999999999958, "floorMatId": "CP032", "innerWalls": [], "center": [15.342842287365638, 6.883198095944008, 0]}, {"id": 23, "roomType": "storage", "floorArea": 8.640000000000466, "floorMatId": "CP032", "innerWalls": [], "center": [-17.05715771263457, 2.383198095943989, 0]}, {"id": 24, "roomType": "toilet", "floorArea": 8.640000000000496, "floorMatId": "CP032", "innerWalls": [], "center": [-15.257157712634474, 2.3831980959440027, 0]}, {"id": 25, "roomType": "storage", "floorArea": 21.600000000000072, "floorMatId": "CP032", "innerWalls": [], "center": [-12.107157712634425, 2.3831980959440027, 0]}, {"id": 26, "roomType": "storage", "floorArea": 21.60000000000008, "floorMatId": "CP032", "innerWalls": [], "center": [-7.607157712634424, 2.3831980959440036, 0]}, {"id": 27, "roomType": "toilet", "floorArea": 8.640000000000363, "floorMatId": "CP032", "innerWalls": [], "center": [-4.4571577126343875, 2.3831980959440013, 0]}, {"id": 28, "roomType": "storage", "floorArea": 8.63999999999982, "floorMatId": "CP032", "innerWalls": [], "center": [-2.657157712634376, 2.3831980959439987, 0]}, {"id": 29, "roomType": "toilet", "floorArea": 8.640000000000231, "floorMatId": "CP032", "innerWalls": [], "center": [-0.857157712634379, 2.383198095943999, 0]}, {"id": 30, "roomType": "storage", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": [], "center": [2.292842287365641, 2.3831980959439956, 0]}, {"id": 31, "roomType": "storage", "floorArea": 21.60000000000007, "floorMatId": "CP032", "innerWalls": [], "center": [6.792842287365642, 2.3831980959439956, 0]}, {"id": 32, "roomType": "toilet", "floorArea": 8.6400000000002, "floorMatId": "CP032", "innerWalls": [], "center": [9.94284228736566, 2.3831980959439942, 0]}, {"id": 33, "roomType": "storage", "floorArea": 8.63999999999979, "floorMatId": "CP032", "innerWalls": [], "center": [11.742842287365658, 2.3831980959439942, 0]}, {"id": 34, "roomType": "toilet", "floorArea": 8.640000000000335, "floorMatId": "CP032", "innerWalls": [], "center": [13.54284228736567, 2.3831980959439942, 0]}, {"id": 35, "roomType": "storage", "floorArea": 21.6, "floorMatId": "CP032", "innerWalls": [], "center": [16.692842287365703, 2.383198095943996, 0]}], [{"isAccessible": true, "edgeId": "2/3", "adjWalls": []}, {"isAccessible": true, "edgeId": "2/5", "adjWalls": []}, {"isAccessible": true, "edgeId": "2/6", "adjWalls": []}, {"isAccessible": true, "edgeId": "3/4", "adjWalls": []}, {"isAccessible": true, "edgeId": "3/5", "adjWalls": []}, {"isAccessible": true, "edgeId": "4/5", "adjWalls": []}, {"isAccessible": true, "edgeId": "4/14", "adjWalls": []}, {"isAccessible": true, "edgeId": "5/6", "adjWalls": []}, {"isAccessible": true, "edgeId": "7/8", "adjWalls": []}, {"isAccessible": true, "edgeId": "7/10", "adjWalls": []}, {"isAccessible": true, "edgeId": "7/11", "adjWalls": []}, {"isAccessible": true, "edgeId": "8/9", "adjWalls": []}, {"isAccessible": true, "edgeId": "8/11", "adjWalls": []}, {"isAccessible": true, "edgeId": "8/12", "adjWalls": []}, {"isAccessible": true, "edgeId": "8/13", "adjWalls": []}, {"isAccessible": true, "edgeId": "9/13", "adjWalls": []}, {"isAccessible": true, "edgeId": "9/14", "adjWalls": []}, {"isAccessible": true, "edgeId": "10/11", "adjWalls": []}, {"isAccessible": true, "edgeId": "10/35", "adjWalls": []}, {"isAccessible": true, "edgeId": "11/12", "adjWalls": []}, {"isAccessible": true, "edgeId": "12/13", "adjWalls": []}, {"isAccessible": true, "edgeId": "13/14", "adjWalls": []}, {"isAccessible": true, "edgeId": "15/16", "adjWalls": []}, {"isAccessible": true, "edgeId": "15/23", "adjWalls": []}, {"isAccessible": true, "edgeId": "15/24", "adjWalls": []}, {"isAccessible": true, "edgeId": "16/24", "adjWalls": []}, {"isAccessible": true, "edgeId": "16/25", "adjWalls": []}, {"isAccessible": true, "edgeId": "17/18", "adjWalls": []}, {"isAccessible": true, "edgeId": "17/26", "adjWalls": []}, {"isAccessible": true, "edgeId": "17/27", "adjWalls": []}, {"isAccessible": true, "edgeId": "18/19", "adjWalls": []}, {"isAccessible": true, "edgeId": "18/27", "adjWalls": []}, {"isAccessible": true, "edgeId": "18/28", "adjWalls": []}, {"isAccessible": true, "edgeId": "18/29", "adjWalls": []}, {"isAccessible": true, "edgeId": "19/29", "adjWalls": []}, {"isAccessible": true, "edgeId": "19/30", "adjWalls": []}, {"isAccessible": true, "edgeId": "20/21", "adjWalls": []}, {"isAccessible": true, "edgeId": "20/31", "adjWalls": []}, {"isAccessible": true, "edgeId": "20/32", "adjWalls": []}, {"isAccessible": true, "edgeId": "21/22", "adjWalls": []}, {"isAccessible": true, "edgeId": "21/32", "adjWalls": []}, {"isAccessible": true, "edgeId": "21/33", "adjWalls": []}, {"isAccessible": true, "edgeId": "21/34", "adjWalls": []}, {"isAccessible": true, "edgeId": "22/34", "adjWalls": []}, {"isAccessible": true, "edgeId": "22/35", "adjWalls": []}, {"isAccessible": true, "edgeId": "23/24", "adjWalls": []}, {"isAccessible": true, "edgeId": "24/25", "adjWalls": []}, {"isAccessible": true, "edgeId": "25/26", "adjWalls": []}, {"isAccessible": true, "edgeId": "26/27", "adjWalls": []}, {"isAccessible": true, "edgeId": "27/28", "adjWalls": []}, {"isAccessible": true, "edgeId": "28/29", "adjWalls": []}, {"isAccessible": true, "edgeId": "29/30", "adjWalls": []}, {"isAccessible": true, "edgeId": "30/31", "adjWalls": []}, {"isAccessible": true, "edgeId": "31/32", "adjWalls": []}, {"isAccessible": true, "edgeId": "32/33", "adjWalls": []}, {"isAccessible": true, "edgeId": "33/34", "adjWalls": []}, {"isAccessible": true, "edgeId": "34/35", "adjWalls": []}, {"edgeId": "1/25", "isAccessible": true, "adjWalls": []}, {"edgeId": "1/26", "isAccessible": true, "adjWalls": []}, {"edgeId": "1/30", "isAccessible": true, "adjWalls": []}, {"edgeId": "1/31", "isAccessible": true, "adjWalls": []}, {"edgeId": "1/35", "isAccessible": true, "adjWalls": []}, {"edgeId": "1/10", "isAccessible": true, "adjWalls": []}, {"edgeId": "1/14", "isAccessible": true, "adjWalls": []}, {"edgeId": "1/4", "isAccessible": true, "adjWalls": []}]]'
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
    
    createParcelations(inputs[0],inputs[1],4,demandProjection,unitTypes)

    
    
if __name__== "__main__":
    main()