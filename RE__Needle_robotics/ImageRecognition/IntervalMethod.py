import numpy as np
import matplotlib.pyplot as plt


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


coordinates = input('input x, y coordinates : ').split()
print(coordinates)
newX = 0
steps = 15
goalX, goalY = coordinates
# For the graph goalY is the x and goalX is the y
z_arr, x_arr = draw(goalY, (goalX - newX), steps)

curve = np.load('Results.npy')
print(curve)
x, y = (530, 280)

