class Constraint:

    def __init__(self, roomType=1,prefWeight=0, prefDoors=[], roomConstraints={}):
        #TODO: Use a lookup table based on room type if all room constraints are consistent
        self.roomType=roomType
        self.prefDoors=prefDoors
        self.prefWeight=prefWeight
        self.roomConstraints=roomConstraints
    def __str__(self):
        return str(self.roomType)+' room unit type'