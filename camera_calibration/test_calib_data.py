# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 22:28:07 2017
@author: Dakota

test functionality of calibration npz files
"""

import numpy as np
import cv2
import glob
import os

outfile = 'calib.npz'

npzfile = np.load(outfile)

print(npzfile.keys())

print("Camera Matrix: ",npzfile.f.mtx )
print("\n" +"Distance Coeffs: ", npzfile.f.dist)
print("\n" + "rvecs: ", npzfile.f.rvecs)
print("\n" + "tvecs: ", npzfile.f.tvecs)

# Arrays to store object points and image points from all the images.
obj_points = [] # 3d point in real world space
img_points = [] # 2d points in image plane.
h, w = 0, 0
