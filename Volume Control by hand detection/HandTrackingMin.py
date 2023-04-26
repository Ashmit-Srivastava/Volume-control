import cv2
import mediapipe as mp
import time

#using camera to capture video
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0                         #previous Time
cTime = 0                         #current Time



while True:
    success, img = cap.read()               # Read the video feed from the camera

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from GBR to RGB
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)                  check if results is decting hand or not

    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            for id , lm in enumerate(handLMS.landmark):           #getting landmark info
                h, w, c = img.shape                               # getting height, width and channels of the image
                cx, cy = int(lm.x*w), int(lm.y*h)                #specifying x and y coordinates according to pixels
                print(id, cx, cy)
                if(id == 0):
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)                #makig a big dot on different points on hand for identifying id
                    


            mpDraw.draw_landmarks(img, handLMS, mpHands.HAND_CONNECTIONS)

    #defining frames
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (200, 150, 150), 3)                  #putting frame rate to come on image 



    cv2.imshow("Image", img)                  #opening video through front cam (cam1 as specified in VideoCapture)
    cv2.waitKey(1)
