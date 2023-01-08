import matplotlib.pyplot as plt
import numpy as np
plt.close()
fig = plt.figure(figsize=[10, 100])
plt.xlim(0, 1)
plt.ylim(-0.04, 0.1)
plt.xlabel('insertion depth [%]')
plt.ylabel('y direction[%]')
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

phantom_1 = [[0, 131, 279, 517, 713, 893, 1085, 1268, 1461], [0, 2, 4, 13, 26, 36, 55, 73, 95]]
phantom_2 = [[0, 119, 267, 418, 571, 727, 874, 1024, 1188, 1353, 1447], [0, -3, -3, -4, -6, -2, 0, 0, 2, 8, 8]]
phantom_3 = [[0, 141, 269, 424, 568, 720, 878, 1024, 1175, 1344], [0, -6, -8, -14, -14, -21, -28, -24, -20, -12]]
phantom_4 = [[0, 129, 274, 427, 570, 739, 892, 1054, 1211, 1313], [0, 0, -7, -9, -11, -10, -11, -11, -4, -4]]
phantom_5 = [[0, 158, 306, 453, 596, 733, 878, 1014, 1177, 1301], [0, -6, -10, -9, -13, -13, -5, 3, 10, 19]]
phantom_6 = [[0, 143, 288, 426, 575, 731, 890, 1047, 1208, 1304], [0, -3, -7, -13, -13, -10, -1, 8, 23, 32]]
total = [phantom_1, phantom_2, phantom_3, phantom_4, phantom_5, phantom_6]

xp = np.linspace(0, 1, 300)
count = 0
for i in total:
    count += 1
    lim = i[0][-1]
    i[0] = [i[0][j] / lim for j in range(len(i[0]))]
    i[1] = [i[1][j] / lim for j in range(len(i[1]))]
    print(i)
    coef = np.polyfit(i[0], i[1], 2)
    p = np.poly1d(coef)
    data = p(xp)
    data[0] = 0
    plt.plot(xp, data, label=f'phantom {count}')


#plt.show()
plt.savefig('40_degrees.png', bbox_inches='tight', pad_inches=0.05)
