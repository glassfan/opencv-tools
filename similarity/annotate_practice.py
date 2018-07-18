# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 16:47:04 2017

@author: Dakota
"""

import numpy as np
import cv2
from time import sleep

# create blank image - y, x
img = np.zeros((600, 1000, 3), np.uint8)

# setup text
font = cv2.FONT_HERSHEY_SIMPLEX
text = "Hello Joseph!!"

# get boundary of this text
#textsize = cv2.getTextSize(text, font, 1, 2)[0]

# get coords based on boundary
textX = (img.shape[1] - textsize[0]) / 2
textY = (img.shape[0] + textsize[1]) / 2

# add text centered on image
cv2.putText(img, text, (textX, textY ), font, 1, (255, 255, 255), 2,cv2.LINE_AA)

# display image
cv2.imshow('image', img)

# wait so you can see the image
sleep(25)

# cleanup
cv2.destroyAllWindows()