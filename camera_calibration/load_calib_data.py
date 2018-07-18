# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 14:46:06 2017

@author: Dakota
"""

import numpy as np
import cv2
import glob
import os
import imutils


#IMAGE_DIR = ./camera_calibration/imgs'

original = cv2.imread("pattern1.png",0)
#resized = imutils.resize(original, 600)
#cv2.imshow('original',resized)
cv2.imshow('original',original)
cv2.imwrite("original.png",original)

#gray = cv2.bilateralFilter(resized, 11, 17, 17)
gray = cv2.bilateralFilter(original, 11, 17, 17)
#edged = cv2.Canny(gray, 30, 200)
edged = imutils.auto_canny(gray)
cv2.imshow("edges_original",edged)
cv2.imwrite("edges_original.png",edged)

#Load calibration data
npzfile = np.load("calibration.npz")
mtx = npzfile.f.mtx
dist = npzfile.f.dist

#h,  w = resized.shape[:2]
h,  w = original.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
#dst = cv2.remap(resized,mapx,mapy,cv2.INTER_LINEAR)
dst = cv2.remap(original,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]

#resized_roi = imutils.resize(dst,600)
#cv2.imshow('calibresult_map',resized_roi)
cv2.imshow('calibresult_map',dst)
cv2.imwrite("calibration_results.png", dst)

edged_roi = imutils.auto_canny(dst)
cv2.imshow("edges_roi",edged_roi)
cv2.imwrite("edges_roi.png", edged_roi)

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
(_,cnts, _) = cv2.findContours(edged_roi.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
screenCnt = None

# loop over our contours
for cnt in contours:
    # approximate the contour
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

    '''
    if our approximated contour has four points, then we can assume that we have found our Rectangle ROI.
    The ROI is saved as a .png image
    '''
    if len(approx) == 4:
        screenCnt = approx
        x, y, width, height = cv2.boundingRect(screenCnt)
        #roi = resized_roi[y:y+height, x:x+width]
        roi = dst[y:y+height, x:x+width]
        cv2.imwrite("roi.png", roi)
        break

#cv2.drawContours(resized_roi, [screenCnt], -1, (255, 0, 255), 2)
#cv2.imshow("LCD Screen", resized_roi)

cv2.drawContours(dst, [screenCnt], -1, (255, 0, 255), 4)
cv2.imshow("LCD Screen", dst)
cv2.imwrite("LCD_identify.png",dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
