"""Provides Entity class which describes an object on the map"""
from math import pi
from Resources import ResObjects
class Robot:
    """Holds data of an robot in the field"""
    def __init__(self,id,position,direction):    
        self.position = list(map(int,position))
        self.direction = float(direction * 180 / pi)
        self.id = int(id)

class Apple:
    """Holds data of an apple in the field"""
    def __init__(self,type,id,position,direction):    
        self.position = list(map(int,position))
        self.direction = float(direction * 180 / pi)
        self.id = int(id)
        if type == ResObjects.APPLE_GOOD:
            self.type = "appleGood"
        elif type == ResObjects.APPLE_BAD:
            self.type = "appleBad"
        else:
            self.type = "unknown"

