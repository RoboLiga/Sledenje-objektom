#!/usr/bin/env python
"""Main Tracker Script"""

from timeit import default_timer as timer
import pickle
import sys
import cv2
import cv2.aruco as aruco
import Utils as u
from Resources import ResFileNames, ResGUIText

__author__ = "Laboratory for adaptive systems and parallel processing"
__copyright__ = "Copyright 2019, UL FRI - LASPP"
__credits__ = ["Laboratory for adaptive systems and parallel processing"]
__license__ = "GPL"
__version__ = "0.9"
__maintainer__ = "Davor Sluga"
__email__ = "davor.sluga@fri.uni-lj.si"
__status__ = "Production"

# Load video
cap = cv2.VideoCapture(ResFileNames.videoSource)

# Setting up aruco tags
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)

#Set aruco detector parameters
arucoParameters = aruco.DetectorParameters_create()
u.initArucoParameters(arucoParameters)

# Initialize Tracker stat variables
gameStart, fieldEditMode, gameDataLoaded, changeScore, timeLeft, timeStart, gameData, configMap, quit, ret, frameCounter, objects, gameScore = \
u.initState()

#just for sorting gameData first Time
#with open(ResFileNames.gameDataFileName, "w") as
#f:
#    ujson.dump(gameData,f)

# Set window name
cv2.namedWindow(ResGUIText.sWindowName)
# Start the FPS timer
ts = timer()
while(ret and not quit):
    
    
    
    # Capture/Load frame-by-frame
    ret, frame = cap.read()

    if ret: 
        # Convert to grayscale for Aruco detection
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frameCounter = frameCounter + 1  
        
        # Undistort image
        sharpened = u.undistort(gray)
        configMap.imageHeighth,  configMap.imageWidth = sharpened.shape
        color = cv2.cvtColor(sharpened,cv2.COLOR_GRAY2BGR)
        
        # Detect markers
        cornersTracked, ids, rejectedImgPoints = aruco.detectMarkers(sharpened, aruco_dict, parameters=arucoParameters)
        
        # Compute mass centers and orientation
        pointsTracked = u.getMassCenter(cornersTracked,ids,configMap)
        
        # Detect Validate and track objects on map
        u.track(pointsTracked, objects, frameCounter)
      
        # Check if time ran out and compute remaining time
        gameStart, timeLeft = u.checkTimeLeft(gameStart, timeLeft, gameData["gameTime"], timeStart)
            

        # Write game data to file
        u.writeGameData(configMap, gameScore, gameStart, timeLeft, objects, fieldEditMode)
        
        # Draw GUI and objects
        frame_markers = aruco.drawDetectedMarkers(color.copy(), cornersTracked, ids)
        u.drawOverlay(frame_markers, objects, configMap, timeLeft, gameScore, gameStart, fieldEditMode, changeScore)
        te = timer()
        fps = 1 / (te - ts)        
        u.drawFPS(frame_markers,fps)
        ts=te
        # Show frame
        cv2.imshow(ResGUIText.sWindowName,frame_markers)


        # Process keys
        (gameStart, gameData, gameScore, configMap, timeStart, gameDataLoaded, fieldEditMode, changeScore, quit) = \
        u.processKeys(gameStart, gameData, gameScore, configMap, timeStart, gameDataLoaded, fieldEditMode, changeScore, quit)
        
        #Compute and display FPS
        te = timer()
        fps = 1 / (te - ts)        
        u.drawFPS(frame_markers,fps)
    else:
       print('No video feed!')
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
       break
  
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
sys.exit(0)
