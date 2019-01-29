"""Provides Score class which handles score of the two competing teams"""
from Resources import ResObjects
class Score:
    """Holds the score for each team"""
    def __init__(self):
        self.team1Apples = []
        self.team2Apples = []
        self.team1bias = 0
        self.team2bias = 0

    def getScore(self, team, gameData):
        ts = 0
        if team == 1:
            for a in self.team1Apples:
                if a in ResObjects.ApplesGoodIds:
                    ts = ts + gameData["goodApple"]
                if a in ResObjects.ApplesBadIds:
                    ts = ts + gameData["badApple"]
            ts = ts + self.team1bias
        if team == 2:
            for a in self.team2Apples:
                if a in ResObjects.ApplesGoodIds:
                    ts = ts + gameData["goodApple"]
                if a in ResObjects.ApplesBadIds:
                    ts = ts + gameData["badApple"]
            ts = ts + self.team2bias
        return ts

    def addApple(self, team, id):
        if team == 1:
            if id not in self.team1Apples:
                self.team1Apples.append(id)
        if team == 2:
            if id not in self.team2Apples:
                self.team2Apples.append(id)

    def removeApple(self, team, id):
        if team == 1:
            if id in self.team1Apples:
                self.team1Apples.remove(id)
        if team == 2:
            if id in self.team2Apples:
                self.team2Apples.remove(id)


    def resetScore(self):
        self.team1Apples.clear()
        self.team2Apples.clear()              


