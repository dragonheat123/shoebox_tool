import Floor_Layout_Syntax.Constants as Constants
#import Floor_Layout_Syntax.Layout_graph_v2 as Layout
#import Floor_Layout_Syntax.UserInput as UserInput
import Floor_Layout_Syntax.GeneticAlgorithm as GA
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
from pandas import DataFrame as df
import jsonpickle

class Building:
    def __init__(self,layoutGraph):
        ### argument format ###
        #parcelizedBuilding is a dictionary:
            #keys -  corresponding floor level as string(int)
            #values - Parcelized_layout_graph objects
        self.parcelizedBuilding={}
        self.layoutPopulation={}
        self.layoutGraph=layoutGraph
        self.demographicModel={}
        self.prob_reconfig=None
        
        #===============================================PHASE 1==============================================
        #--evaluative phase to find out all possible unit combinations for a layout
        #====================================================================================================
        self.layoutGraph.generateParcelationDb(Constants.EMPTY_SPACE_THRESHOLD)
        
    def setDefaultState(self):
        for f in range(1,31):
            self.parcelizedBuilding[f] = self.layoutGraph.getDefaultLayout()
            
    def parcelate(self, demographicModel):
        start = datetime.now()
        
        #===============================================PHASE 2==============================================
        #--Selection and layout generation component; GA selects unit combination and traveral allocates units
        #====================================================================================================
        self.demographicModel=demographicModel
        
        #--foreach floor range, select unitCombination in floors then generate layout in each
        for fR in self.demographicModel.keys():
            floorBound = list(map(int, fR.split('-',1)))  #[0]->lower floor bound; [1]->upper floor bound
            floorCount = floorBound[1]-floorBound[0]+1  # TODO: static floorcount definition
            #--GA component to get try get best floor combinations
            population = GA.Population(self.demographicModel[fR], floorCount, Constants.GA_MUTATION_RATE, self.layoutGraph.unitCombinations, Constants.GA_POPCOUNT, len(self.layoutGraph.nodes))
            for i in range(Constants.GA_GENERATIONS):
                population.calcFitness()
                population.naturalSelection()
                population.generate()
                population.evaluate()
                
            #drawOverallDistributionChart(overallProb[fR],"Distribution for floors "+fR)
            self.layoutPopulation[fR] = population
            for i in range(len(population.bestResults[0].genes)):
                self.parcelizedBuilding[floorBound[0]+i] = self.layoutGraph.getRandomParcelation(population.bestResults[0].genes[i])
#            --for all possible results
#            for dna in population.bestResults:
#                print("--DNA "+str(dna.genes)+" Results--")
#                for combinationIndex in dna.genes:
#                    self.layoutGraph.getRandomParcelation(combinationIndex)
        print('Start Time: ')
        print(start)
        print('End Time: ')
        print(datetime.now())
    
    def getBuildingLayoutResults(self):
        result = dict()
        result['layouts'] = list()
        idx = 0
        for floorIndex in sorted(self.parcelizedBuilding.keys()):
            #print("--floor "+str(floorIndex)+" parcelation--")
            layouts = dict()
            layouts['units'] = self.parcelizedBuilding[floorIndex].exportUnitData()
            result['layouts'].append(layouts)
            #print(json.dumps(result['layouts'][idx]))
            idx += 1
        return result
    
    def getTotalGwp(self,floor=None,wallType='infill'):
        gwp=0
        #TOOO: a more elegant solution
        if floor==None:
            gwp+=self.getStructuralGwp(True)
            for f in self.parcelizedBuilding.values():
                f.turnOnUnitSurroundingWalls(wallType,self.layoutGraph)
                gwp+=f.getTotalGwpOfWallType(wallType,self.layoutGraph)
        else:
            self.parcelizedBuilding[floor].turnOnUnitSurroundingWalls(wallType,self.layoutGraph)
            gwp+=self.getStructuralGwp(False)
            gwp+=self.parcelizedBuilding[floor].getTotalGwpOfWallType(wallType)
        return gwp
    
    def getStructuralGwp(self, lcaDb, materialId=None,wallThickness=None,forAllFloors=True):
        gwp = self.layoutGraph.getStructuralGwp(lcaDb,materialId,wallThickness)
        if forAllFloors==True:
            gwp*=len(self.parcelizedBuilding)
        return gwp
    
    def getInfillGWP(self,otherBuilding):
        return self.compareBuildingWallChanges(otherBuilding)['added']['cost']
    
    def compareBuildingWallChanges(self,other,lcaDb,materialId=None,wallThickness=None,wallType='infill'):
        res={
                'added':{'qty':0,'cost':0},
                'removed':{'qty':0,'cost':0},
                'saved':{'qty':0,'cost':0}
                }
        for floor in self.parcelizedBuilding.keys():
            d=self.compareFloorWallChanges(other,floor,lcaDb,materialId,wallThickness,wallType)
            for key in res.keys():
                res[key]['qty']+=d[key]['qty']
                res[key]['cost']+=d[key]['cost']
        return res
    
    def compareFloorWallChanges(self,other,floor,lcaDb,materialId=None,wallThickness=None,wallType='infill'):
        self.parcelizedBuilding[floor].turnOnUnitSurroundingWalls(wallType,self.layoutGraph)
        other.parcelizedBuilding[floor].turnOnUnitSurroundingWalls(wallType,self.layoutGraph)
        return self.parcelizedBuilding[floor].compareGwpDifference(other.parcelizedBuilding[floor],wallType,self.layoutGraph,lcaDb,materialId,wallThickness)
        
    def save(self,savefilePath):
        f= open(savefilePath+'building.txt',"w")
        f.write(jsonpickle.encode(self))
        f.close()

    def updateBuildingFloorLayout (self, floorLevel, ParcelizedLayoutGraph):
        self.parcelizedBuilding[floorLevel]=ParcelizedLayoutGraph
    
    def reindex(self):
        self.parcelizedBuilding=reindexToIntKeyDict(self.parcelizedBuilding)
    
    #for future reference only 
    #-deprecated- new algorithm filters this 
    def fillEmptyClusters(self):
        for floorIndex in range (0, len(self.parcelizedBuilding.keys())):
            parcelized=self.parcelizedBuilding[len(self.parcelizedBuilding.keys()-floorIndex)]
