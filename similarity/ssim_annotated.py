# -*- coding: utf-8 -*-
"""
Created on Sun Sep  3 12:06:57 2017
@author: Dakota

difference of images via ssim simularity score.
Difference image annotated. 
"""

# import the necessary packages
from skimage.measure import compare_ssim
from scipy.spatial import distance as dist
#import argparse
import imutils
import cv2
import numpy as np

TARGET = (255,255)

def de_noise(img):
    dst = cv2.fastNlMeansDenoising(img,None,10,7,21)
    cv2.imwrite("denoised.png",dst)
    blur = cv2.GaussianBlur(dst,(7,7),2)
    # create a CLAHE object (Arguments are optional).
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #equalized = clahe.apply(blur)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,21,5)
    cv2.imwrite("adaptive_thresholded.png", thresh)
    return thresh

imageA = cv2.imread("all_white_roi.png",0)
imageB = cv2.imread("white1px_roi.png",0)

cleanA = de_noise(imageA)
cleanB = de_noise(imageB)

# compute the Structural Similarity Index (SSIM) between the two
# images, ensuring that the difference image is returned
(score, diff) = compare_ssim(cleanA, cleanB, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))

# threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# loop over the contours
for c in cnts:
	# compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
   (x, y, w, h) = cv2.boundingRect(c)
   cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
   cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
if score < 1:

    cv2.putText(imageB,'SSIM: {}'.format(score),(500,770),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,255),2,cv2.LINE_AA)
    cv2.putText(imageB,'Match to Original:Failed ',(500,795),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,255),2,cv2.LINE_AA)

cv2.imshow("Detected differences", imageB)
cv2.imwrite("Detected_differences.png", imageB)
cv2.waitKey(0)
