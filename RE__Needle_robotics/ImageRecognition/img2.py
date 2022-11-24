# Import essential libraries
import requests
import cv2
import numpy as np
import imutils
import copy

"""
This part will take in the camera shot and segment it into looking at only the area of interest 
which will be marked with bright yellow tape.
"""


def segmentImg(image):
    #blur the image
    image2 = cv2.GaussianBlur(image, (5, 5), 0)

    hsvPlate = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
    grayPlate = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    colorMin = np.array([24, 40, 158])
    colorMax = np.array([49, 255, 255])
    holdImg = copy.deepcopy(image)
    mask = cv2.inRange(hsvPlate, colorMin, colorMax)
    segPlate = cv2.bitwise_and(holdImg, holdImg, mask=mask)

    element = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
    element_circle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    element3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    segPlate = cv2.erode(segPlate, element)
    segPlate = cv2.dilate(segPlate, element)

    gray = cv2.cvtColor(segPlate, cv2.COLOR_RGB2GRAY)
    x = np.sum(gray, axis=0)
    x2 = np.nonzero(x)
    y = np.sum(gray, axis=1)
    y2 = np.nonzero(y)
    y3 = y2[0][int((len(y2[0]) - 1) / 2)]
    x3 = x2[0][int((len(x2[0]) - 1) / 2)]

    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    crop = cv2.erode(image, element2)
    crop = cv2.dilate(crop, element2)
    crop = crop[y2[0][0]:y2[0][-1], x2[0][0]:x2[0][-1], :]
    coord = [y2[0][0], y2[0][-1], x2[0][0], x2[0][-1]]

    image = cv2.circle(image, (x3, y3), radius=100, color=(255, 0, 0), thickness=1)
    #cv2.imshow('Cropped', crop)
    #cv2.waitKey(0)

    return image, x3, y3


"""
This part will then use the segmented image prom abobve and find where the probe is within the image 
by finding its x and y location, keep in mind the x here is the z for the main code and the x can be 
either the x or the y of the main code.
"""


def findProbe(image):
    hsvPlate = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    grayPlate = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    colorMin = np.array([150, 100, 100])
    colorMax = np.array([255, 255, 255])
    holdImg = copy.deepcopy(image)
    mask = cv2.inRange(hsvPlate, colorMin, colorMax)
    segProbe = cv2.bitwise_and(holdImg, holdImg, mask=mask)

    gray = cv2.cvtColor(segProbe, cv2.COLOR_RGB2GRAY)
    x = np.sum(gray, axis=0)
    x2 = np.nonzero(x)
    y = np.sum(gray, axis=1)
    y2 = np.nonzero(y)
    y3 = y2[0][int((len(y2[0]) - 1) / 2)]
    x3 = x2[0][int((len(x2[0]) - 1) / 2)]
    image = segProbe
    image = cv2.circle(image, (x3, y3), radius=1, color=(255, 0, 0), thickness=-1)
    #image = cv2.circle(image, (x3, y3 + 100), radius=1, color=(255, 0, 0), thickness=-1)
    cv2.imshow('img', image)
    cv2.waitKey(0)
    return x3, y3

def convertXY(x, y, xs, ys):
    xLength = 100000
    yLength = 50000

    x = (xLength/xs) * x
    y = (yLength/ys) * y
    return x, y

"""
This part will combine the two methods above and it is also here that the x and y values are converted to the 
proper values for the main code.
"""


def findOffset(imageName):
    img = cv2.imread(imageName)
    cv2.imshow('original', img)
    cv2.waitKey(0)

    segmented, coords = segmentImg(img)

    #get demensions of segmented image
    #xs, ys, zs = segmented.shape

    #x, y = findProbe(segmented)

    #x, y = convertXY(x, y, xs, ys)


    #print("X coord is {} and Y coord is {}".format(x, y))
    # Convert this x and y into the x and z or y and z the other code uses and we can see the location
    # diff on one axis, so we do this for both perspectives and we have our x and y location


def getFrame(img):
    segmented, coords = segmentImg(img)
    #return findProbe2(segmented)

#findOffset('BME.png')
#findOffset('BME2.png')
#findOffset('BME3.jpeg')

