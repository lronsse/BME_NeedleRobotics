import numpy as np
import matplotlib.pyplot as plt
import time
from pySerialTransfer import pySerialTransfer as txfer


def draw(newX, newY, steps):
    # Variable set up
    I = 10  # The centre of the circle measured from the template
    K = 150  # Radius of circle
    K = newX + 150
    X1 = 30  # Start X-coordinate
    Y1 = 30  # Start Y-coodrinate

    X2 = newY  # End X-coordinate
    Y2 = newX  # End Y-coordinate

    datasets = []  # Array of arrays containing all the x and y point for every height
    z2 = []
    x2 = []
    y2 = []

    steps = steps  # Determines the precision of the visualization

    A = (Y2 - Y1) / (X2 - X1)  # Directional coefficient of path
    B = Y1 - A * X1  # Intersection point with y-axis

    R_arr = np.linspace(1, 120, 40)

    # Projection of movement space of needle tip
    for i in range(len(R_arr)):
        x_cont = np.linspace(-R_arr[i], R_arr[i], 100)
        y_cont = np.sqrt(R_arr[i] ** 2 - x_cont ** 2)
        z = np.sqrt(K ** 2 - R_arr[i] ** 2)
        datasets.append([x_cont, y_cont, z])

    x_arr = np.linspace(X1, X2, steps)
    y_arr = []
    z_arr = []

    # Display movement path of needle tip
    for i in range(len(x_arr)):
        y_arr.append(A * x_arr[i] + B)
        R = np.sqrt(x_arr[i] ** 2 + y_arr[i] ** 2)
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

    # projection of line on surface
    Px = np.linspace(-R, R, 50)
    Py = A * Px + B
    Pz = np.zeros(50)
    x_arr = np.linspace(X1, X2, steps)
    return z_arr, x_arr

def open_ser_com():
    try:
        link = txfer.SerialTransfer('COM8')

        link.open()
        time.sleep(2)  # allow some time for the Arduino to completely reset
        print('link = open')

        return link

    except:
        import traceback
        traceback.print_exc()

        try:
            link.close()

        except:
            pass

def send_arr(link, step_count_M1, step_count_M2, step_count_M3):
    list_of_lists = [step_count_M1, step_count_M2, step_count_M3]

    length = len(list_of_lists)

    for i in range(length):
        send_size = 0

        ###################################################################
        # Send lists
        ###################################################################

        list_ = list_of_lists[i]

        list_size = link.tx_obj(list_)
        send_size += list_size

        ###################################################################
        # Transmit all the data to send in a single packet
        ###################################################################
        link.send(send_size)

        ###################################################################
        # Wait for a response and report any errors while receiving packets
        ###################################################################
        while not link.available():
            if link.status < 0:
                if link.status == txfer.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif link.status == txfer.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif link.status == txfer.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(link.status))

        ###################################################################
        # Parse response list
        ###################################################################
        rec_list = link.rx_obj(obj_type=type(list_),
                               obj_byte_size=list_size,
                               list_format='i')
        """"       
        rec_list_M2  = link.rx_obj(obj_type=type(list_M2),
                                         obj_byte_size=list_size_M2,
                                         list_format='i')

        rec_list_M4  = link.rx_obj(obj_type=type(list_M4),
                                         obj_byte_size=list_size_M4,
                                         list_format='i')

        """

        ###################################################################
        # Display the received data
        ###################################################################
        # print('SENT: {}'.format(list_))
        # print('RCVD: {}'.format(rec_list))
        # print(' ')

link = open_ser_com()


# Variable set up
I = 20  # The centre of the circle measured from the template
K_0 = 171
D_max = 100  # Maximum deflection

C1 = 3200  # 1/16 step mode
C2 = 3200  # 1/16 step mode
C3 = 3200  # 1/16 step mode

datasets = []  # Array of arrays containing all the x and y point for every hight
z2 = []
x2 = []
y2 = []

steps = 30  # Determines the precision of the movement
straight = 50  # Point where maximum deflection is no longer determined by mechanical limit

corner = np.arctan(D_max / straight)






# coordinates = input('input x, y coordinates : ').split()
# coordinates = map(int, coordinates)
coordinates = [0, 311, 600]
# newX = 0
steps = 15
newX, goalX, goalY = coordinates
# For the graph goalY is the x and goalX is the y
x_arr, z_arr = draw(goalY, (goalX - newX), steps)
print(z_arr, '\n', x_arr)
