# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 15:18:05 2017

@author: Dakota
"""
import glob
import os
import sys
import select
import cv2


#Image Directory
IMAGE_DIR = 'images'

# Prefix for lcd image filenames.
LCD_IMAGES_PREFIX = 'img_'

'''
def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False
'''

# Create the directory for lcd images if it doesn't exist.
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Find the largest ID of existing lcd images.
# Start new images after this ID value.
files = sorted(glob.glob(os.path.join(IMAGE_DIR,LCD_IMAGES_PREFIX + '[0-9][0-9][0-9].png')))
count = 0
if len(files) > 0:
    # Grab the count from the last filename.
    count = int(files[-1][-7:-4])+1

cap = cv2.VideoCapture(0)
#Resolution:0.3MP(Default) 640x480

#Resolution:800x600
#cap.set(3,800); #set frame width
#cap.set(4,600); #set frame height
        
#Resolution:1024x768
#cap.set(3,1024); #set frame width
#cap.set(4,768); #set frame height

#Resolution 1MP 1280x960
#cap.set(3,1280); #set frame width
#cap.set(4,960); #set frame height
                 
#Resolution 1.3MP 1280x1024
#cap.set(3,1280); #set frame width
#cap.set(4,1024); #set frame height

#Resolution:1536x1180
#cap.set(3,1024); #set frame width
#cap.set(4,768); #set frame height
        
#Resolution 2MP 1600x1200
#cap.set(3,1600); #set frame width
#cap.set(4,1200); #set frame height
        
#Resolution 3MP 2048x1680
cap.set(3,2048); #set frame width
cap.set(4,1680); #set frame height

#Resolution 4MP 2240x1680
#cap.set(3,2240); #set frame width
#cap.set(4,1680); #set frame height

#Resolution 5MP 2560x1920
#cap.set(3,2560); #set frame width
#Scap.set(4,1920); #set frame height
        
# Resolution: Max Res (3.6mm lens)       
#cap.set(3,2592); #set frame width
#cap.set(4,1944); #set frame height

        
while(True):

    # Capture frame-by-frame

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    
    # break if q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if cv2.waitKey(1) & 0xFF == ord('c'):
        filename = os.path.join(IMAGE_DIR, LCD_IMAGES_PREFIX + '%03d.png' % count)
        #cropped = gray[60:400, 80:590] #StartY-EndY, StartX-EndX
        cv2.imwrite(filename,gray)
        count += 1
        

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
