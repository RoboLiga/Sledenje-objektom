"""Provides GameLiveData class, which is communicated to robots"""
#import json
class GameLiveData:
    """Holds data to be sent to robots"""
    def __init__(self):
        self.gameOn = False
        self.score = {
                 "Team1": 0,
                 "Team2": 0
                }
        self.timeLeft = 0
        self.field = {
                 "TopLeft" : [0,0],
                 "TopRight" : [0,0],
                 "BottomLeft": [0,0],
                 "BottomRight": [0,0]
                }
        self.baskets = { "Team1" : {
                               "TopLeft" : [0,0],
                               "TopRight" : [0,0],
                               "BottomLeft": [0,0],
                               "BottomRight": [0,0]
                              },
                    "Team2" : {
                               "TopLeft" : [0,0],
                               "TopRight" : [0,0],
                               "BottomLeft": [0,0],
                               "BottomRight": [0,0]
                              }
                  }
        self.apples = []
        self.robots = []
    #def toJSON(self):
    #   return json.dumps(self, default=lambda o: o.__dict__, 
    #        sort_keys=False, indent=4) 


