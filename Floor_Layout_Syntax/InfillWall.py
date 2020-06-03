class InfillWall:

    def __init__(self, vertices=None, material=None, thickness=None, wallArea=None, isStructural=None, isInfill=False, wallLength=None ):


        self.material=material
        self.vertices = vertices # list of two vectors
        self.wallLength = wallLength # or calc from vertext positions
        self.wallArea = wallArea
        self.thickness = thickness
        self.isOn=True

