import Floor_Layout_Syntax.Constants as Constants
import Floor_Layout_Syntax.GeneticAlgorithm as GA
import numpy as np
from datetime import datetime
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import seaborn.apionly as sns
# from matplotlib.colors import LinearSegmentedColormap
from pandas import DataFrame as df
import jsonpickle

class Building:    
    def __init__(self,layoutGraph,floorCount, floorHeight, floorThickness):
        ### argument format ###
        #parcelizedBuilding is a dictionary:
            #keys -  corresponding floor level as string(int)
            #values - Parcelized_layout_graph objects
        self.floorCount=floorCount
        self.floorHeight=floorHeight
        self.floorThickness=floorThickness
        
        self.parcelizedBuilding={}
        self.layoutPopulation={}
        self.layoutGraph=layoutGraph
        self.demographicModel={}
        
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
            floorCount = floorBound[1]-floorBound[0]+1
            #--GA component to get try get best floor combinations
            population = GA.Population(self.demographicModel[fR], floorCount, Constants.GA_MUTATION_RATE, self.layoutGraph.unitCombinations, Constants.GA_POPCOUNT)
            for i in range(Constants.GA_GENERATIONS):
                population.naturalSelection()
                population.generate()
                population.calcFitness()
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
    
    def getStructuralGwp(self, forAllFloors=True):
        gwp = self.layoutGraph.getStructuralGwp()
        if forAllFloors==True:
            gwp*=len(self.parcelizedBuilding)
        return gwp
    
    def getInfillGWP(self,otherBuilding):
        return self.compareBuildingWallChanges(otherBuilding)['added']['cost']
    
    def compareBuildingWallChanges(self,other,wallType='infill'):
        res={
                'added':{'qty':0,'cost':0},
                'removed':{'qty':0,'cost':0},
                'saved':{'qty':0,'cost':0}
                }
        for floor in self.parcelizedBuilding.keys():
            d=self.compareFloorWallChanges(other,floor,wallType)
            for key in res.keys():
                res[key]['qty']+=d[key]['qty']
                res[key]['cost']+=d[key]['cost']
        return res
    
    def compareFloorWallChanges(self,other,floor,wallType='infill'):
        self.parcelizedBuilding[floor].turnOnUnitSurroundingWalls(wallType,self.layoutGraph)
        other.parcelizedBuilding[floor].turnOnUnitSurroundingWalls(wallType,self.layoutGraph)
        return self.parcelizedBuilding[floor].compareGwpDifference(other.parcelizedBuilding[floor],wallType,self.layoutGraph)
        
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
        
    def drawFloorGraph(self,floorIndex):
        print("--floor "+str(floorIndex)+" parcelation--")
        parcelized=self.parcelizedBuilding[floorIndex]
        self.layoutGraph.drawTraversedPaths(parcelized)
    
    def drawAllFloorGraphs(self):
        for floorIndex in sorted(self.parcelizedBuilding.keys()):
            print("--floor "+str(floorIndex)+" parcelation--")
            parcelized=self.parcelizedBuilding[floorIndex]
            self.layoutGraph.drawTraversedPaths(parcelized)
            
    def drawElevation (self, displayType='ELEVATION', saveFig=False):
        elevationDf=self.getElevationTypeSequence(displayType)
        dataReversed = elevationDf.reindex(index=elevationDf.index[::-1])
        
        sns.set(font_scale=0.8)        
        colors=[d['color'] for d in Constants.UNIT_TYPES]
        colors.insert(0,[242/256, 242/256, 242/256])
        cmap = LinearSegmentedColormap.from_list('NextGen', colors, len(colors))
        ax = sns.heatmap(dataReversed, cmap=cmap, linewidths=0, linecolor='white')
        
        # Manually specify colorbar labelling after it's been generated
        colorbar = ax.collections[0].colorbar
        ticks = []
        for i in range(0, 6):
            step = (colorbar.vmax - colorbar.vmin)/ 6
            ticks.append((step * i) + colorbar.vmin + step/ 2)
        
        colorbar.set_ticks(ticks)
        ticklabels=["Type "+str(d['unitTypeIndex']) for d in Constants.UNIT_TYPES]
        ticklabels.insert(0,"None")
        colorbar.set_ticklabels(ticklabels)
        colorbar.ax.tick_params(size=0)
        # X - Y axis labels
        ax.set_ylabel('FLOOR')
        ax.set_xlabel('WING POSITION')
        # Only y-axis labels need their rotation set, x-axis labels already have a rotation of 0
        _, labels = plt.yticks()
        plt.setp(labels, rotation=0)

        for floorIndex in sorted(self.parcelizedBuilding.keys()):
            rFloor=len(self.parcelizedBuilding)+1-floorIndex
            if displayType=='DOORS':
                parcelisedLG = self.parcelizedBuilding[rFloor].unitSequence #count downwards due to inversin of origin on heatmap - matpotlib issue
            elif displayType=='ELEVATION':
                parcelisedLG = self.parcelizedBuilding[rFloor].elevationSequence

            index=0
            while index < len(parcelisedLG):
                currentDoor = parcelisedLG[index]
                if currentDoor < 0:
                    numOccupiedDoors = 1
                    rect = patches.Rectangle((index, floorIndex-1), width=1, height=1, linewidth=4,
                                             edgecolor='white', facecolor='none')
                    ax.add_patch(rect)

                else:
                    numOccupiedDoors = parcelisedLG.count(currentDoor)
                    rect = patches.Rectangle((index, floorIndex-1), width=numOccupiedDoors, height=1, linewidth=4,
                                             edgecolor='white', facecolor='none')
                    ax.add_patch(rect)
                index+=numOccupiedDoors
        plt.show()

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