import cv2
import time
import numpy as np
import HandTrackingModule1 as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#########################################################
wCam, hCam = 640, 480                                        #Defining width and height of cam window
########################################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)                                               #setting defined width 
cap.set(4, hCam)

cTime, pTime = 0,0

detector = htm.HandDetector(DetectionCon=0.8)                                  #creating an object


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

print(minVol, maxVol)
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.FindPosition(img, draw = False)
    if len(lmList) != 0:    
        # print(lmList[4], lmList[8])                                                      
        
        x1, y1 = lmList[8][1], lmList[8][2]                                              #getting position of index finger tip
        x2, y2 = lmList[4][1], lmList[4][2]                                              #getting position of thumb tip
        cx, cy = (x1+x2)//2, (y1+y2)//2


        cv2.circle(img, (x1,y1), 10, (0, 255, 0), 3)                                      #drawing ring around points of use
        cv2.circle(img, (x2,y2), 10, (0, 255, 0), 3)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 2)                                   #joining the 2 poins
        cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)

        
        length = math.hypot(x2-x1, y2-y1)


        if(length<30):
            cv2.circle(img, (cx, cy), 10, (0,0,255), cv2.FILLED)                          #changing center of line colour when length less than 30


        #Hand range 30 - 170
        #Volume range -96 - 0

        vol = np.interp(length, [30, 125], [minVol, maxVol])
        volBar = np.interp(length, [30, 125], [400, 120])
        volPer = np.interp(length, [30, 125], [0, 100])

        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, [30,120], [60, 400], (0,255,0), 3)
    cv2.rectangle(img, [30,int(volBar)], [60, 400], (0,255,0), cv2.FILLED)
    cv2.putText(img, f'Vol: {(int(volPer))} %', (20,100), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 0), 2)        #putting volume percentage



    cTime = time.time()
    fps = 1/(cTime-pTime)                                         #Defining frame rate
    pTime = cTime    

    cv2.putText(img, f'FPS: {(int(fps))}', (20,40), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 0, 0), 2)                  #putting frame rate to come on image 


    cv2.imshow("Image", img)
    cv2.waitKey(1)