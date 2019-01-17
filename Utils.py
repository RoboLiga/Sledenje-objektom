"""Provides various utility functions"""
import cv2
from Resources import *
from math import sqrt, cos, sin
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from timeit import default_timer as timer
from GameLiveData import GameLiveData
from os import replace
import ujson
import pickle
from ObjectTracker import ObjectTracker
from Entity import Entity
from Score import Score

def correct(x, y, map):
    """Corrects the coordinates.
    Scale0 and scale1 define scaling constants. The scaling factor is a linear function of distance from center.
    Args:
        x (int): x coordinate
        y (int): y coordinate
        map (ResMap) : map object
    Returns:
        Tuple[int, int]: Corrected coordinates
    """

    # Scaling factors
    scale0 = ResCamera.scale0
    scale1 = ResCamera.scale1

    # Convert screen coordinates to 0-based coordinates
    offset_x = map.imageWidth / 2
    offset_y = map.imageHeighth / 2

    # Calculate distance from center
    dist = sqrt((x - offset_x) ** 2 + (y - offset_y) ** 2)

    # Correct coordinates and return
    return (int(round((x - offset_x) * (scale0 + scale1 * dist) + offset_x)),
        int(round((y - offset_y) * (scale0 + scale1 * dist) + offset_y)))

def moveOrigin(x, y, map):
    """Translates coordinate to new coordinate system.
    Scale0 and scale1 define scaling constants. The scaling factor is a linear function of distance from center.
    Args:
        x (int): x coordinate
        y (int): y coordinate
        map (ResMap) : map object
    Returns:
        Tuple[int, int]: Corrected coordinates
    """
    # Translate coordinates if new origin exists (top left corner of map)
    if map.fieldCorners:
        x = x - map.fieldCorners[0][0]
        y = y - map.fieldCorners[0][1]
    return  (x,y) 

def getMassCenter(corners, ids, map):
    """Computes mass centers of objects in the frame.
    Args:
        corners (array of array of float): corners of each object in the frame
        ids (array of array of int): aruco tag ids
        map (ResMap) : map object
    Returns:
        List[int, Tuple[float, float, float, float]]: List of aruco tag ids with object center and top coordinates
    """
    id = 0
    massCenters = []
    for object in corners:
        x1 = object[0][0][0]
        y1 = object[0][0][1]
        x2 = object[0][1][0]
        y2 = object[0][1][1]
        x3 = object[0][2][0]
        y3 = object[0][2][1]
        x4 = object[0][3][0]
        y4 = object[0][3][1]

        #A=1/2*(x1*y2-x2*y1+x2*y3-x3*y2+x3*y4-x4*y3+x4*y1-x1*y4);
        #Cx=1/(6*A)*((x1+x2)*(x1*y2-x2*y1)+ \
                    #(x2+x3)*(x2*y3-x3*y2)+ \
                    #(x3+x4)*(x3*y4-x4*y3)+ \
                    #(x4+x1)*(x4*y1-x1*y4))
        (Cx,Cy) = moveOrigin(*correct((x1 + x2 + x3 + x4) / 4,(y1 + y2 + y3 + y4) / 4,map),map)
        (CxTop,CyTop) = moveOrigin(*correct((x1 + x2) / 2,(y1 + y2) / 2,map),map)
        massCenters.append([ids[id][0],(Cx,Cy,CxTop,CyTop)])
        id = id + 1
    return massCenters

def initState():
    """Initializes Tracker state variables
    Args:
        None
    Returns:
        Tuple[bool, bool, bool, bool, int, int, ResGame, ResMap, bool, bool, int, dict, score]: Initalized state variables
    """
    gameStart = False
    gameDataLoaded = False
    fieldEditMode = False
    changeScore = False
    timeLeft = 0
    timeStart = 0
    gameData = vars(ResGame())
    configMap = ResMap()
    quit = False
    ret = True
    frameCounter = 0
    objects = dict()
    gameScore = Score()
    return (gameStart, fieldEditMode, gameDataLoaded, changeScore, timeLeft, timeStart, gameData, configMap, quit, ret, frameCounter, objects, gameScore)

