import cv2
import numpy as np
import copy
import matplotlib.pyplot as plt
import numpy as np

cv2.namedWindow("Trackbars")

def nothing(x):
    pass

def showImage(image):
    img = cv2.imread(image)
    x, y, z = img.shape
    img = cv2.resize(img, (int(y/2), int(x/2)))
    cv2.imshow('image', img)
    cv2.waitKey(0)


def main():
    img = 'BME3.jpeg'
    img = cv2.imread(img)
    x, y, z = img.shape
    img = cv2.resize(img, (int(y / 2), int(x / 2)))
    x, y, z = img.shape
    cv2.createTrackbar("Insertion Point", "Trackbars", 0, y, nothing)
    cv2.imshow('Trackbars', img)
    new_val = cv2.getTrackbarPos("Insertion Point", "Trackbars")
    #print(new_val)
    cv2.waitKey(0)


def draw(newX, newY, steps):
    # Variable set up
    I = 10  # The centre of the circle measured from the template
    K = 150  # Radius of circle
    K = newX + 150
    X1 = 30  # Start X-coordinate
    Y1 = 30  # Start Y-coodrinate

    X2 = newY  # End X-coordinate
    Y2 = newX  # End Y-coordinate
    #print(X2)

    datasets = []  # Array of arrays containing all the x and y point for every height
    z2 = []
    x2 = []
    y2 = []

    steps = steps  # Determines the precision of the visualization

    A = (Y2 - Y1) / (X2 - X1)  # Directional coefficient of path
    B = Y1 - A * X1  # Intersection point with y-axis

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    R_arr = np.linspace(1, 120, 40)

    # Projection of movement space of needle tip
    for i in range(len(R_arr)):
        x_cont = np.linspace(-R_arr[i], R_arr[i], 100)
        y_cont = np.sqrt(R_arr[i] ** 2 - x_cont ** 2)
        z = np.sqrt(K ** 2 - R_arr[i] ** 2)

        datasets.append([x_cont, y_cont, z])
        # ax.plot(x_cont, y_cont, z, color='grey')

    x_arr = np.linspace(X1, X2, steps)
    y_arr = []
    z_arr = []

    # Display movement path of needle tip
    for i in range(len(x_arr)):
        y_arr.append(A * x_arr[i] + B)
        R = np.sqrt(x_arr[i] ** 2 + y_arr[i] ** 2)
        #print(K - R)
        z_arr.append(np.sqrt(K ** 2 - R ** 2))

    # Drawing the needle curve on the x-y plane from the template to the starting point
    Q = z_arr[0]
    Re = np.sqrt(x_arr[0] ** 2 + y_arr[0] ** 2)  # Radius of needle deviation at starting point
    theta = np.arctan(x_arr[0] / y_arr[0])

    zN = np.linspace(0, z_arr[0], steps)
    yN = Re / (Q ** 2) * zN ** 2  # Re_arr
    xN = np.zeros(steps)

    # Rotating the needle curve in the right configuration in 3 dimensional space
    zR = zN
    yR = yN * np.cos(theta) - xN * np.sin(theta)
    xR = yN * np.sin(theta) + xN * np.cos(theta)

    # Drawing the needle curve on the x-y plane from the template to the end point
    Q2 = z_arr[steps - 1]
    Re2 = np.sqrt(x_arr[steps - 1] ** 2 + y_arr[steps - 1] ** 2)  # Radius of needle deviation at starting point
    theta2 = np.arctan(x_arr[steps - 1] / y_arr[steps - 1])

    zN2 = np.linspace(0, z_arr[steps - 1], steps)
    yN2 = Re2 / (Q ** 2) * zN ** 2  # Re_arr
    xN2 = np.zeros(steps)

    # Rotating the needle curve in the right configuration in 3 dimensional space
    zR2 = zN2
    yR2 = yN2 * np.cos(theta2) - xN2 * np.sin(theta2)
    xR2 = yN2 * np.sin(theta2) + xN2 * np.cos(theta2)

    # Plot path of the needle tip
    # ax.plot(x_arr, y_arr, z_arr, label='Movement path')

    #print('xR=', xR)
    #print('yR=', yR)
    #print('zR=', zR)

    # Plot the needle
    # ax.plot(xR, yR, zR, label="Start position")
    # ax.plot(xR2, yR2, zR2, label="End postion")
    # ax.plot(xN, yN, zN)

    # ax.axes.set_zlim3d(bottom=0, top=150)
    # ax.axes.set_xlim3d(-50, 110)
    # ax.axes.set_ylim3d(0, 160)
    # ax.legend(loc='upper right')
    # ax.set_xlabel('$X-as$')
    # ax.set_ylabel('$Y-as$')
    # ax.set_zlabel('$Z-as$')
    # ax.view_init(20, 20)

    # projection of line on surface
    Px = np.linspace(-R, R, 50)
    Py = A * Px + B
    Pz = np.zeros(50)

    plt.plot(x_arr, z_arr)
    plt.show()
    x_arr = np.linspace(X1, X2, steps)
    return z_arr, x_arr


img = 'BME3.jpeg'
img2 = cv2.imread(img)
img = cv2.imread(img)
x, y, z = img.shape
img = cv2.resize(img, (int(y / 2), int(x / 2)))
x2, y2, z2 = img2.shape
img2 = cv2.resize(img, (int(y / 2), int(x / 2)))
x, y, z = img.shape
arrZ = np.array([])
arrX = np.array([])

cv2.createTrackbar("Insertion Point", "Trackbars", 0, x, nothing)
cv2.createTrackbar("Goal X", "Trackbars", 0, x, nothing)
cv2.createTrackbar("Goal Y", "Trackbars", 0, y, nothing)

while True:

    # Start reading the webcam feed frame by frame.
    frame = copy.deepcopy(img)
    frame2 = img2

    newX = cv2.getTrackbarPos("Insertion Point", "Trackbars")
    goalX = cv2.getTrackbarPos("Goal X", "Trackbars")
    goalY = cv2.getTrackbarPos("Goal Y", "Trackbars")
    frame = cv2.circle(frame, (0, newX), radius=5, color=(255, 0, 0), thickness=-1)
    frame = cv2.circle(frame, (goalY, goalX), radius=5, color=(0, 0, 255), thickness=-1)
    stacked = np.hstack((frame, frame2))
    cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.8, fy=0.8))

    # If the user presses ESC then exit the program
    key = cv2.waitKey(1)
    if key == 27:
        break

        #print(thearray)
        thearray = [newX,goalX, goalY]
    if key == ord('r'):
    # If the user presses `r` then print this array.

        # Also save this array as penval.npy
        np.save('Results', thearray)
    # If the user presses `s` then print this array.
    if key == ord('s'):
        #break
        steps = 15
        # For the graph goalY is the x and goalX is the y
        z_arr, x_arr = draw(goalY, (goalX - newX), steps)
        #print(np.array(z_arr) - 150)
        #print(x_arr)
        #print(newX)

        count = 1
        for val in np.array(z_arr) - 150:
            xV = int(val)
            frame2 = cv2.circle(frame2, (xV, int(x_arr[steps-count]) - 30), radius=10, color = (0, 255, 0), thickness=-1)
            count = count + 1
            arrX = np.append(arrX, int(x_arr[steps-count]))
            arrZ = np.array(z_arr) - 150
        thearray = [arrZ, arrX]
        # print(thearray)
        # Also save this array as penval.npy
        np.save('Results', thearray)

    frame = copy.deepcopy(img)
# Release the camera & destroy the windows.
cv2.destroyAllWindows()