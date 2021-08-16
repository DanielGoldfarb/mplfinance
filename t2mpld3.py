import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import mpld3

import pandas as pd
import mplfinance as mpf

x  = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
xr = np.array([ i*.05 for i in range(24)])
y = np.sin(2*np.pi*xr)
#y = np.random.randint(100, size=x.shape)

plt.rcParams['font.size'] *= 1.0

fig = plt.figure()
fig.set_size_inches((6.,4.))

ax = fig.add_axes( [0.1, 0.1, 0.9, 0.9] )
ax.tick_params(axis='x',rotation=30)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set_facecolor('lightcyan')

ax1 = ax.twinx()
ax1.grid(False)
ax.set_axisbelow(True)

ax.plot(x,y,linewidth=3)
#plt.plot(x,y)
#plt.show()
mpld3.show()
