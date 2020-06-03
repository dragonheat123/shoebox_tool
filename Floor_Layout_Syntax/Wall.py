
class Wall:
    def __init__(self, vertices=None, materialID=None, wallType=None, thickness=None, wallArea=None, isStructural=None, wallLength=None, lcaDb=None ):

        self.materialID=materialID
        self.wallType=wallType
        self.vertices = vertices # list of two vectors
        self.wallLength = float(wallLength) if wallLength!="" else 0.5 # or calc from vertext positions
        self.wallArea = float(wallArea) if wallArea!="" else 0.5
        self.thickness = float(thickness) if thickness!="" else 0.1 # or taken from LCADB
        self.height = 3 #metres
        #self.isStructural = isStructural # true: strutural support, false: optional infill
        #self.isInfill = isInfill
        self.GWP = self.wallLength*self.height*self.thickness*lcaDb.factor(materialID)

    #TODO: dynamic material and gwp changes -store them as state (Parcelized_layout_graph) rather than here