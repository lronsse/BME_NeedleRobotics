import numpy as np
import matplotlib.pyplot as plt

#
#  80 degree stuff
#
'''
N = 6
ind = np.arange(N)
width = 0.25

xvals = [3.937788267,	2.18627184,	0.230727949,	0.11841394,	0.095302741,	0.073650423]
bar1 = plt.bar(ind, xvals, width, color='b')

yvals = [0,	0,	0.735738404,	0.147690864,	0.072751118,	0.127971821]
bar2 = plt.bar(ind + width, yvals, width, color='lime')

#zvals = [11, 12, 13]
#bar3 = plt.bar(ind + width * 2, zvals, width, color='b')

plt.xlabel("Phantoms")
plt.ylabel('Error (mm)')
plt.title("Errors for 80 degrees")

plt.xticks(ind + width, ['Phantom 1', 'Phantom 2', 'Phantom 3', 'Phantom 4', 'Phantom 5', 'Phantom 6'])
plt.legend((bar1, bar2), ('Error type 1', 'Error type 3'))
plt.savefig('80_degrees_error.png', bbox_inches='tight', pad_inches=0.05)'''


#
#  40 degree stuff
#

N = 6
ind = np.arange(N)
width = 0.25

xvals = [0.202316223,	0.090433069,	0.05777731,	0.066571459,	0.076370423,	0.062620084]
bar1 = plt.bar(ind, xvals, width, color='b')

yvals = [0,	0,	0,	0.426104748,	0.149388773,	0.082550873]
bar2 = plt.bar(ind + width, yvals, width, color='lime')

#zvals = [11, 12, 13]
#bar3 = plt.bar(ind + width * 2, zvals, width, color='b')

plt.xlabel("Phantoms")
plt.ylabel('Error (mm)')
plt.title("Errors for 40 degrees")

plt.xticks(ind + width, ['Phantom 1', 'Phantom 2', 'Phantom 3', 'Phantom 4', 'Phantom 5', 'Phantom 6'])
plt.legend((bar1, bar2), ('Error type 1', 'Error type 3'))
plt.savefig('40_degrees_error.png', bbox_inches='tight', pad_inches=0.05)
