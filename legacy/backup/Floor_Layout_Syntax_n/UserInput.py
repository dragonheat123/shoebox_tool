from pandas import DataFrame as df
import Floor_Layout_Syntax.Helper_functions as hf
import numpy
import copy

class User_input:

    def __init__(self, numFloors, numDoors, positions, levelRanges, unitTypes = None, positionRanges=None, positionDistribution=None, floorDistribution=None):

        self.numDoors = numDoors
        self.numFloors = numFloors
        self.positions = positions
        self.levelRanges = levelRanges
        self.floorDistribution = floorDistribution #floorDistribution must match size of levelRanges
        self.positionDistribution = positionDistribution
        self.unitTypes = unitTypes

        if positionRanges==None:
            self.positionRanges = []
        else: self.positionRanges = positionRanges
        
        doors = []
        
        for i in range(1, numDoors + 1): doors.append('D' + str(i))
        doorsBldgDf = df(columns=doors)

        for i in range(numFloors):
            row = []
            for j in range(numDoors):
                row.append(0)
            doorsBldgDf.loc[i] = row
        self.doorsBldgDf = doorsBldgDf
        self.doorsBldgDf.index+=1 #set index to start from 1

        # redundant?
        indices = []
        for bin in levelRanges:
            indices.append(str(bin[0])+'-'+ str(bin[1]))

        binnedBldg = df(columns = self.positions, index=indices)
        typeProbBins = df(columns = self.positions, index=indices)
        locProbBins = df(columns=self.positions, index=indices)

        for flBin in (indices):
            row = []
            for j in range(len(self.positions)):
                row.append([0])
            binnedBldg.loc[flBin]=row
            locProbBins.loc[flBin]=row
            typeProbBins.loc[flBin]=row
        self.binnedBldg=binnedBldg
        self.locProbBins=locProbBins
        self.typeProbBins=typeProbBins


    def populateBinnedBldg(self, numPeople):
        for f in range(0, numPeople):
            #floorDistribution must match size of levelRanges
            if self.floorDistribution!= None:
                fl = (numpy.random.choice(self.binnedBldg.index.values.tolist(),1, p=self.floorDistribution))[0]
            else:
                fl = hf.normalChoice(lst=self.binnedBldg.index.values.tolist())

            if self.positionDistribution!=None:
                dr = (numpy.random.choice(self.positions,1, p=self.positionDistribution))[0]
            else:
                dr = hf.normalChoice(lst=self.positions)

            if (self.binnedBldg.loc[fl, dr][0]) == 0:
                del self.binnedBldg.loc[fl, dr][0]

            type = hf.normalChoice(lst=self.unitTypes)
            self.binnedBldg.loc[fl, dr].append(type)


    def genFakeUnitTypePrefs (self, numPeople, binned, RAYformat, savefilePath): # returns a binned DF containing probabilities
        self.populateBinnedBldg(numPeople)
        for floorBin in self.binnedBldg.index.values.tolist():
            for pos in self.positions:
                typeProbabilities = []
                for t in self.unitTypes:
                    doorPrefs = self.binnedBldg.loc[floorBin, pos]
                    typeProbabilities.append(round(doorPrefs.count(t)/len(doorPrefs),3))
                self.typeProbBins.loc[floorBin, pos]=typeProbabilities
                #probability=len(self.binnedBldg.loc[floorBin,pos])/numPeople
                #self.locProbBins.loc[floorBin, pos]=probability
        
        exportPath=savefilePath+'df_DoorProbabilities.csv'
        f= open(exportPath,"w")
        f.write(self.getDoorProbabilities(self.typeProbBins).to_csv(index=False))
        f.close()
        exportPath=savefilePath+'df_typeProbBins.csv'
        f= open(exportPath,"w")
        f.write(self.typeProbBins.to_csv(index=False))
        f.close()
        
