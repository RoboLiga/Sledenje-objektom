"""Provides starting configurations and resources"""
#import json
class ResGame:
    """Game configuration"""
    def __init__(self):
        # Aruco Id for each team
        self.teams = {
                    '0' :'Ekipa 1',
                    '1' :'Ekipa 2'
                }
        self.currentGameTeams = {
                                'Team1': 0,
                                'Team2': 1
                       }
        # Game Time in seconds
        self.gameTime = 120
        # Apple value
        self.goodApple = 1
        self.badApple = -2
    #def toJSON(self):
    #    return json.dumps(self, default=lambda o: o.__dict__,
    #        sort_keys=False, indent=4)
class ResObjects:
    """Stores Object configs"""
    ROBOT = 0
    APPLE_GOOD = 1
    APPLE_BAD = 2
    RobotIds = {0, 5, 12, 14, 18, 19, 25, 32, 33, 35, 39, 41, 44}
    ApplesGoodIds = {9, 22, 27, 29, 36, 40, 43, 47}
    ApplesBadIds = {10, 24, 30, 42}
    ObjectTimeout = 50
    PosLimitX = [-50,3600]
    PosLimitY = [-50,2100]

class ResFileNames:
    """Stores file names for json data"""
    gameDataFileName = "gameData.json"
    gameLiveDataFileName = "../nginx/html/game.json"
    gameLiveDataTempFileName = "gameLiveTemp.json"
    mapConfigFileName = "mapConfig"
    #videoSource = "rtsp://193.2.72.149/axis-media/media.amp"
    videoSource="http://193.2.72.149/mjpg/video.mjpg"

class ResKeys:
    loadKey = 'l'
    editMapKey = 'e'
    alterScoreKey = 'c'
    startGameKey = 's'
    quitKey = 'q' 

class ResGUIText:
    """Holds various strings displayed on window"""
    sFieldDefineGuide = ['Mark Field Top Left Corner',
                             'Mark Field Top Right Corner',
                             'Mark Field Bottom Right Corner',
                             'Mark Field Bottom Left Corner',
                             'Mark Team 1 Bottom Left Corner',
                             'Mark Team 1 Top Left Corner',
                             'Mark Team 1 Top Right Corner',
                             'Mark Team 1 Bottom Right Corner',
                             'Mark Team 2 Top Left Corner',
                             'Mark Team 2 Top Right Corner',
                             'Mark Team 2 Bottom Right Corner',
                             'Mark Team 2 Bottom Left Corner',
                             'Mark Field Top Left Corner']
    fieldDefineGuideId = 0
    sFps = 'FPS: '
    sTimeLeft = 'Time left: '
    sScore = ' Score: '
    sHelp = 'HotKeys: ' + ResKeys.loadKey + ' - load game data | ' + ResKeys.editMapKey + ' - edit map | ' + ResKeys.alterScoreKey + ' - alter score | ' + ResKeys.startGameKey + ' - start game | ' + ResKeys.quitKey + ' - quit'
    sWindowName = 'Tracker'
    


class ResMap:
    """Stores Map configs"""
    def __init__(self):
        self.fieldCorners = []
        self.imageWidth = 0
        self.imageHeighth = 0
        self.fieldCornersVirtual=[[0,2055], [3555,2055],[3555,0],[0,0]]
        self.M = []
        
    

class ResKalmanFilter:
    """Stores Kalman Filter configs"""
    dt = 1 # Sampling rate
    u = 0.0 # Acceleration magnitude
    accNoiseMag = 0.003
    measurementNoiseX = 0.6
    measurementNoiseY = 0.6

class ResArucoDetector:
    # Min.  okno za binarizacijo.  Premajhno okno naredi celotne tage iste
    # barve
    adaptiveThreshWinSizeMin = 13
    # Max.  okno.  Preveliko okno prevec zaokrozi kote bitov na tagu
    adaptiveThreshWinSizeMax = 23
    # Dno za thresholding.  Prenizko dno povzroci prevec kandidatov, previsoko
    # popaci tage (verjetno tudi odvisno od kontrasta)
    adaptiveThreshConstant = 7
    # Najmanjsa velikost kandidatov za tage.  Prenizko pregleda prevec
    # kandidatov in vpliva na performanse
    minMarkerPerimeterRate = 0.04
    # Najvecja velikost kandidatov.  Rahlo vpliva na performanse, vendar je
    # prevelikih kandidatov ponavadi malo
    maxMarkerPerimeterRate = 0.1
    # Algoritem izreze tag in ga upsampla na x pixlov na celico.  Vpliva na
    # prefromanse
    perspectiveRemovePixelPerCell = 30
    # Algoritem vsako celico obreze in gleda samo sredino.  Vecji faktor bolj
    # obreze
    perspectiveRemoveIgnoredMarginPerCell = 0.30
    # Verjetno najpomembnejsi parameter za nas.  Omejitev kako blizu sta lahko
    # dva taga.  Ker so nasi lahko zelo blizu,
    # moramo to nastaviti nizko, kar pa lahko pomeni, da isti tag detektira
    # dvakrat, kar lahko filtriramo naknadno.
    minMarkerDistanceRate = 0.001

class ResCamera:
    """Stores camera configs"""

    # Camera parameters for removing distortion
    k1 = -0.4077
    k2 = 0.2827
    k3 = -0.1436
    p1 = 6.6668e-4
    p2 = -0.0025
    fx = 1445#1.509369848235880e+03#
    fy = 1.509243126646947e+03
    cx = 9.678725207348843e+02
    cy = 5.356599023732050e+02

    # Scaling factors
    scale0 = 0.954
    scale1 = 0.00001