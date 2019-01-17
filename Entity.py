"""Provides Entity class which describes an object on the map"""
from math import pi
class Entity:
    """Holds data of an object in the field"""
    def __init__(self,type,id,position,direction):    
        if  type == 0:
            self.type = "robot"
        elif type == 1:
            self.type = "appleBad"
        elif type == 2:
            self.type = "appleGood"
        else:
            self.type = "unknown"
        self.X = int(list(position)[0])
        self.Y = int(list(position)[1])
        self.direction = float(direction * 180 / pi)
        self.id = int(id)