#        print(self.getDoorProbabilities(self.typeProbBins))
#        print(self.typeProbBins)

        if binned == False:
            if RAYformat==True:
                return self.toRayFormat(self.getDoorProbabilities(self.typeProbBins), binned=False)
            else:
                return self.getDoorProbabilities(self.typeProbBins)
        else:
            if RAYformat==True:
                return self.toRayFormat(self.typeProbBins, binned=True)
            else:
                return self.typeProbBins


    def genFakeLocationPrefs(self, numPeople, binned=False, RAYformat=False):  # returns a binned DF containing probabilities
        for f in range(0, numPeople):
            if self.floorDistribution!= None:
                fl = (numpy.random.choice(self.binnedBldg.index.values.tolist(),1, p=self.floorDistribution))[0]
            else:
                fl = hf.normalChoice(lst=self.binnedBldg.index.values.tolist())

            if self.positionDistribution!=None:
                dr = (numpy.random.choice(self.positions, 1, p=self.positionDistribution))[0]
            else:
                dr = hf.normalChoice(lst=self.positions)

            if (self.binnedBldg.loc[fl, dr][0]) == 0:
                del self.binnedBldg.loc[fl, dr][0]


            self.binnedBldg.loc[fl, dr].append(hf.normalChoice(lst=self.unitTypes))

        for floorBin in self.binnedBldg.index.values.tolist():

            for pos in self.positions:
                probability = len(self.binnedBldg.loc[floorBin, pos]) / numPeople

                self.locProbBins.loc[floorBin, pos] = probability

        if binned == False:
            if RAYformat == True:
                self.toRayFormat(self.getDoorProbabilities(self.locProbBins), binned=False)

            else:
                return self.getDoorProbabilities(self.locProbBins)

        else:
            if RAYformat==True:
                return self.toRayFormat(self.locProbBins, binned=True)
            else:
                return self.locProbBins



    def getDoorProbabilities (self, binnedProb,):


        # go through all doors
            #check: whih position do I lie in? --> pos
            #check: which floor bin do I lie in? --> floorBin

            # return probability from probBins.loc[floorBin, pos]


        for floor in (self.doorsBldgDf.index.values.tolist()):

            for door in range (1, self.numDoors+1):

                #which position (floor, position) do I lie in?
                doorBin = 0
                floorBin = 0

                for flBounds in self.levelRanges:

                    #print ('flBounds ', flBounds)

                    if (floor >= flBounds[0]) and (floor <= flBounds[1]):floorBin=str(flBounds[0])+'-'+ str(flBounds[1])
                    #break

                for posBounds in self.positionRanges:

                    if (door >= posBounds[0]) and (door <= posBounds[1]):

                        doorBin= self.positions[self.positionRanges.index(posBounds)]
                    #break

                self.doorsBldgDf.loc[floor, list(self.doorsBldgDf)[door-1]]=binnedProb.loc[floorBin,doorBin]


        return self.doorsBldgDf

    def calcProbFromPref(self,unitPrefsList):
        demand={}
        total=0
        p=[]
        for unitTypeIndex in unitPrefsList:
            if unitTypeIndex not in demand:
                demand[unitTypeIndex]=1
            else:
                demand[unitTypeIndex]+=1
            total+=1
        #sanity check- probabilities must add up to 1
        diff=0  
        nonEmptyIndex=0
        for i in range(len(self.unitTypes)):
            key=i+1 #key of dictionary- in this case the unit type
            if key not in demand:
                p.append(0)
            else:
                nonEmptyIndex=i
                q=demand[key]/total
                diff+=q
                p.append(q)
        diff-=1
        if diff!=0:
            p[nonEmptyIndex]-=diff
        return p

    def calcBinnedProb(self,prefBinDf):
        probDf=copy.copy(prefBinDf)
        floorRanges=probDf.index.values.tolist()
        for fR in floorRanges:
            for generalLocation in probDf.keys():
                unitPrefsList=probDf.loc[fR,generalLocation]
                probDf.loc[fR,generalLocation]=self.calcProbFromPref(unitPrefsList)
        return probDf

    def calcOverallBinnedProb(self,prefBinDf):
        probDf=copy.copy(prefBinDf)
        overallProb={}
        floorRanges=probDf.index.values.tolist()
        for fR in floorRanges:
            dist=[0,0,0,0,0]
            for generalLocation in probDf.keys():
                unitPrefsList=probDf.loc[fR,generalLocation]
                probDf.loc[fR,generalLocation]=self.calcProbFromPref(unitPrefsList)
                dist=numpy.add(dist,probDf.loc[fR,generalLocation])
            overallProb[fR]=numpy.divide(dist,3)
        return probDf, overallProb
    
    def toRayFormat(self, prefDf, binned=False):
        prefDict = {}
        if binned==False:
            for floorIndex in (prefDf.index.values.tolist()):
                for doorIndex in range (1, self.numDoors+1):
                    prefDict[str(floorIndex)+'F/D'+str(doorIndex)]=prefDf.loc[floorIndex, list(self.doorsBldgDf)[doorIndex-1]]
            return prefDict
        else:
            for floorBin in (prefDf.index.values.tolist()):
                for doorBin in (list(prefDf)):
                    prefDict[str(floorBin) + 'F/D' + str(doorBin)] = prefDf.loc[floorBin, doorBin]
            return prefDict