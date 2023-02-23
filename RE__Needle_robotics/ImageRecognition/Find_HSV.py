"""

Simple helper class that when run will connect to a camera feed via the internet and provides a GUI where the user can
input the lower and upper bound of HSV values ot try segment specific colors from the video feed.
This was used by us to try find the HSV values to segment the yellow tape from the video feed from out cameras to try
segment the image in calculate insertion.

@author: Arjun, Louis
"""


import cv2
import numpy as np
import time
import requests


# A required callback method that goes into the trackbar function.
def nothing(x):
    pass


url = "BME4.jpeg"
# Not a real url
url = "http://xxx.xxx:8080/shot.jpg"
# Initializing the webcam feed.
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Create a window named trackbars.
cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of
# H,S and V channels. The Arguments are like this: Name of trackbar,
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
while True:

    # Start reading the webcam feed frame by frame.
    #ret, frame = cap.read()
    #if not ret:
    #    break
    # Flip the frame horizontally (Not required)
    #frame = cv2.flip(frame, 1)

    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)
    # 1080, 1920
    frame = frame[300:700, 500:1920, :]

    #frame = segmentImg(frame)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)

    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the new values of the trackbar in real time as the user changes
    # them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")


    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])



    # Filter the image and get the binary mask, where white represents
    # your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    element = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
    elementCircle = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    elementEclipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (200, 200))
    res = cv2.erode(res, elementCircle)
    res = cv2.dilate(res, elementCircle)
    stacked = np.hstack((frame, res))
    img = res
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)
    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    cnts = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    # draw contours on the original image
    image_copy = frame.copy()
    res = cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 0, 255), thickness=5)

    # Converting the binary mask to 3 channel image, this is just so
    # we can stack it with the others
    #stacked = np.hstack((frame, res))

    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stack the mask, orginal frame and the filtered result
    #stacked = np.hstack((frame, res))

    # Show this stacked frame at 40% of the size.
    cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.4, fy=0.4))

    # If the user presses ESC then exit the program
    key = cv2.waitKey(1)
    if key == 27:
        break

    # If the user presses `s` then print this array.
    if key == ord('s'):
        thearray = [[l_h, l_s, l_v], [u_h, u_s, u_v]]
        print(thearray)

        # Also save this array as penval.npy
        np.save('hsv_value', thearray)
        break

# Release the camera & destroy the windows.
cap.release()
cv2.destroyAllWindows()