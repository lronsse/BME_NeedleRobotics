#import Steedle_sercom
import copy

from Motor_controller import motor_controller
from pySerialTransfer import pySerialTransfer as txfer
import numpy as np
import cv2
import requests
import csv

Controller = motor_controller()

def run():
    print('Attempting connection')
    # link = Controller.open_ser_com()
    link = ''
    print('connected with {}'.format(link))
    x, y = Controller.Move_tip(10, 10)

def moveXY(x, y):
    x, y = Controller.Move_tip(x, y)
    return x, y

def moveZ(z):
    Current_X, Current_Y, X_coord, Y_coord = Controller.Insert(z)
    return 0

def nothing(x):
    pass

def calculateInsertion(frame):

    cv2.namedWindow("Trackbars")


    img2 = copy.deepcopy(frame)
    img = copy.deepcopy(frame)
    x, y, z = img.shape
    x2, y2, z2 = img2.shape
    x, y, z = img.shape
    arrZ = np.array([])
    arrX = np.array([])

    cv2.createTrackbar("X", "Trackbars", 0, x, nothing)
    cv2.createTrackbar("Y", "Trackbars", 0, y, nothing)
    while True:

        # Start reading the webcam feed frame by frame.
        frame = copy.deepcopy(img)
        frame2 = img2

        goalX = cv2.getTrackbarPos("X", "Trackbars")
        goalY = cv2.getTrackbarPos("Y", "Trackbars")
        frame = cv2.circle(frame, (goalY, goalX), radius=10, color=(0, 0, 255), thickness=-1)
        stacked = np.hstack((frame, frame2))
        cv2.imshow('Trackbars', frame)
        # cv2.imshow('Trackbars', stacked)

        # If the user presses ESC then exit the program
        key = cv2.waitKey(1)
        if key == 27:
            break

        # If the user presses `s` then print this array.
        if key == ord('s'):
            cv2.destroyAllWindows()
            return frame, goalX, goalY

        frame = copy.deepcopy(img)
    # Release the camera & destroy the windows.
    cv2.destroyAllWindows()

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

xV = 0
yV = 0
zV = 0
#link = Controller.Home()
link = Controller.get_link()

M1 = [0, 0]  # M1 = [28282, 3500]  # 1000 --> 4.5 mm
M2 = [0, 0]  # M2 = [28282, -2295]
M3 = [0, 0]  # M3 = [28282, 9690]  # 1000 --> 9.9
#send_arr(link, M1, M2, M3)

#Controller.getShit()

url = "http://145.94.170.3:8080/shot.jpg"

count = 0
gelatin = ''
xP = np.array([])
yP = np.array([])
xPr = np.array([])
yPr = np.array([])
xPm = np.array([])
yPm = np.array([])

while True:

    val = input('what value do you wish to change : ')

    if val == 'h':
        link = Controller.Home()

    if val == 'name':
        name = input(f'Enter test name')
        gelatin = name

    if val == 'xy':
        x, y = input(f'Enter x and y percentage : ').split()
        x, y = int(x), int(y)
        x, y = moveXY(x, y)
        print(f'Tip moved x by {x} and y by {y}')
        print('')

    if val == 'z':
        z = int(input(f'Enter z coordinate : '))
        zV += z
        moveZ(z)
        print(f'Moved Z by : {z}')

    if val == '1':
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        img, x, y = calculateInsertion(frame)
        xP = np.append(xP, x)
        yP = np.append(yP, y)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        #cv2.imshow('res', img)
        cv2.imwrite(f'images/{gelatin}_insertion{count}.jpg', img)

        with open('values.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow([f'{gelatin}_insertion_{count}', f'{x}', f'{y}'])
        count += 1

    if val == '2':
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        img, x, y = calculateInsertion(frame)
        xPr = np.append(xPr, x)
        yPr = np.append(yPr, y)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        #cv2.imshow('res', img)
        cv2.imwrite(f'images/{gelatin}_zero_{count-1}.jpg', img)

        with open('values.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow([f'{gelatin}_zero_{count-1}', f'{x}', f'{y}'])

    if val == '3':
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        img, x, y = calculateInsertion(frame)
        xPm = np.append(xPm, x)
        yPm = np.append(yPm, y)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        #cv2.imshow('res', img)
        cv2.imwrite(f'images/{gelatin}_retraction_{count-1}.jpg', img)

        with open('values.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow([f'{gelatin}_retraction_{count-1}', f'{x}', f'{y}'])

    if val == 's':
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        img, x, y = calculateInsertion(frame)
        xPm = np.append(xPm, x)
        yPm = np.append(yPm, y)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        #cv2.imshow('res', img)
        cv2.imwrite(f'images/{gelatin}.jpg', img)

        with open('values.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow([f'{gelatin}', f'{x}', f'{y}'])

    if val == 'c':
        im1, im2 = input(f'Which two images do you want to compare? write their number').split()
        im1, im2 = int(im1), int(im2)
        resV = np.sqrt((xP[im2] - xP[im1])**2 + (yP[im2] - yP[im1])**2)
        print(f'error is {resV}')
