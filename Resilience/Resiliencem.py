from Floor_Layout_Syntax import Building_v2
import Floor_Layout_Syntax.GeneticAlgorithm as GA
import os
from pandas import DataFrame as df
from LCA import LCADB
import numpy
import matplotlib.pyplot as plt

class Resilience:
    def __init__(self,rootBuildingDir, lcaFilepath):

        self.parcelisedBuildings=[]
        #files=['building1.txt', 'building2.txt', 'building3.txt', 'building4.txt']
        for dirs, subdirs, files in os.walk(rootBuildingDir):
            for subdir in subdirs:
                filepath=os.path.join(dirs,subdir)
                self.parcelisedBuildings.append(Building_v2.loadBuilding(filepath+'/'))
        self.lcaDb = LCADB.LCADB(lcaFilepath)

    def assignNewMaterial(self, building, strucMatID, infillMatID):
        for edge in building.layoutGraph.edges.values():
            for k in edge.adjWalls.keys():
                for w in edge.adjWalls[k]:
                    # print ('GWP before ', w.GWP)
                    if k == 'structural':
                        w.materialID=strucMatID
                        w.GWP = w.wallLength * w.height * w.thickness * self.lcaDb.factor(strucMatID)
                    elif k== 'infill':
                        w.materialID=infillMatID
                        w.GWP = w.wallLength * w.height * w.thickness * self.lcaDb.factor(infillMatID)
                    # print('GWP after ', w.GWP)


    def getKlDiv(self, bldg):
        demand = bldg.demographicModel['1-30']
        # supply = bldg.layoutPopulation['1-30'].bestResults[0].v
        # supply = [0.019215,0.019215,0.26354, 0.39138, 0.29929] #HDB distribution
        supplyDefault = numpy.array([0.33, 0.67, 0, 0, 0]) #hard coded based on case study plan - all partition walls turned on
        return GA.KL(supplyDefault, demand)

    def accumFlexGWP(self, strucMatID, infillMatID, decades):
        #decades should be a list of decade strings
        GWPlist=[]
        sumFlexGWP=0
        #for decade in range (0, len(self.parcelisedBuildings)):
        for decade, parcelisedBldg in enumerate(self.parcelisedBuildings):
            self.assignNewMaterial(parcelisedBldg, strucMatID, infillMatID)
            if decade==0:
                # strucGWP=parelisedBldg.getStructuralGwp(forAllFloors=True)
                # infillGWP=parelisedBldg.getInfillGWP(self.parcelisedBuildings[decade-1])
                # sumFlexGWP+=strucGWP+infillGWP
                sumFlexGWP+=parcelisedBldg.getTotalGwp(floor=None,wallType='infill')
                GWPlist.append(sumFlexGWP)
            else:
                infillGWP=parcelisedBldg.getInfillGwp(self.parcelisedBuildings[decade-1])
                print ('infillGWP ', infillGWP)
                sumFlexGWP+=infillGWP
                GWPlist.append(sumFlexGWP)

        return GWPlist, sumFlexGWP

    def accumFixedGWP (self, decades):
        GWPlist=[]
        sumFixedGWP=0
        fixedFilepath = '/Users/zack_sutd/Dropbox (Personal)/SUTD/PostDoc/Space Syntax/next-gen-space-syntax/saved_results/default/'
        fixedBuilding = Building_v2.loadBuilding(fixedFilepath)
        print (fixedBuilding.demographicModel)
        #set all structural and infill walls to concrete
        self.assignNewMaterial(fixedBuilding, strucMatID='CP042', infillMatID='CP042') # we assume concrete masonry - perhaps this can be made more customisable
        for decade in range (0, len(decades)):
            #TODO: this loop should take into account if fixed floor plan accomodates new demographics
            print(self.getKlDiv(self.parcelisedBuildings[decade]))
            if (self.getKlDiv(self.parcelisedBuildings[decade])) > 1: # 1 needs to change
                sumFixedGWP+=fixedBuilding.getTotalGwp()
                GWPlist.append(sumFixedGWP)
        return GWPlist, sumFixedGWP



    def eval(self, constructionSystems, decades):

        #constructionSystems need to specified as a list of [strucMatID,infillMatID], [strucMatID,infillMatID], ...
        #decades need to be a list of strings eg. [2020-2040], [2040-2060], ...

        GWPdict = {}
        GWPdict['non-flexible']=self.accumFixedGWP(decades)[0]
        for system in constructionSystems:
            GWPdict['StructMatID: '+str(system[0])+' / '+'InfillMatID: '+str(system[1])]=self.accumFlexGWP(strucMatID=system[0], infillMatID=system[1], decades=decades)[0]

        results = df(GWPdict, index=decades)
        print (results)
        # subtract the total GWP for a flexible building from the GWP of a fixed building
        # GWPsaved=self.accumFixedGWP(total=True,decades=decades)
        #
        #         -(self.accumFlexGWP(total=True))
        results.plot.bar(rot=0)
        plt.show()

        return results.transpose()


    def resultsMatrix(self):
        return

    def plot (self):
        return

"""
    
    def GWP_saved (self, demographicDistributions, jsonDirectory ): ## this should go in Resilience class that loads buildings (for now)

        #load building

        #demographicDistributions format: [[0.1, 0.4, 0.5], [0.1, 0.4, 0.5], ...]
        #savedParcelations format: a series of saved json files
        #here we assume loaded LayoutGraph for each decade, are preloaded with .isReused flags
        #TODO: how to factor material variations
        accumulatedGWP=0
        for decade in demographicDistributions:
            buildingGWP=self.GWP()

        #Given a pareclated building graph syntax:
            #for each time span
            # {
                #read saved parcelations
                # OPVs = []
                # for each parcelation
                # {
                    #GWPreconfig = graph.calcGWP() --> should return total GWP for the entire parcelised building
                    #Option Value = GWPreconfig - GWPrecons
                    #OPVs.append(Option Value)

"""