#            print('old seq:',parcelized.unitSequence)
            self.layoutGraph.fillEmptyNodes(parcelized)
#            print('new seq:',self.parcelizedBuilding[str(len(self.parcelizedBuilding.keys())-floorIndex)].unitSequence)
    
    def getElevationTypeSequence(self,displayType):
        types = []
        for floorIndex in sorted(self.parcelizedBuilding.keys()):
#            print ('Floor ', floorIndex)
            parcelisedLG = self.parcelizedBuilding[floorIndex]
            if displayType=="DOORS":
                floorTypeSeq = parcelisedLG.doorSequence
            else:
                floorTypeSeq = parcelisedLG.elevationSequence
            types.append(floorTypeSeq)
#            print (floorTypeSeq)
            dataF = df(data=types)
            dataF.index+=1
        return dataF
    
    def drawDemographicModelChart(self):
        for fR,demographicModel in self.demographicModel.items():
            drawOverallDistributionChart(demographicModel,"Distribution for floors "+fR)
    
    def drawComparisonChart(self):
        for fR,population in self.layoutPopulation.items():
            population.printBestResults(self.layoutGraph.unitCombinations,self.demographicModel[fR],drawComparisonChart)
    
    def getBestFitness(self):
        for fR,population in self.layoutPopulation.items():
            return population.getBestFitness()
    
    def drawFloorGraph(self,floorIndex):
        print("--floor "+str(floorIndex)+" parcelation--")
        parcelized=self.parcelizedBuilding[floorIndex]
        for u in parcelized.units:
            print("Unit type "+str(u.getUnitTypeIndex())+":",u.connectedNodeIds)
#        self.layoutGraph.drawTraversedPaths(parcelized)
    
    def drawAllFloorGraphs(self):
        for floorIndex in sorted(self.parcelizedBuilding.keys()):
            print("--floor "+str(floorIndex)+" parcelation--")
            parcelized=self.parcelizedBuilding[floorIndex]
            self.layoutGraph.drawTraversedPaths(parcelized)

#==================================DRAW & MISC. FUNCTIONS==================================
def reindexToIntKeyDict(d):
    correctedDict = {}
    for key, value in d.items():
        correctedDict[int(key)] = value
    return correctedDict

def loadBuilding(savefilePath):
    f= open(savefilePath+'building.txt',"r")
    bldg=jsonpickle.decode(f.read())
    f.close()
    bldg.reindex()
    return bldg
    
def drawDataFrameChart(floorRanges,prefDf,probDf):
    width=0.8
    unitTypeLegend=[]
    for u in Constants.UNIT_TYPES:
        unitTypeLegend.append("T"+str(u['unitTypeIndex']))
    color=[d['color'] for d in Constants.UNIT_TYPES]
    fig, axs = plt.subplots(ncols=3,nrows=6,subplot_kw={'xticks': [],'yticks': []})
    
    for row in reversed(range(len(floorRanges))):
        for col in range(len(Constants.DOOR_POSITIONS)):
            demandCount=[0]*5
            for n in prefDf.loc[floorRanges[row],col]:
                demandCount[n-1]+=1
            ax=axs[len(floorRanges)-1-row,col]  #plotting in reverse to reflect bottom up structure of a building
            ax.set_ylim([0,1])
            unitProbability=probDf.loc[floorRanges[row],col]
            ax.bar(unitTypeLegend,unitProbability,width,color=color)
            if row==len(floorRanges)-1 and col<3:
                ax.set_title(Constants.DOOR_POSITIONS[col]['pos'])
            if col==0:
                ax.set_ylabel(floorRanges[row])
    fig.tight_layout()
    plt.show()
    
def drawOverallDistributionChart(fRDist, title):
    width=0.8
    unitTypeLegend=[]
    for u in Constants.UNIT_TYPES:
        unitTypeLegend.append("T"+str(u['unitTypeIndex']))
    color=[d['color'] for d in Constants.UNIT_TYPES]
    fig, axs = plt.subplots(subplot_kw={'xticks': [],'yticks': []})
    
    axs.set_ylim([0,1])
    axs.bar(unitTypeLegend,fRDist,width,color=color)
    axs.set_title(title)
    axs.set_ylabel("Unit Types")
    fig.tight_layout()
    plt.show()
    
def drawComparisonChart(oriDist, newDist, title):
    width=0.35
    unitTypeLegend=[]
    for u in Constants.UNIT_TYPES:
        unitTypeLegend.append("T"+str(u['unitTypeIndex']))
    
    ind = np.arange(len(Constants.UNIT_TYPES))
    fig, axs = plt.subplots()
    axs.set_ylim([0,1])
    axs.bar(ind,oriDist,width,label="Demographic Demand")
    axs.bar(ind+width,newDist,width,label="Result Parcelation")
    
    axs.set_title(title)
    axs.set_xticks(ind + width / 2)
    axs.set_xticklabels(unitTypeLegend)
    axs.legend()
    plt.show()