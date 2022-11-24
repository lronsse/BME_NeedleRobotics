# -*- coding: utf-8 -*-
"""
Created on Fri May  7 09:40:35 2021

@author: Rolf
"""

import time
from pySerialTransfer import pySerialTransfer as txfer
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np


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

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


class motor_controller(object):
    def __init__(self):
        self.K_pos = K_0  # Radius of circle
        self.Z_pos = K_0
        self.X_pos = 0
        self.Y_pos = 0
        self.theta = 0
        self.round_counter = 0

    def close_connection(self):
        link.close()

    def Home(self):
        print('starting homing')
        step_count_M1 = [28282, 2600]
        step_count_M2 = [28282, -2195]
        step_count_M3 = [28282, 9570]

        self.K_pos = K_0  # Radius of circle
        self.Z_pos = K_0
        self.X_pos = 0
        self.Y_pos = 0
        self.theta = 0
        self.round_counter = 0

        send_arr(link, step_count_M1, step_count_M2, step_count_M3)
        print('done homing, array sent')

    def Move_tip(self, X, Y):
        if self.K_pos > np.sqrt(D_max ** 2 + straight ** 2):
            R_max = D_max
        else:
            # R_max = -1*(self.K_pos - I)/((-I + K_0)/-D_max)    # Line representing the maximum deflection at every z value
            R_max = np.sin(corner) * self.K_pos

        X_coord = 0.01 * X * R_max
        Y_coord = 0.01 * Y * R_max

        print('X_coord, Y_coord', X_coord, Y_coord, self.K_pos)

        if X_coord != 0:  # Check if x is 0
            theta_end = np.arctan(Y_coord / X_coord)
            if X_coord < 0:  # Check if tip is in second or third quadrant
                theta_end = np.pi + theta_end
            elif Y_coord < 0 and theta_end < 0:  # Check if tip is in fourth quadrant
                theta_end = 2 * np.pi + theta_end
            else:
                theta_end = self.theta

        else:
            if Y_coord > 0:
                theta_end = 0.5 * np.pi
            elif Y_coord < 0:
                theta_end = 1.5 * np.pi
            else:
                theta_end = self.theta

        # Projected on the x-y plane the tip of the needle follows a path
        # characterized by the equation y= Ax + B the coëfficient A and B can be found
        # through the following equations.

        if round(X_coord, 6) != round(self.X_pos, 6):  # Checking for a vertical line
            A = (Y_coord - self.Y_pos) / (X_coord - self.X_pos)  # Directional coefficient of path
            B = self.Y_pos - A * self.X_pos  # Intersection point with y-axis

            x_arr, y_arr, z_arr, R_arr, theta_arr = self.Non_vertical_line(A, B, X_coord, Y_coord)

        else:
            x_arr, y_arr, z_arr, R_arr, theta_arr = self.vertical_line(X_coord, Y_coord)

        step_count_M1 = []
        step_count_M2 = []
        step_count_M3 = []

        Z_steps = []
        theta_steps = []
        R_steps = []

        print('x_arr=', x_arr, '\n')
        print('y_arr=', y_arr, '\n')
        print('R_arr=', R_arr, '\n')
        print('Theta_arr=', theta_arr, '\n')
        print('z_arr=', z_arr, '\n')

        # Convert positions of needle tip path to Motor positions
        for i in range(steps):
            Z_steps.append(int(round((z_arr[i] - z_arr[0]) / (32 / C1))))
            theta_steps.append(int(round(-1 * (theta_arr[i] - theta_arr[0]) / ((2 * np.pi / C2) * (16 / 100)))))
            R_steps.append(int(round(-1 * (R_arr[i] - R_arr[0]) / (32 / C3))))

            if i > 0:
                step_count_M1.append(-1 * (Z_steps[i] - Z_steps[i - 1]))
                step_count_M2.append(theta_steps[i] - theta_steps[i - 1])
                step_count_M3.append(R_steps[i] - R_steps[i - 1])

        send_arr(link, step_count_M1, step_count_M2, step_count_M3)

        """
        ar = np.linspace(1,120, 40)
        
        #Projection of movement space of needle tip
        for i in range(len(ar)):
            x_cont = np.linspace( -ar[i], ar[i], 100)       
            y_cont = np.sqrt(ar[i]**2 - x_cont**2)
            z = np.sqrt(self.K_pos**2 - ar[i]**2)
            
            ax.plot( x_cont, y_cont, z, color='grey')
        
        ax.plot( x_arr, y_arr, z_arr, label='Movement path')
        #ax.axes.set_xlim3d(0, 150)
        #ax.axes.set_ylim3d(0, 150)
        ax.axes.set_zlim3d(0, 150)
        ax.legend(loc='lower right') 
        ax.set_xlabel('$X-as$')
        ax.set_ylabel('$Y-as$')
        ax.set_zlabel('$Z-as$')
        ax.view_init( 90, -90)
             
        print('x_arr=', x_arr, '\n')
        print('y_arr=', y_arr, '\n')
        print('R_arr=', R_arr, '\n')
        print('Theta_arr=', theta_arr, '\n')
        print('z_arr=', z_arr, '\n')
        
        #print('Z_steps=', Z_steps, '\n')
        #print('Theta_steps=', theta_steps, '\n')
        #print('R_steps=', R_steps, '\n')
        
        print('M1_arr=', step_count_M1, '\n')
        print('M2_arr=', step_count_M2, '\n')
        print('M3_arr=', step_count_M3, '\n')
        """

        # Update position
        self.X_pos = X_coord
        self.Y_pos = Y_coord
        self.Z_pos = z_arr[steps - 1]

        return X_coord, Y_coord

    def Insert(self, depth):
        R_start = np.sqrt(self.X_pos ** 2 + self.Y_pos ** 2)
        Z_start = np.sqrt(self.K_pos ** 2 - R_start ** 2)
        Q = Z_start

        if self.X_pos != 0:  # Check if x is 0
            theta = np.arctan(self.Y_pos / self.X_pos)
            if self.X_pos < 0:  # Check if tip is in second or third quadrant
                theta = np.pi + theta
            elif self.Y_pos < 0 and theta < 0:  # Check if tip is in fourth quadrant
                theta = 2 * np.pi + theta
            else:
                theta = self.theta

        else:
            if self.Y_pos > 0:
                theta = 0.5 * np.pi
            elif self.Y_pos < 0:
                theta = 1.5 * np.pi
            else:
                theta = self.theta

        zN = np.linspace(Z_start - depth, Z_start, steps)
        yN = R_start / (Q ** 2) * zN ** 2  # Re_arr
        xN = np.zeros(steps)

        # Rotating the needle curve in the right configuration in 3 dimensional space
        zR = zN
        xR = yN * np.cos(theta) - xN * np.sin(theta)
        yR = yN * np.sin(theta) + xN * np.cos(theta)

        z_arr_ins = []  # Array with all the z positions of the needle tip
        R_arr_ins = []  # Array of all radi
        theta_arr_ins = []  # Array of all the theta angles

        # Calculating the motor positions
        # zR is given from the end of the insertion to the begining
        # Therefore this array needs to be flipped so that it start at the beginning

        for i in range(len(zR)):
            z_arr_ins.append(zR[len(zR) - i - 1])
            R_arr_ins.append(np.sqrt(xR[len(zR) - i - 1] ** 2 + yR[len(zR) - i - 1] ** 2))

            if xR[len(zR) - i - 1] == 0:
                theta_arr_ins.append(0)
            else:
                theta_arr_ins.append(np.arctan(yR[len(zR) - i - 1] / xR[len(zR) - i - 1]))

        step_count_M1 = []
        step_count_M2 = []
        step_count_M3 = []

        Z_steps = []
        theta_steps = []
        R_steps = []

        # Check if the insertion doesn't cause to much bending:
        Check_K = np.sqrt(zR[0] ** 2 + (xR[0] ** 2 + yR[0] ** 2))
        if Check_K > np.sqrt(D_max ** 2 + straight ** 2):
            Current_Rmax = D_max
        else:
            Current_Rmax = np.sin(corner) * Check_K

        X_perc = int(round(xR[0] / Current_Rmax * 100))
        Y_perc = int(round(yR[0] / Current_Rmax * 100))

        if X_perc > 100 or Y_perc > 100:
            return 'To much', 'To much', 'To much', 'To much'

        else:
            """
            #Convert positions of needle tip path to Motor positions
            for i in range(len(zR) - 1):
                step_count_M1.append(int(round((z_arr_ins[i+1] - z_arr_ins[i])/(32/C3))))          
                step_count_M2.append(int(round(-1*(theta_arr_ins[i+1] - theta_arr_ins[i])/((2*np.pi/C2)*(16/100)))))
                step_count_M3.append(int(round(-1*(R_arr_ins[i+1] - R_arr_ins[i])/(32/C1))))
            """
            # Convert positions of needle tip path to Motor positions
            for i in range(steps):
                Z_steps.append(int(round((z_arr_ins[i] - z_arr_ins[0]) / (32 / C1))))
                theta_steps.append(
                    int(round(-1 * (theta_arr_ins[i] - theta_arr_ins[0]) / ((2 * np.pi / C2) * (16 / 100)))))
                R_steps.append(int(round(-1 * (R_arr_ins[i] - R_arr_ins[0]) / (32 / C3))))

                if i > 0:
                    step_count_M1.append(-1 * (Z_steps[i] - Z_steps[i - 1]))
                    step_count_M2.append(theta_steps[i] - theta_steps[i - 1])
                    step_count_M3.append(R_steps[i] - R_steps[i - 1])

            send_arr(link, step_count_M1, step_count_M2, step_count_M3)

            # Update position
            self.X_pos = xR[0]
            self.Y_pos = yR[0]
            self.Z_pos = zR[0]
            self.K_pos = np.sqrt(self.Z_pos ** 2 + (self.X_pos ** 2 + self.Y_pos ** 2))

            # Update bending percentages
            if self.K_pos > np.sqrt(D_max ** 2 + straight ** 2):
                Current_Rmax = D_max
            else:
                # Current_Rmax = -1*(self.K_pos - I)/((-I + K_0)/-D_max)    # Line representing the maximum deflection at every z value
                # Current_Rmax = D_max/straight *self.K_pos
                Current_Rmax = np.sin(corner) * self.K_pos

            X_perc = int(round(self.X_pos / Current_Rmax * 100))
            Y_perc = int(round(self.Y_pos / Current_Rmax * 100))

            print('R_max', Current_Rmax)
            print('x_arr=', xR, '\n')
            print('y_arr=', yR, '\n')
            print('z_arr=', zR, '\n')

            return X_perc, Y_perc, self.X_pos, self.Y_pos

        """
        print('x_arr=', xR, '\n')
        print('y_arr=', yR, '\n')
        
        print('R_arr_ins=', R_arr_ins, '\n')
        print('Theta_arr_ins=', theta_arr_ins, '\n')
        print('z_arr_ins=', z_arr_ins, '\n')
        
        
        #Plot the needle
        ax.plot(xR, yR, zR, label="Insertion path")
        
        R_arr = np.linspace(1,120, 40)

        #Projection of movement space of needle tip
        for i in range(len(R_arr)):
            x_cont = np.linspace( -R_arr[i], R_arr[i], 100)       
            y_cont = np.sqrt(R_arr[i]**2 - x_cont**2)
            z = np.sqrt(self.K_pos**2 - R_arr[i]**2)
            
            ax.plot( x_cont, y_cont, z, color='grey')
        
        ax.axes.set_xlim3d(0, 150)
        ax.axes.set_ylim3d(0, 150)
        ax.axes.set_zlim3d(0, 150)
        ax.legend(loc='upper right') 
        ax.set_xlabel('$X-as$')
        ax.set_ylabel('$Y-as$')
        ax.set_zlabel('$Z-as$')
        ax.view_init( 20, 20)
        """

    def Non_vertical_line(self, A, B, X_coord, Y_coord):
        x_arr = np.linspace(self.X_pos, X_coord, steps)  # Array with all the x positions of the needle tip
        y_arr = []  # Array with all the y positions of the needle tip
        z_arr = []  # Array with all the z positions of the needle tip
        R_arr = []  # Array of all radi
        theta_arr = []  # Array of all the theta angles

        # Get positions of needle tip path
        for i in range(len(x_arr)):
            y_arr.append(A * x_arr[i] + B)
            R_arr.append(np.sqrt(x_arr[i] ** 2 + y_arr[i] ** 2))
            z_arr.append(np.sqrt(self.K_pos ** 2 - R_arr[i] ** 2))

            if (y_arr[i] * y_arr[i - 1]) <= 0 and x_arr[i] > 0 and i > 0 and y_arr[0] != 0:
                if y_arr[i] <= y_arr[i - 1]:
                    self.round_counter -= 1
                else:
                    self.round_counter += 1

            if x_arr[i] != 0:  # Check if x is 0
                self.theta = np.arctan(y_arr[i] / x_arr[i]) + 2 * np.pi * self.round_counter
                if x_arr[i] < 0:  # Check if tip is in second or third quadrant
                    self.theta = np.pi + self.theta
                    theta_arr.append(self.theta)
                elif y_arr[i] < 0 and self.theta < 0:  # Check if tip is in fourth quadrant
                    self.theta = 2 * np.pi + self.theta
                    theta_arr.append(self.theta)
                else:  # Check if tip is in first quadrant
                    theta_arr.append(self.theta)
            else:
                if round(y_arr[i], 6) > 0:
                    self.theta = 0.5 * np.pi + 2 * np.pi * self.round_counter
                    theta_arr.append(self.theta)
                elif round(y_arr[i], 6) < 0:
                    self.theta = 1.5 * np.pi + 2 * np.pi * self.round_counter
                    theta_arr.append(self.theta)
                else:
                    self.theta = 0
                    theta_arr.append(self.theta)

        return x_arr, y_arr, z_arr, R_arr, theta_arr

    def vertical_line(self, X_coord, Y_coord):
        x_arr = []  # Array with all the x positions of the needle tip
        y_arr = np.linspace(self.Y_pos, Y_coord, steps)  # Array with all the y positions of the needle tip
        z_arr = []  # Array with all the z positions of the needle tip
        R_arr = []  # Array of all radi
        theta_arr = []

        # Get positions of needle tip path
        for i in range(len(y_arr)):
            x_arr.append(self.X_pos)
            R_arr.append(np.sqrt(x_arr[i] ** 2 + y_arr[i] ** 2))
            z_arr.append(np.sqrt(self.K_pos ** 2 - R_arr[i] ** 2))
            if x_arr[i] != 0:
                theta_arr.append(np.arctan(y_arr[i] / x_arr[i]))
            else:
                if y_arr[i] == 0:
                    self.theta = 0
                    theta_arr.append(self.theta)
                elif y_arr[i] > 0:
                    self.theta = 0.5 * np.pi
                    theta_arr.append(self.theta)
                else:
                    self.theta = -0.5 * np.pi
                    theta_arr.append(self.theta)

        return x_arr, y_arr, z_arr, R_arr, theta_arr
