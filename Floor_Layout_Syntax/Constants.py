#TODO: Load layout constants from layout file
#--Phase 1 constants
EMPTY_SPACE_THRESHOLD = 3 #ignore unit combinations if empty spaces exceed value specified
#--Phase 2 Genetic algorithm constants
GA_MUTATION_RATE = 0.1
GA_POPCOUNT = 1000
GA_GENERATIONS = 100

#--UNIT TYPE CONSTANTS
UNIT_TYPES=[{
    "unitTypeIndex":0,
    "color":(0.031, 0.612, 0.533),
    "roomCount":4,
    "normal":2,
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

#--BUILDING AND LAYOUT CONSTANTS
FLOOR_COUNT=30
FLOORLEVELRANGE = [[1,5],[6,10],[11,15],[16,20],[21,25],[26,30]]
DOOR_POSITIONS=[
    {
     'pos':'left',
     'edges':['1/14','1/15']
     },
    {
     'pos':'middle',
     'edges':['1/9','1/10']
     },
    {
     'pos':'right',
     'edges':['1/4','1/5']
     }]
DOOR_COUNT=0
DOOR_EDGE_INDEX=[] #for current dataframe initialization; to remove in future
for i in range(len(DOOR_POSITIONS)):
    dCountInPos=len(DOOR_POSITIONS[i]['edges'])
    DOOR_EDGE_INDEX.append(list(range(0,dCountInPos,1)))
    DOOR_COUNT+=dCountInPos

#--DISTRIBUTION CONSTANTS
HDB_DISTRIBUTION = [0.133, 0.275, 0.211, 0.194, 0.187]
#HDB_DISTRIBUTION = [0.133, 0.275, 0.211, 0.124, 0.147, 0.11] # from HDB paper
POS_DISTRIBUTION = [0.1, 0.2, 0.7]


#numFloors=30, numDoors=6, positions=[0,1,2], unitTypes=[0,1,2,3,4], levelRanges=Constants.FLOORLEVELRANGE, positionRanges=[[1, 2],[3,4] ,[5, 6]], floorDistribution=Constants.HDB_DISTRIBUTION, positionDistribution=None) # from HDB paper
