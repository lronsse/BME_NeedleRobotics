import cv2
import numpy as np
import imutils
import requests
import copy
import matplotlib.pyplot
from img2 import segmentImg2
from matplotlib import pyplot as plt

from CalculateInsertion import calculateInsertion

from Motor_controller import motor_controller
Controller = motor_controller()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
url = "http://145.94.151.26:8080/shot.jpg"

# Motor parameters
frame_conversion = 150 / 1280  # pixel to mm # TODO: Should be converted properly with cropped frame
step_dis_m1 = 100  # Motor steps required for 10 mm  Z axis
step_dis_m2 = 100  # Motor steps required for 10 mm  Theta modification clockwise
step_dis_m3 = 100  # Motor steps required for 10 mm  X axis

M1 = [0, 0]
M2 = [0, 0]
M3 = [0, 0]

#link = Controller.Home()
link = Controller.get_link()

def getTestImg(img, step):

    img = cv2.imread(img)
    x, y, z = img.shape
    img = cv2.resize(img, (int(y / 2), int(x / 2)))

    data = np.load('Output.npy')
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
    print(arrZ)

    frame = cv2.circle(img, (int(arrX[step]), int(arrZ[step])), radius=10, color=(0, 255, 0),
                                        thickness=-1)

    return frame

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

    #img_resp = requests.get(url)
    #img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    #frame = cv2.imdecode(img_arr, -1)

    # Get the first frame to use an input for next step
    #ret, frame = cap.read()

    # Flip the frame horizontally (Not required)
    #frame = cv2.flip(frame, 1)

    # Intended filename to save results in
    fileName = 'output'

    # Get the intended insertion point and goal, then save to a file
    calculateInsertion(fileName, cv2.imread('BME3.jpeg'))

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

    c1 = len(arrZ) - 1
    for step in range(0, len(arrZ)):
        step = c1 - step

        # First needle must be brought ot the intended point
        # For the XY coord we first move the x and the y of the needle in small increments to the intended val
        # Then we push

        # First optimize the x location
        error = 100
        adjustmentFactor = 10
        maxE = 10  # Threshold error in mm
        while error > 10:  # TODO: why 10?
            # Find current needle position
            # img_resp = requests.get(url)
            # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            # image = cv2.imdecode(img_arr, -1)
            # x, y, z = image.shape
            # image = cv2.resize(image, (int(y / 2), int(x / 2)))
            # For now we use this for debugging purposes

            img = getTestImg('BME3.jpeg', step)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            # Now having the image taken, we can do a mask to find the needle tip since its a unique color we chose
            img = needleTip(img)
            cv2.imshow('img', img)
            cv2.waitKey(0)

            # Now we get the x,y of the needle tip
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
            # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
            contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            cnts = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            # draw contours on the original image
            #image_copy = image.copy()
            #res = cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 0, 255), thickness=5)

            cnts = imutils.grab_contours(cnts)
            cX = 0
            cZ = 0
            count1 = 0
            for c in cnts:
                # compute the center of the contour
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"]) + cX
                cZ = int(M["m01"] / M["m00"]) + cZ
                count1 = count1 + 1

            # Actual co-ordiantes
            cX = int(cX / count1)
            cZ = int(cZ / count1)

            # Then we calulate error on the x-coord
            error = np.sqrt((cX - arrX[step]) ** 2) * frame_conversion  # Actual error in mm

            if error > maxE:
                mov = error * step_dis_m3
                M3 = [mov, 0]
                # move the tip
                if cX > arrX[step]:
                    # in this case we have to decrease x
                    send_arr(link, M1, M2, M3)
                    print('moving down')
                if cX < arrX[step]:
                    # in this case we have to move the x up
                    send_arr(link, M1, M2, M3)
                    print('moving up')

                # Update adjustment factor so we move less next time since we will be closer and to reach a termiation point
                adjustmentFactor /= adjustmentFactor

        # Now optimize the Y location
        error = 100
        adjustmentFactor = 10
        while error > maxE:
            # Find current needle position
            # img_resp = requests.get(url)
            # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
            # image = cv2.imdecode(img_arr, -1)z
            # x, y, z = image.shape
            # image = cv2.resize(image, (int(y / 2), int(x / 2)))

            # For now we use this for debugging purposes
            img = getTestImg('BME3.jpeg', step)
            # Now having the image taken, we can do a mask to find the needle tip since its a unique color we chose
            img = needleTip(img)

            # Now we get teh x,y of the needle tip
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
            # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
            contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            cnts = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            # draw contours on the original image
            #image_copy = image.copy()
            #res = cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 0, 255), thickness=5)

            cnts = imutils.grab_contours(cnts)
            cX = 0
            cZ = 0
            count2 = 0
            for c in cnts:
                # compute the center of the contour
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"]) + cX
                cZ = int(M["m01"] / M["m00"]) + cZ
                count2 = count2 + 1

            # Actual co-ordiantes
            cX = int(cX / count2)
            cZ = int(cZ / count2)

            # Then we calulate error on the x-coord
            error = np.sqrt((cZ - arrZ[step]) ** 2)

            if error > maxE:
                mov = error * step_dis_m1
                M1 = [mov, 0]
                # move the tip
                if cZ > arrZ[step]:
                    send_arr(link, M1, M2, M3)
                    # in this case we have to move the Z back
                    print('moving back')
                if cZ < arrZ[step]:
                    send_arr(link, M1, M2, M3)
                    # in this case we have to move the Z forward
                    print('moving forward')

                # Update adjustment factor so we move less next time since we will be closer and to reach a termiation point
                adjustmentFactor /= 2
god()