def initArucoParameters(arucoParameters):
    arucoParameters.adaptiveThreshWinSizeMin = ResArucoDetector.adaptiveThreshWinSizeMin
    arucoParameters.adaptiveThreshWinSizeMax = ResArucoDetector.adaptiveThreshWinSizeMax
    arucoParameters.adaptiveThreshConstant = ResArucoDetector.adaptiveThreshConstant
    arucoParameters.minMarkerPerimeterRate = ResArucoDetector.minMarkerPerimeterRate
    arucoParameters.maxMarkerPerimeterRate = ResArucoDetector.maxMarkerPerimeterRate
    arucoParameters.perspectiveRemovePixelPerCell = ResArucoDetector.perspectiveRemovePixelPerCell
    arucoParameters.perspectiveRemoveIgnoredMarginPerCell = ResArucoDetector.perspectiveRemoveIgnoredMarginPerCell
    arucoParameters.minMarkerDistanceRate = ResArucoDetector.minMarkerDistanceRate


def checkIfObjectInArea(objectPos, area):
    """Checks if object in area of map.
    Args:
        objectPos (list): object x and y coordinates
        area(list of tuple): corners (x and y) of polygon definig the area
    Returns:
        bool: True if object in area
    """
    point = Point(objectPos)
    polygon = Polygon(area)
    return polygon.contains(point)

