"""

This the class we run to combine everything together. Running it takes the video and outputs the probes position using
all the methods from the other classes to process the image.

@author: Arjun, Louis
"""

# Import essential libraries
import cv2
import numpy as np
import imutils

# Replace the below URL with your own. Make sure to add "/shot.jpg" at last.
from RE__Needle_robotics.Steedle_software_package.img2 import segmentImg

url = "http://xxx.xxx:8080/shot.jpg"

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

coords = np.array([])
# While loop to continuously fetching data from the Url
while True:
    ret, frame = cap.read()
    if not ret:
        break
    #img_resp = requests.get(url)
    #img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    #img = cv2.imdecode(img_arr, -1)
    img = frame
    img = imutils.resize(img, width=1000, height=1800)
    img, x, y = segmentImg(img)
    coords = np.append(coords, (x, y))
    cv2.imshow("Android_cam", img)
    print(coords)
    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()