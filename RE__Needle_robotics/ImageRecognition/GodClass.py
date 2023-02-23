"""
First attempt at the feedback loop. This class is incomplete and was kept here as a reference. Please ignore it.
A better and the updated version is Feedbackloop.py.

@author: Arjun
"""

import cv2
import numpy as np
import imutils
import requests
import copy
from RE__Needle_robotics.Steedle_software_package.img2 import segmentImg2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
url = "http://145.94.151.26:8080/shot.jpg"

def needleTip(image):
    #blur the image
    image2 = cv2.GaussianBlur(image, (5, 5), 0)

    hsvPlate = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    grayPlate = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # TODO: These colors will need to be min maxed
    colorMin = np.array([50, 100, 100])
    colorMax = np.array([120, 255, 255])

    holdImg = copy.deepcopy(image)
    mask = cv2.inRange(hsvPlate, colorMin, colorMax)
    segPlate = cv2.bitwise_and(holdImg, holdImg, mask=mask)

    element = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
    elementCircle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    elementEclipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    segPlate = cv2.erode(segPlate, elementCircle)
    segPlate = cv2.dilate(segPlate, elementCircle)

    return segPlate

def god():

    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)

    # Get the first frame to use an input for next step
    #ret, frame = cap.read()

    # Flip the frame horizontally (Not required)
    #frame = cv2.flip(frame, 1)

    # Intended filename to save results in
    fileName = 'output'

    # Get the intended insertion point and goal, then save to a file
    #calculateInsertion(fileName, frame)

    # Having calculated the parabola, extract the intended points
    data = np.load('{}.npy'.format(fileName))
    arrX = data[0]
    arrZ = data[1]
    def fixArrZ(arrZ):
        arr = copy.deepcopy(arrZ)
        placeholder = arr[-1]
        for i in range(1, len(arr)):
            arr[i] = arrZ[i - 1]
        arr[0] = placeholder
        return arr
    arrZ = fixArrZ(arrZ)
    print(arrX)

    for step in range(0, len(arrZ)):
        # TODO: movement
        # having the movement done we know that the needle is where it 'should' be,
        # so we can take an image capture here and use that as the actual needle posiiton
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        image = cv2.imdecode(img_arr, -1)
        # Now having the image taken, we can do a mask to find the needle tip since its a unique color we chose
        #img = needleTip(img)
        # For now we use this for debugging purposes
        img = segmentImg2(image)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
        # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        cnts = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        # draw contours on the original image
        image_copy = image.copy()
        res = cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 0, 255), thickness=5)

        cnts = imutils.grab_contours(cnts)
        cX = 0
        cY = 0
        count = 0
        for c in cnts:
            # compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"]) + cX
            cY = int(M["m01"] / M["m00"]) + cY
            count = count + 1

        #Actual co-ordiantes
        cX = int(cX/count)
        cY = int(cY / count)


        # TODO: compute error
        # TODO: error correction
        
god()