def getClickPoint(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if	len(param.fieldCorners) == 12:
            param.fieldCorners.clear()
            ResGUIText.fieldDefineGuideId  = 0
        param.fieldCorners.append([x, y])
        ResGUIText.fieldDefineGuideId +=1

def alterScore(event, x, y, flags, param):
    point = Point(moveOrigin(x,y,param[3]))
    polygon1 = Polygon(param[0])
    polygon2 = Polygon(param[1])
    if event == cv2.EVENT_LBUTTONDOWN:
        if polygon1.contains(point):
            param[2].team1bias = param[2].team1bias + 1
        if polygon2.contains(point):
            param[2].team2bias = param[2].team2bias + 1
    if event == cv2.EVENT_RBUTTONDOWN:
        if polygon1.contains(point):
            param[2].team1bias = param[2].team1bias - 1
        if polygon2.contains(point):
            param[2].team2bias = param[2].team2bias - 1
        

def undistort(img):
    # Camera parameters
    k1 = ResCamera.k1
    k2 = ResCamera.k2
    k3 = ResCamera.k3
    p1 = ResCamera.p1
    p2 = ResCamera.p2
    fx = ResCamera.fx
    fy = ResCamera.fy
    cx = ResCamera.cx
    cy = ResCamera.cy
    dist = np.array([k1,k2,p1,p2,k3])
    mtx = np.array([[fx,0,cx],[0,fy,cy],[0,0,1]])
    
    # Setting the params
    h,  w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

    # Undistort
    mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
    dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

    # Crop the image
    x,y,w,h = roi
    dst = dst[y:y + h, x:x + w]
    return dst

def putTextCentered(img,text,pos,font,fontScale,color,thickness=None,lineType=None):
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textX = (pos[0] - textsize[0] // 2)
    cv2.putText(img,text,(textX,pos[1]), font, fontScale,color,thickness,lineType)

def track(pointsTracked,objects,frame_counter):
    for ct in pointsTracked:
            id = ct[0]
            position = ct[1]
            if id in objects:
                objects[id].updateState(position)
                objects[id].detected = True
                objects[id].enabled = True
                objects[id].last_seen = frame_counter
            #if object seen first time add it to the list of tracked ojects
            else: 
                if id in ResObjects.RobotIds:
                   objects[id] = ObjectTracker(ResObjects.ROBOT,id,position,(0,0,0,0))
                   objects[id].last_seen = frame_counter
                elif id in ResObjects.ApplesGoodIds:
                   objects[id] = ObjectTracker(ResObjects.APPLE_GOOD,id,position,(0,0,0,0))
                   objects[id].last_seen = frame_counter
                elif id in ResObjects.ApplesBadIds:
                   objects[id] = ObjectTracker(ResObjects.APPLE_BAD,id,position,(0,0,0,0))
                   objects[id].last_seen = frame_counter
                   
        #Disable object tracking if not seen detected for a long time
    for k, v in list(objects.items()): 
        if (frame_counter - v.last_seen) > ResObjects.ObjectTimeout:
            objects[k].enabled = False      
        
    #Track undetected objects
    for obj in objects:
        if objects[obj].detected == False:
            objects[obj].lost_frames = objects[obj].lost_frames + 1 
            if objects[obj].enabled == True:
                objects[obj].updateState([])
        objects[obj].detected = False 

def checkTimeLeft(gameStart, timeLeft, startTime, totalTime):
    if gameStart:
        timeLeft = totalTime - (timer() - startTime)
    else:
        timeLeft = 0
    if timeLeft <= 0:
        gameStart = False
        timeLeft = 0  
    
    return (gameStart,timeLeft)     

def writeGameData(configMap, gameScore, gameStart, timeLeft, objects):
    gLive = GameLiveData()    
    gLive.gameOn = gameStart     
    gLive.timeLeft = timeLeft
    # Fill map data
    if len(configMap.fieldCorners) == 12:
        gLive.field["TopLeft"] = moveOrigin(*tuple(configMap.fieldCorners[0]),configMap)
        gLive.field["TopRight"] = moveOrigin(*tuple(configMap.fieldCorners[1]),configMap)
        gLive.field["BottomRight"] = moveOrigin(*tuple(configMap.fieldCorners[2]),configMap)
        gLive.field["BottomLeft"] = moveOrigin(*tuple(configMap.fieldCorners[3]),configMap)
        
        gLive.baskets["Team1"]["TopLeft"] = moveOrigin(*tuple(configMap.fieldCorners[5]),configMap)
        gLive.baskets["Team1"]["TopRight"] = moveOrigin(*tuple(configMap.fieldCorners[6]),configMap)
        gLive.baskets["Team1"]["BottomRight"] = moveOrigin(*tuple(configMap.fieldCorners[7]),configMap)
        gLive.baskets["Team1"]["BottomLeft"] = moveOrigin(*tuple(configMap.fieldCorners[4]),configMap)

        gLive.baskets["Team2"]["TopLeft"] = moveOrigin(*tuple(configMap.fieldCorners[8]),configMap)
        gLive.baskets["Team2"]["TopRight"] = moveOrigin(*tuple(configMap.fieldCorners[9]),configMap)
        gLive.baskets["Team2"]["BottomRight"] = moveOrigin(*tuple(configMap.fieldCorners[10]),configMap)
        gLive.baskets["Team2"]["BottomLeft"] = moveOrigin(*tuple(configMap.fieldCorners[11]),configMap)
    #Fill objects
    for obj in objects:
        if objects[obj].enabled == True:
            if objects[obj].type == ResObjects.ROBOT:
                gLive.robots.append(Entity(objects[obj].type,objects[obj].id,objects[obj].position,objects[obj].direction))
            if objects[obj].type == ResObjects.APPLE_GOOD:
                gLive.apples.append(Entity(objects[obj].type,objects[obj].id,objects[obj].position,objects[obj].direction))
            if objects[obj].type == ResObjects.APPLE_BAD:
                gLive.apples.append(Entity(objects[obj].type,objects[obj].id,objects[obj].position,objects[obj].direction))
        
    # Compute score
    AreaT1 = [gLive.baskets["Team1"]["TopLeft"],gLive.baskets["Team1"]["TopRight"],gLive.baskets["Team1"]["BottomRight"],gLive.baskets["Team1"]["BottomLeft"]]
    AreaT2 = [gLive.baskets["Team2"]["TopLeft"],gLive.baskets["Team2"]["TopRight"],gLive.baskets["Team2"]["BottomRight"],gLive.baskets["Team2"]["BottomLeft"]]
    for a in gLive.apples:
        if checkIfObjectInArea([a.X,a.Y],AreaT1):
            gameScore.addApple(1,a.id)
        if checkIfObjectInArea([a.X,a.Y],AreaT2):
            gameScore.addApple(2,a.id)
    gLive.score["Team1"] = gameScore.getScore(1)
    gLive.score["Team2"] = gameScore.getScore(2)
    outputFile = ResFileNames.gameLiveDataTempFileName
    with open(str(outputFile),'w') as f:
        #f.write(gLive.toJSON())
        ujson.dump(gLive,f)
    try:
        replace(ResFileNames.gameLiveDataTempFileName,ResFileNames.gameLiveDataFileName)
    except:
        pass

def drawOverlay(frame_markers, objects, configMap, timeLeft, gameScore, gameStart, fieldEditMode, changeScore):
        
        # Display object centers and direction
        for obj in objects:
            cv2.circle(frame_markers, (int(round(objects[obj].position[0])),int(round(objects[obj].position[1]))), 2, (0,255,255),2) 
            cv2.line(frame_markers, (int(round(objects[obj].position[0])),int(round(objects[obj].position[1]))), (int(round(objects[obj].position[0] + 20 * cos(objects[obj].direction))),int(round(objects[obj].position[1] + 20 * sin(objects[obj].direction)))), (255,0,196), 2)
        # Set font
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Display time left and score
        if gameStart:
            #cv2.putText(frame_markers,'Game On',(10,56), font,
            #1,(0,255,0),2,cv2.LINE_AA)
            putTextCentered(frame_markers,ResGUIText.sTimeLeft + str(round(timeLeft)) +' '+ ResGUIText.sScore + str(gameScore.getScore(1)) + ' - ' + str(gameScore.getScore(2)),(configMap.imageWidth // 2,30), font, 1,(0,0,255),2,cv2.LINE_AA)
        # Display info when in map edit mode
        if fieldEditMode:
            #cv2.putText(frame_markers,'Field edit mode On',(10,56), font,
            #1,(0,255,0),2,cv2.LINE_AA)
            putTextCentered(frame_markers,ResGUIText.sFieldDefineGuide[ResGUIText.fieldDefineGuideId],(configMap.imageWidth // 2,30), font, 1,(255,0,0),2,cv2.LINE_AA)   
        
        # Display info when in change score mode  
        if changeScore:
            try:
               textX = (configMap.fieldCorners[5][0] + configMap.fieldCorners[7][0]) // 2
               textY = (configMap.fieldCorners[5][1] + configMap.fieldCorners[7][1]) // 2
               putTextCentered(frame_markers,str(gameScore.getScore(1)),(textX,textY), font, 1,(0,255,0),2,cv2.LINE_AA)
               textX = (configMap.fieldCorners[8][0] + configMap.fieldCorners[10][0]) // 2
               textY = (configMap.fieldCorners[8][1] + configMap.fieldCorners[10][1]) // 2
               putTextCentered(frame_markers,str(gameScore.getScore(2)),(textX,textY), font, 1,(0,255,0),2,cv2.LINE_AA)
            except: 
                pass
        # Display map
        for p in configMap.fieldCorners:
            cv2.circle(frame_markers, (p[0],p[1]), 3, (0,255,255),3)
        try:
            cv2.line(frame_markers, tuple(configMap.fieldCorners[0]), tuple(configMap.fieldCorners[1]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[1]), tuple(configMap.fieldCorners[2]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[2]), tuple(configMap.fieldCorners[3]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[3]), tuple(configMap.fieldCorners[0]), (0,255,255), 2)

            cv2.line(frame_markers, tuple(configMap.fieldCorners[4]), tuple(configMap.fieldCorners[5]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[5]), tuple(configMap.fieldCorners[6]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[6]), tuple(configMap.fieldCorners[7]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[7]), tuple(configMap.fieldCorners[4]), (0,255,255), 2)

            cv2.line(frame_markers, tuple(configMap.fieldCorners[8]), tuple(configMap.fieldCorners[9]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[9]), tuple(configMap.fieldCorners[10]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[10]), tuple(configMap.fieldCorners[11]), (0,255,255), 2)
            cv2.line(frame_markers, tuple(configMap.fieldCorners[11]), tuple(configMap.fieldCorners[8]), (0,255,255), 2)
        except:
            pass
        #Display help
        cv2.putText(frame_markers,ResGUIText.sHelp,(10,configMap.imageHeighth - 10), font, 0.5,(0,0,255),1,cv2.LINE_AA)

def drawFPS(frame_markers,fps):
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Display FPS
        cv2.putText(frame_markers,ResGUIText.sFps + str(int(fps)),(10,30), font, 1,(0,255,255),2,cv2.LINE_AA)

def processKeys(gameStart, gameData, gameScore, configMap, startTime, gameDataLoaded, fieldEditMode, changeScore, quit):
    
    # Detect key press
    keypressed = cv2.waitKey(1) & 0xFF
    
    # Game start
    if keypressed == ord(ResKeys.startGameKey) and not fieldEditMode and gameDataLoaded:
        gameStart = not gameStart
        if gameStart:
            startTime = timer()
            gameScore = Score()
            if changeScore:
                AreaT1 = [moveOrigin(*tuple(configMap.fieldCorners[5]),configMap),moveOrigin(*tuple(configMap.fieldCorners[6]),configMap),moveOrigin(*tuple(configMap.fieldCorners[7]),configMap),moveOrigin(*tuple(configMap.fieldCorners[4]),configMap)]
                AreaT2 = [moveOrigin(*tuple(configMap.fieldCorners[8]),configMap),moveOrigin(*tuple(configMap.fieldCorners[9]),configMap),moveOrigin(*tuple(configMap.fieldCorners[10]),configMap),moveOrigin(*tuple(configMap.fieldCorners[11]),configMap)]
                cv2.setMouseCallback(sWindowName, alterScore, [AreaT1,AreaT2,gameScore,configMap])
               
    
    # Load game data
    elif keypressed == ord(ResKeys.loadKey) and not gameStart and not fieldEditMode:
            try:
                with open(ResFileNames.gameDataFileName, "r") as read_file:
                    gameData = ujson.load(read_file)
                gameDataLoaded = True
                print("Game Data loaded!")
            except Exception as e: 
                print(e)
                print('Game data file could not be loaded!')
            # Try to load map if exists
            try:
                with open(ResFileNames.mapConfigFileName, 'rb') as map:
                    configMap = pickle.load(map)
            except Exception as e: 
                print(e)
    # Edit Map mode
    elif keypressed == ord(ResKeys.editMapKey) and not gameStart:
            fieldEditMode = not fieldEditMode
            if fieldEditMode:
                configMap.fieldCorners.clear()
                cv2.setMouseCallback(ResGUIText.sWindowName, getClickPoint,configMap)
            else:
                cv2.setMouseCallback(ResGUIText.sWindowName, lambda *args : None)
    
    # Change score mode
    elif keypressed == ord(ResKeys.alterScoreKey) and gameDataLoaded and len(configMap.fieldCorners)==12:
        changeScore = not changeScore
        if changeScore:
            AreaT1 = [moveOrigin(*tuple(configMap.fieldCorners[5]),configMap),moveOrigin(*tuple(configMap.fieldCorners[6]),configMap),moveOrigin(*tuple(configMap.fieldCorners[7]),configMap),moveOrigin(*tuple(configMap.fieldCorners[4]),configMap)]
            AreaT2 = [moveOrigin(*tuple(configMap.fieldCorners[8]),configMap),moveOrigin(*tuple(configMap.fieldCorners[9]),configMap),moveOrigin(*tuple(configMap.fieldCorners[10]),configMap),moveOrigin(*tuple(configMap.fieldCorners[11]),configMap)]
            cv2.setMouseCallback(ResGUIText.sWindowName, alterScore, [AreaT1,AreaT2,gameScore,configMap])
        else:
            cv2.setMouseCallback(ResGUIText.sWindowName, lambda *args : None)
    # Quit
    elif keypressed == ord(ResKeys.quitKey):
        quit = True
    return gameStart, gameData, gameScore, configMap, startTime, gameDataLoaded, fieldEditMode, changeScore, quit
