import matplotlib.pyplot as plt
import numpy as np
plt.close()
fig = plt.figure(figsize=[10, 100])
plt.xlim(0, 1)
plt.ylim(0, 0.2)
plt.xlabel('Insertion depth [%]')
plt.ylabel('Y direction[%]')
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

phantom_1 = [[0, 131, 279, 517, 713, 893, 1085, 1268, 1461], [0, 2, 4, 13, 26, 36, 55, 73, 95]]
phantom_2 = [[0, 119, 267, 418, 571, 727, 874, 1024, 1188, 1353, 1447], [0, -3, -3, -4, -6, -2, 0, 0, 2, 8, 8]]
phantom_3 = [[0, 141, 269, 424, 568, 720, 878, 1024, 1175, 1344], [0, -6, -8, -14, -14, -21, -28, -24, -20, -12]]
phantom_4 = [[0, 129, 274, 427, 570, 739, 892, 1054, 1211, 1313], [0, 0, -7, -9, -11, -10, -11, -11, -4, -4]]
phantom_5 = [[0, 158, 306, 453, 596, 733, 878, 1014, 1177, 1301], [0, -6, -10, -9, -13, -13, -5, 3, 10, 19]]
phantom_6 = [[0, 143, 288, 426, 575, 731, 890, 1047, 1208, 1304], [0, -3, -7, -13, -13, -10, -1, 8, 23, 32]]
total = [phantom_1, phantom_2, phantom_3, phantom_4, phantom_5, phantom_6]

Phantom_1 = [[0, 133, 271, 417, 573, 709, 861, 1019, 1173, 1327, 1457], [0, 2, 11, 25, 54, 74, 100, 130, 162, 195, 226]]
Phantom_2 = [[0, 167, 336, 513, 703, 880, 1080, 1265, 1421], [0, 6, 18, 40, 69, 100, 143, 182, 221]]
Phantom_3 = [[0, 229, 447, 654, 860, 1064, 1228, 1494], [0, 5, 17, 38, 66, 103, 137, 198]]
Phantom_4 = [[0, 180, 357, 541, 690, 854, 1003, 1153, 1370], [0, 6, 21, 43, 68, 99, 132, 167, 223]]
Phantom_5 = [[0, 134, 275, 427, 571, 720, 888, 1063, 1256, 1356], [0, -3, -5, -5, -1, 6, 22, 45, 72, 86]]
Phantom_6 = [[0, 153, 340, 493, 656, 826, 967, 1125, 1232], [0, 0, 2, 11, 25, 47, 67, 91, 113]]
Total = [Phantom_1, Phantom_2, Phantom_3, Phantom_4, Phantom_5, Phantom_6]

xp = np.linspace(0, 1, 300)
count = 0
for i in Total:
    count += 1
    lim = i[0][-1]
    i[0] = [i[0][j] / lim for j in range(len(i[0]))]
    i[1] = [i[1][j] / lim for j in range(len(i[1]))]
    print(i)
    coef = np.polyfit(i[0], i[1], 2)
    p = np.poly1d(coef)
    data = p(xp)
    data[0] = 0
    plt.plot(xp, data, label=f'Phantom {count}')

plt.legend()
#plt.show()
plt.savefig('80_degrees.png', bbox_inches='tight', pad_inches=0.05)
