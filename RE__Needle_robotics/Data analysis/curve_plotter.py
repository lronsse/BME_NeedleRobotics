# importing the module
import cv2
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

'''
Code used to discretise the shape and curvature of the needle path during hte curved insertion tests in order to plot 
them for the report.
'''
# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
        x_list.append(x)
        y_list.append(y)
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)

total_coordx = []
total_coordy = []
total_coord = []
# driver function
if __name__ == "__main__":
    # reading the image
    for j in range(5):
        x_list = []
        y_list = []
        img = cv2.imread(f'C:\My_Life\Apps\GitHub Desktop\BME_NeedleRobotics\RE__Needle_robotics\Data analysis\Curve\90 degrees\phantom3\phantom3\phantom3test5_insertion.jpg', 1)
        img = cv2.resize(img, (1920, 1080))
        img = cv2.flip(img, 1)
        # displaying the image
        cv2.imshow('image', img)

        # setting mouse handler for the image
        # and calling the click_event() function
        cv2.setMouseCallback('image', click_event)
        #z = np.polyfit(x, y, 3)
        # wait for a key to be pressed to exit
        key = cv2.waitKey(0)
        x_list = [x_list[i] - x_list[0] for i in range(len(x_list))]
        y_list = [y_list[i] - y_list[0] for i in range(len(y_list))]
        y_list = [-y_list[i] for i in range(len(y_list))]
        list_coord = [x_list, y_list]
        #total_coordx.append(x_list)
        #total_coordy.append(y_list)
        #total_coord.append(list_coord)
        print(f'test {j+1} : {list_coord}')
