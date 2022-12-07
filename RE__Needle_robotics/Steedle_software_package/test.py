#import Steedle_sercom
from Motor_controller import motor_controller
from pySerialTransfer import pySerialTransfer as txfer

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
print('We have the link')

M1 = [0, 0]  # M1 = [28282, 3500]
M2 = [0, 0]  # M2 = [28282, -2295]
M3 = [0, 0]  # M3 = [28282, 9690]
send_arr(link, M1, M2, M3)
print("array sent")

#Controller.getShit()

while True:
    val = input('what value do you wish to change : ')
    if val == 'xy':
        x, y = input(f'Enter x and y coordinate : ').split()
        x, y = int(x), int(y)
        x, y = moveXY(x, y)
        print(f'Tip moved x by {x} and y by {y}')
        print('')
    if val == 'z':
        z = int(input(f'Enter z coordinate : '))
        zV += z
        moveZ(z)
        print(f'Moved Z by : {z}')
    if val == 's':
        break
    if val == 'r':
        while True:
            c = input('key : ')
            if c == '1':
                M2[1] += 10
                send_arr(link, [0, 0], M2, [0, 0])
                print(M2)
            if c == '2':
                M2[1] -= 10
                send_arr(link, M1, M2, M3)
                print(M2)
            else:
                break
