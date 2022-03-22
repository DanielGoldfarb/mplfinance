import matplotlib.pyplot as plt
import matplotlib.figure as figure
import math

fig = plt.figure()
#fig = figure.Figure()

ax = fig.add_axes([0.1,0.1,0.8,0.8])

X = [ 0.05*x for x in range(1,40) ]
Y = [ 1.0*math.sin(4*x) for x in X ]

ax.plot(X,Y,linewidth=4.0,color='k',linestyle=':')

ax.pie([1,2,3,4], radius=0.75, center=(1,0), frame=True,
       wedgeprops=dict(edgecolor='k',alpha=0.75))

plt.show()
