# importing the module
import cv2
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d


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


# driver function
if __name__ == "__main__":
    # reading the image
    #for j in range(5):
    x_list = []
    y_list = []
    img = cv2.imread('C:\My_Life\Apps\GitHub Desktop\BME_NeedleRobotics\RE__Needle_robotics\Data analysis\Curve\80 degrees\phantom 1\phantom1test1_insertion0.jpg', 1)
    #img = cv2.resize(img, (1920, 1080))
    #img = cv2.flip(img, 0)
    # displaying the image
    cv2.imshow('image', img)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
    #z = np.polyfit(x, y, 3)
    # wait for a key to be pressed to exit
    #key = cv2.waitKey(1)

    #if key == ord('s'):
    #    cv2.destroyAllWindows()
    #df = pd.read_csv('curve_data.csv')
        

# x_list = [1920 - x_list[i] for i in range(len(x_list))]
# y_list = [1080 - y_list[i] for i in range(len(y_list))]

list_coord = [x_list, y_list]
print(list_coord)