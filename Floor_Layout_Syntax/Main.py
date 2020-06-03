import Floor_Layout_Syntax.Layout_graph as layout
import Floor_Layout_Syntax.UserInput as userInp
import Floor_Layout_Syntax.Building as bldg
import Floor_Layout_Syntax.Constraint as con
import networkx as nx
from pandas import DataFrame as df
import matplotlib.pyplot as plt


######## SPECIFY EDGE AND NODE JSON FILEPATHS ########

rootPath = '/Users/zack_sutd/Dropbox (Personal)/SUTD/PostDoc/Space Syntax/next-gen-space-syntax/'

edges_jsonfilepath =rootPath+'testcases/2_edges.txt'
nodes_jsonfilepath =rootPath+'testcases/2_nodes.txt'

pos_path = rootPath+"floorplan_vectors/node position_vectors_rot_offsets.txt"
lengths_path = rootPath+"floorplan_vectors/position_vector_lengths.txt"

#savefilePath=rootPath+'saved_results/'
savefilePath = rootPath+'saved_results/2/'

#edges_jsonfilepath ='/Users/zack_sutd/Dropbox (Personal)/SUTD/PostDoc/Space Syntax/next-gen-space-syntax/testcases/2_edges.txt'
#nodes_jsonfilepath ='/Users/zack_sutd/Dropbox (Personal)/SUTD/PostDoc/Space Syntax/next-gen-space-syntax/testcases/2_nodes.txt'

######## LOAD NEW LAYOUT_GRAPH ########

Layoutjson = layout.Layout_graph()
Layoutjson.importJSON(nodes_jsonfilepath, edges_jsonfilepath)

######## DRAW GRAPH ########

#Layoutjson.draw()
#pos_path = "/Users/zack_sutd/NextGenHighRise Dropbox/2018(09).NGH_NextGeneration(Residential)Highrise/05_Production/_Zack/node position_vectors.txt"
#lengths_path = "/Users/zack_sutd/NextGenHighRise Dropbox/2018(09).NGH_NextGeneration(Residential)Highrise/05_Production/_Zack/position_vector_lengths.txt"
#fig, ax = plt.subplots(figsize=(2*12.83, 2*3.94))
#fig.tight_layout()

Layoutjson.loadDrawVectors(pos_path, lengths_path)
Layoutjson.drawTraversedPaths(traversedNodesIds=[], traversedEdgesIds=[])
#Layoutjson.drawFromFile(pos_path, lengths_path, traversedNodesIds=[1, 3, 4, 19, 18], traversedEdgesIds=['1/4', '4/3', '3/19', '19/18'])
#ax.spines['top'].set_visible(False)
#ax.spines['right'].set_visible(False)
#ax.spines['left'].set_visible(False)
#lt.tight_layout( w_pad=2, h_pad=0)
######## GENERATE FAKE USER UNIT-TYPE AND LOCATION PREFERENCES ########
unitTypes = [1, 2, 3, 4, 5, 6]
hdbDistribution = [0.133, 0.275, 0.211, 0.124, 0.147, 0.11] # from HDB paper
posDistribution = [0.1, 0.2, 0.7]
floorLevels = [[1,5],[6,10], [11,15], [16,20], [21,25], [26,30]]
u = userInp.User_input(numFloors=30, numDoors=6, positions=["left", "middle" ,"right"], unitTypes=unitTypes, levelRanges=floorLevels, positionRanges=[[1, 2],[3,4] ,[5, 6]], floorDistribution=hdbDistribution, positionDistribution=None) # from HDB paper

#u = userInp.User_input(numFloors=10, numDoors=6, positions=["left", "middle" ,"right"], levelRanges=[[1, 5], [6, 10]], positionRanges=[[1, 2],[3,4] ,[5, 6]])
data = u.genFakeLocationPrefs(numPeople=100, binned=False, RAYformat=False)
#u.genFakeUnitTypePrefs(numPeople=100, binned=False, RAYformat=False)
#print (u.genFakeUnitTypePrefs(numPeople=100, binned=True, RAYformat=False))
print ('binned bldg ' ,u.binnedBldg)


path = "/Users/zack_sutd/NextGenHighRise Dropbox/2018(09).NGH_NextGeneration(Residential)Highrise/05_Production/_Zack/node position_vectors.txt"

######## VISUALISE ELEVATION MATRIX OF UNIT PARCELATIONS ########

building = bldg.Building(Layoutjson)
building.loadBuilding(savefilePath)
building.fillEmptyClusters()
seq,dType = building.getElevationPermTypeSequence()
print ('mapped type sequence')
building.drawElevation(seq,dType)

#seq.columns = data.columns.tolist()

#permDf = df(data=fakeperms, columns=data.columns.tolist())
#rev_permDf = permDf.reindex(index=permDf.index[::-1])

#building.drawElevation(permDf)

