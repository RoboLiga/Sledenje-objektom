"""Provides GameLiveData class, which is communicated to robots"""
class GameLiveData:
    """Holds data to be sent to robots"""
    def __init__(self):
        self.gameOn = False
        self.timeLeft = 0
        self.team1 = {
                "id" : 0,
                "name" : "team1",
                "score" : 0        
            }
        self.team2 = {
                "id" : 1,
                "name" : "team2",
                "score" : 0        
            }
        
        self.field = {
                 "topLeft" : [0,0],
                 "topRight" : [0,0],
                 "bottomLeft": [0,0],
                 "bottomRight": [0,0],
                 "baskets": {  "team1" : {
                               "topLeft" : [0,0],
                               "topRight" : [0,0],
                               "bottomLeft": [0,0],
                               "bottomRight": [0,0]
                              },
                    "team2" : {
                               "topLeft" : [0,0],
                               "topRight" : [0,0],
                               "bottomLeft": [0,0],
                               "bottomRight": [0,0]
                              }
                  }
                }
        self.apples = []
        self.robots = []
    #def toJSON(self):
    #   return json.dumps(self, default=lambda o: o.__dict__, 
    #        sort_keys=False, indent=4) 


