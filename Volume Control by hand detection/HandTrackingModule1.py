import cv2
import mediapipe as mp
import time


class HandDetector():
    def __init__(self, mode = False, maxHands = 1, DetectionCon = 0.5, TrackingCon = 0.5):
        
        # static_image_mode=False,
        #  max_num_hands=2,
        #  min_detection_confidence=0.5,
        #  min_tracking_confidence=0.5)

        self.mode = mode
        self.maxHands = maxHands
        self.DetectionCon = DetectionCon
        self.TrackingCon = TrackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, int(self.DetectionCon), int(self.TrackingCon))
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                   # Convert from GBR to RGB
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLMS, self.mpHands.HAND_CONNECTIONS)
        return img
    

    def FindPosition(self, img, handNo = 0, draw = True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id , lm in enumerate(myHand.landmark):           #getting landmark info
                h, w, c = img.shape                               # getting height, width and channels of the image
                cx, cy = int(lm.x*w), int(lm.y*h)                #specifying x and y coordinates according to pixels
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255,0,255), cv2.FILLED)           #makig a big dot on different points on hand for identifying id

        return lmList
        
                        


def main():
    pTime = 0                         #previous Time
    cTime = 0                         #current Time
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()               # Read the video feed from the camera
        img = detector.findHands(img)
        lmList = detector.FindPosition(img)

        if len(lmList)!=0:
            print(lmList[4])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (200, 150, 150), 3)                  #putting frame rate to come on image 



        cv2.imshow("Image", img)                  #opening video through front cam (cam1 as specified in VideoCapture)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()