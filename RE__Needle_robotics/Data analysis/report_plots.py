import matplotlib.pyplot as plt
import numpy as np
plt.close()
fig = plt.figure(figsize=[10, 100])
plt.xlim(0, 1)
plt.ylim(0, 0.2)
plt.xlabel('insertion depth [%]')
plt.ylabel('y direction[%]')
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

phantom_1 = [[0, 133, 271, 417, 573, 709, 861, 1019, 1173, 1327, 1457], [0, 2, 11, 25, 54, 74, 100, 130, 162, 195, 226]]
phantom_2 = [[0, 167, 336, 513, 703, 880, 1080, 1265, 1421], [0, 6, 18, 40, 69, 100, 143, 182, 221]]
phantom_3 = [[0, 229, 447, 654, 860, 1064, 1228, 1494], [0, 5, 17, 38, 66, 103, 137, 198]]
phantom_4 = [[0, 180, 357, 541, 690, 854, 1003, 1153, 1370], [0, 6, 21, 43, 68, 99, 132, 167, 223]]
phantom_5 = [[0, 134, 275, 427, 571, 720, 888, 1063, 1256, 1356], [0, -3, -5, -5, -1, 6, 22, 45, 72, 86]]
phantom_6 = [[0, 153, 340, 493, 656, 826, 967, 1125, 1232], [0, 0, 2, 11, 25, 47, 67, 91, 113]]
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

plt.legend()
plt.show()
#plt.savefig('80_degrees.png', bbox_inches='tight', pad_inches=0.05)