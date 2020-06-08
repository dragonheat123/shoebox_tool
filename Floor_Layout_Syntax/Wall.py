import math

class Wall:
    def __init__(self, vertices=None, matId=[], thickness=None, composition=[]):
        self.matId = matId
        self.vertices = vertices # list of two vectors
        self.thickness = float(thickness) if thickness!="" else 0.1 # or taken from LCADB
        self.composition = composition
        self.length = None
        #self.height = 3 #metres
        #self.isStructural = isStructural # true: strutural support, false: optional infill
        #self.isInfill = isInfill
        #self.GWP = self.wallLength*self.height*self.thickness*lcaDb.factor(matId)
    
    def getLength(self):
        if self.length == None:
            p0 = self.vertices[0]
            p1 = self.vertices[1]
            self.length = math.sqrt(math.pow(float(p0[0])-float(p1[0]),2)+math.pow(float(p0[1])-float(p1[1]),2))
        return self.length
    
    def getGwp(self,height,lcaDb,wallTypes=['infill','structural']):
        gwp = 0
        if 'structural' in wallTypes:
            gwp += self.composition[0]*self.getLength()*height*self.thickness*lcaDb.factor(self.matId[0])
        if 'infill' in wallTypes:
            gwp += self.composition[1]*self.getLength()*height*self.thickness*lcaDb.factor(self.matId[1])
        return gwp