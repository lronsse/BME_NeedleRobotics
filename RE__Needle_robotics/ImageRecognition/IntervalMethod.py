import numpy as np
# from Motor_controller import motor_controller

with np.load('Results.npy') as data:
    a = data['a']

print(a)
