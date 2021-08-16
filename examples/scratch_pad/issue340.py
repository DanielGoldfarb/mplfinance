import matplotlib.pyplot as plt
import math


# x = [ x*0.01 for x in range(2000) ]

x = [ x*0.05 for x in range(400) ]

y = [ math.sin(x) for x in x ]

yr = [ float('nan') if y <= -0.025 else y for y in y ]

yb = [ float('nan') if y >=  0.025 else y for y in y ]

fig = plt.figure()

ax  = fig.add_subplot()

ax.plot(x,yr,color='r')
ax.plot(x,yb,color='b')

plt.show()
