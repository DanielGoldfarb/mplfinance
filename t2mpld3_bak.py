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

ax.plot(x,y,linewidth=3)
#plt.plot(x,y)
#plt.show()
mpld3.show()

##    ##  plt.plot([3,1,4,1,5])
##    ##  mpld3.show()
##    x = np.arange(0.0,1.0,0.05)
##    y = np.sin(2*np.pi*x)
##    
##    # fig = mpl.figure.Figure()

#---  fig = plt.figure(figsize=(10,15))
#---  ax = fig.add_axes([0.15, 0.1, 0.7, 0.3])

##    ax.plot(x,y)
##    plt.figure(fig)
##    mpld3.show()

#mpld3.show()
#mpld3.save_html(fig,'testmpld3.html')
