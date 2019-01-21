"""Provides Entity class which describes an object on the map"""
from math import pi
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
        self.id = int(id)
        if type == 1:
            self.type = "appleBad"
        elif type == 2:
            self.type = "appleGood"
        else:
            self.type = "unknown"

