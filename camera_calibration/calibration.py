# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 14:26:23 2017

@author: Dakota
"""

import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt

def draw(img, corners, imgpnts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpnts[0].ravel()), (255, 0, 0), 5)
    img = cv2.line(img, corner, tuple(imgpnts[1].ravel()), (0, 255, 0), 5)
    img = cv2.line(img, corner, tuple(imgpnts[2].ravel()), (0, 0, 255), 5)
    return img

def calibrateCamera(x, y, square_size, image_folder):
    #  prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((x * y, 3), np.float32)
    objp[:, :2] = np.mgrid[0:x, 0:y].T.reshape(-1, 2)
    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    obj_pnts = []  # 3d points in real world space
    img_pnts = []  # 2d points in image plane.

    # Make a list of calibration images
    images = glob.glob("C:/Users/Dakota/Desktop/Panic/camera calibration/images/calibrate_imgs/*.png")

    #images = glob.glob(image_folder + '/*.png')
    fig, axis = plt.subplots(1, 1)
    # fig.canvas.mpl_connect('key_press_event', press)

    # Step through the list and search for chessboard corners
    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(img, (x, y), None)

        # If found, add object points, image points
        if ret is True:
            # Draw and display the
            # corners
            cv2.drawChessboardCorners(img, (x, y), corners, ret)
            axis.imshow(img)
            axis.set_title(fname)
            plt.waitforbuttonpress(4)
            #  Figure out how to skip addnig an image if one decides its bad
            obj_pnts.append(objp)
            img_pnts.append(corners)



    plt.close
    img_size = (cv2.imread(images[0]).shape[1], cv2.imread(images[0]).shape[0])

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_pnts, img_pnts, img_size, None, None)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    text = fig.suptitle("figure title")

    total_error = 0
    for i in range(len(obj_pnts)):
        imgpoints2, _ = cv2.projectPoints(obj_pnts[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(img_pnts[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        total_error += error

    for idx, fname in enumerate(images):
        img = cv2.imread(fname)
        dst = cv2.undistort(img, mtx, dist, mtx)

        imgpoints2, _ = cv2.projectPoints(obj_pnts[idx], rvecs[idx], tvecs[idx], mtx, dist)
        error = cv2.norm(img_pnts[idx], imgpoints2, cv2.NORM_L2) / len(imgpoints2)

        # fig.suptitle(fname)
        text.set_text(fname + "\n total error: %3f" % total_error )
        ax1.imshow(img)
        ax1.set_title('original')
        ax2.imshow(dst)
        ax2.set_title("undistorted" + "\n rms error: %3f" % error )
        plt.waitforbuttonpress(4)

    return {'mtx': mtx, 'dist': dist, 'error' : total_error, 'image_size' : img_size}


def writeResults(filename, results):
    camera_mtx = results['mtx']
    distortion_params = results['dist']
    image_size = results['image_size']
    total_error = results['error']

    output = open(filename, 'w')
    output.write("image_width: " + str(image_size[0]) + "\n")
    output.write("image_height: " + str(image_size[1]) + "\n")
    output.write("camera_name: " + filename + "\n")
    output.write("camera_matrix:\n")
    output.write("  rows: 3\n")
    output.write("  cols: 3\n")
    output.write("  data: [" + ", ".join(["%8f" % i for i in camera_mtx.reshape(1, 9)[0]]) + "]\n")
    output.write("distortion_model: " + ("rational_polynomial" if distortion_params.size > 5 else "plumb_bob") + "\n")
    output.write("distortion_coefficients:\n")
    output.write("  rows: 1\n")
    output.write("  cols: 5\n")
    dist_size = distortion_params.size
    output.write("  data: [" + ", ".join(["%8f" % i for i in distortion_params.reshape(1, dist_size)[0]]) + "]\n")
    output.write("RMS Error: %8f" % total_error)
    output.close()

if __name__ == "__main__":
    results = calibrateCamera(7, 6, 1.0, 'calibrate_imgs')
    # calib_results = prepyaml('test', results['mtx'], results['dist'], results['image_size'])
    writeResults('test.txt', results)
