#import Steedle_sercom
from Motor_controller import motor_controller

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

xV = 0
yV = 0
zV = 0

print('Homing')
Controller.Home()
print('We have homed')

'''
while True:
    val = input('what value do you wish to change')
    if val == 'xy':
        x, y = input(f'Enter x and y coordinate : ').split()
        x, y = int(x), int(y)
        xV += x
        yV += y
        x, y = moveXY(x, y)
        print(f'Moved x by {x} and y by {y}')
        print('')
    if val == 'z':
        z = int(input(f'Enter z coordinate'))
        zV += z
        moveZ(z)
        print(f'Moved Z by : {z}')
    if val == 's':
        break
'''