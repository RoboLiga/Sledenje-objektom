import numpy as np
import math
import cv2
## For Aruco tags you need cv2 contrib library
import cv2.aruco as aruco
from timeit import default_timer as timer
import worldObject2 as worldObject
#import worldObject as worldObject





# Load video
cap = cv2.VideoCapture("../Videos/ROBO_9.mp4")
#counter = 0;
#cap = cv2.VideoCapture(0)
#cap.set(3,1280)
#cap.set(4,720)


ret = True
frame_counter = 0
objects=dict()

# Setting up aruco tags
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_100)
parameters =  aruco.DetectorParameters_create()
# Min. okno za binarizacijo. Premajhno okno naredi celotne tage iste barve
parameters.adaptiveThreshWinSizeMin = 13
# Max. okno. Preveliko okno prevec zaokrozi kote bitov na tagu
parameters.adaptiveThreshWinSizeMax = 23
# Dno za thresholding. Prenizko dno povzroci prevec kandidatov, previsoko popaci tage (verjetno tudi odvisno od kontrasta)
parameters.adaptiveThreshConstant = 7
# Najmanjsa velikost kandidatov za tage. Prenizko pregleda prevec kandidatov in vpliva na performanse
parameters.minMarkerPerimeterRate = 0.04
# Najvecja velikost kandidatov. Rahlo vpliva na performanse, vendar je prevelikih kandidatov ponavadi malo
parameters.maxMarkerPerimeterRate = 0.1
# Algoritem izreze tag in ga upsampla na x pixlov na celico. Vpliva na prefromanse
parameters.perspectiveRemovePixelPerCell = 30
# Algoritem vsako celico obreze in gleda samo sredino. Vecji faktor bolj obreze
parameters.perspectiveRemoveIgnoredMarginPerCell = 0.30
# Verjetno najpomembnejsi parameter za nas. Omejitev kako blizu sta lahko dva taga. Ker so nasi lahko zelo blizu,
# moramo to nastaviti nizko, kar pa lahko pomeni, da isti tag detektira dvakrat, kar lahko filtriramo naknadno.
parameters.minMarkerDistanceRate = 0.001
def getMassCenter(corners, ids):
    id=0
    massCenters=[]
    for object in corners:
        x1=object[0][0][0];
        y1=object[0][0][1];
        x2=object[0][1][0];
        y2=object[0][1][1];
        x3=object[0][2][0];
        y3=object[0][2][1];
        x4=object[0][3][0];
        y4=object[0][3][1];

        #A=1/2*(x1*y2-x2*y1+x2*y3-x3*y2+x3*y4-x4*y3+x4*y1-x1*y4);
        #Cx=1/(6*A)*((x1+x2)*(x1*y2-x2*y1)+ \
                    #(x2+x3)*(x2*y3-x3*y2)+ \
                    #(x3+x4)*(x3*y4-x4*y3)+ \
                    #(x4+x1)*(x4*y1-x1*y4))
        Cx=int(round((x1+x2+x3+x4)/4))
        Cy=int(round((y1+y2+y3+y4)/4))
        CxTop=(x1+x2)/2
        CyTop=(y1+y2)/2
        theta=math.atan2(CyTop-Cy,CxTop-Cx)
        #print(ids[id][0],Cx,Cy,theta*180/math.pi)
        massCenters.append([ids[id][0],(Cx,Cy),theta])
        id=id+1
    return massCenters



#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# Create our shapening kernel and convolve
#kernel_sharpening = np.array([[-1,-1,-1], [-1, 9,-1],[-1,-1,-1]])
#kernel_sharpening = np.array([[-4,-1,0,-1,-4],[-1,2,3,2,-1],[0,3,4,3,0],[-1,2,3,2,-1],[-4,-1,0,-1,-4]])

#for test.mp4
#best params:0.34 130
#BEST VALUES: 0.87 71 with AVG ERROR 5.639929652840706
#BEST VALUES: 0.1 100 with AVG ERROR 6.34111453041444
#BEST VALUES: 0.05 29 with AVG ERROR 3.9933071579347823
#BEST VALUES: 0.026 7.7 with AVG ERROR 3.9953676880811564
#BEST VALUES FIT: 0.047 6.4

#for tag_action.mp4
#BEST VALUES: 0.01 7 with AVG ERROR 8.56119409183915
#BEST VALUES: 0.003 0.6 with AVG ERROR 8.417411832147696
ts = timer()
while(ret):
    # Capture/Load frame-by-frame
    ret, frame = cap.read()
    frame_counter=frame_counter+1;
    # This serves only for clean exit from a video
    # If you want to exit the video stream and stop simulation just press q 
    # on keyboard
    if ret:   
        # applying the sharpening kernel to the input image & displaying it.
        sharpened = frame;
        #sharpened = cv2.filter2D(frame, -1, kernel_sharpening)

        #psf = np.ones((5, 5)) / 25
        # Add Noise to Image
        
        # Restore Image using Richardson-Lucy algorithm
       # sharpened = restoration.richardson_lucy(gray, psf, iterations=30)
        #print(parameters)qq
        #lists of ids and the corners beloning to each id
        cornersTracked, ids, rejectedImgPoints = aruco.detectMarkers(sharpened, aruco_dict, parameters=parameters)
        centersTracked=getMassCenter(cornersTracked,ids)
        for ct in centersTracked:
            id=ct[0];
            position=ct[1];
            direction=ct[2];
            if id in objects:
                objects[id].updateState(position)
                objects[id].direction=direction
                objects[id].detected=True
                objects[id].enabled=True
                objects[id].last_seen=frame_counter;
            else: 
                objects[id]=worldObject.Object(worldObject.ROBOT,id,position,direction,(0,0))
                objects[id].last_seen=frame_counter;

        for k, v in list(objects.items()): 
            if (frame_counter-v.last_seen)>100:
                #del objects[k]
                objects[k].enabled=False      

        for obj in objects:
            
            if objects[obj].detected==False:
                objects[obj].lost_frames=objects[obj].lost_frames+1 
                if objects[obj].enabled==True:
                    objects[obj].updateState([])
            objects[obj].detected=False
            #print(objects[obj].id,' ',objects[obj].lost_frames/frame_counter)
        frame_markers = aruco.drawDetectedMarkers(frame.copy(), cornersTracked, ids)
        for obj in objects:
            cv2.circle(frame_markers, (int(round(objects[obj].position[0])),int(round(objects[obj].position[1]))), 2, (0,255,255),2) 
            #cv2.line(frame_markers, cs[1], (int(round(cs[1][0]+20*math.cos(cs[2]))),int(round(cs[1][1]+20*math.sin(cs[2])))), (255,0,196), 2)
        te = timer()
        fps=frame_counter/(te-ts)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame_markers,'FPS: '+str(int(fps)),(10,30), font, 1,(0,255,255),2,cv2.LINE_AA)
        cv2.imshow('frame',frame_markers)
        #cv2.imshow('frame',centers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
       print('no video')
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()