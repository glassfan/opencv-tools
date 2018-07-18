# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 09:32:56 2017

@author: Dakota
"""

import time
import cv2


cap = cv2.VideoCapture(0)

cap.set(3,1280)

cap.set(4,1024)

time.sleep(2)

while(True):

    # Capture frame-by-frame

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    # break if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()