# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 14:10:24 2018
First attempt to use the webcam
@author: sve_n
"""

import cv2
import numpy as np
import sys
import os 
os.name = OS_NAME 

if OS_NAME is not "posix": # for mac 
    import winsound
    
facePath = "haarcascade_frontalface_default.xml"
smilePath = "haarcascade_smile.xml"
handPath = ""
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

sF = 1.05

while True:

    ret, frame = cap.read() # Capture frame-by-frame
    img = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor= sF,
        minNeighbors=8,
        minSize=(55, 55),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        # draw a bounding box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.7,
            minNeighbors=22,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
            )

        # Set region of interest for smiles
        for (x, y, w, h) in smile:
            print("Found a", len(smile), "smile!")

            if OS_NAME is "posix":
                duration = 0.1  # second
                freq = 440  # Hz
                os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
            else:
                winsound.MessageBeep(type = "MB_ICONEXCLAMATION")
                
            cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)

    cv2.imshow('Smile Detector', frame)
    c = cv2.waitKey(7) % 0x100
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()