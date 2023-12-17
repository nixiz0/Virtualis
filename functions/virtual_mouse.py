import cv2 
import numpy as np
import time
import pyautogui

from functions.HandTrackingModuleVM import HandDetector


def virtual_mouse(num_cam, width_cam, height_cam, fps=True):
    wCam, hCam = width_cam, height_cam
    
    # Frame Reduction
    frameR = 80 
    # Virtual Mouse Smoothing
    smoothening = 3

    # Desactivated the protection for shutdown windows
    pyautogui.FAILSAFE = False 

    cap = cv2.VideoCapture(num_cam)
    cap.set(3, wCam)
    cap.set(4, hCam)
    wScreen, hScreen = pyautogui.size()

    detector = HandDetector(maxHands=1)
    pTime = 0
    # previous location X & Y
    plocX, plocY = 0, 0
    # current location X & Y
    currX, currY = 0, 0

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            x5, y5 = lmList[20][1:]
            
            fingers = detector.fingersUp()
            # frame reduction
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (40, 250, 0), 2)
            
            # Moving on screen
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScreen))
                y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))
                
                currX = plocX + (x3 - plocX) / smoothening
                currY = plocY + (y3 - plocY) / smoothening
                
                pyautogui.moveTo(currX, currY)
                cv2.circle(img, (x1, y1), 9, (0, 0, 255), cv2.FILLED) 
                plocX, plocY = currX, currY
                
            # Click
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 9, (0, 255, 0), cv2.FILLED)
                pyautogui.click()
                    
            # Right Click
            if fingers[1] == 1 and fingers[4] == 1:
                cv2.circle(img, (x5, y5), 9, (0, 255, 0), cv2.FILLED) 
                pyautogui.rightClick()
                    
            # Scroll
            if fingers[0] == 1 and fingers[1] == 1:
                length, img, lineInfo = detector.findDistance(4, 8, img)
                if length < 20:
                    pyautogui.scroll(-50)
                elif 20 < length < 40:
                    pyautogui.scroll(50)
                else: 
                    pyautogui.scroll(0)            
        if fps:
            img, pTime = detector.fps(img, pTime, displayFPS=True)
        else: 
            img, pTime = detector.fps(img, pTime, displayFPS=False)
        
        cv2.imshow("Virtual Mouse (press space to exit)", img)
        if cv2.waitKey(1) == 32:
            cap.release()
            cv2.destroyAllWindows()
            break