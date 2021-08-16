import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import mpld3

import pandas as pd
import mplfinance as mpf

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

df = pd.read_csv('examples/data/SP500_NOV2019_Hist.csv',index_col=0,parse_dates=True)
fig, axlist = mpf.plot(df,type='candle',returnfig=True,show_nontrading=True)

#plt.figure(fig)

mpld3.show()
#mpld3.save_html(fig,'testmpld3.html')
