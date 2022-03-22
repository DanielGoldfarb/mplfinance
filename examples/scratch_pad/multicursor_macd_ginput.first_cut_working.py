import pandas as pd
import mplfinance as mpf
from matplotlib.widgets import MultiCursor
from matplotlib.collections import LineCollection

idf = pd.read_csv('../data/SPY_20110701_20120630_Bollinger.csv',index_col=0,parse_dates=True)
df  = idf.loc['2011-07-01':'2011-12-30',:]


exp12 = df['Close'].ewm(span=12, adjust=False).mean()
exp26 = df['Close'].ewm(span=26, adjust=False).mean()

macd = exp12 - exp26

signal    = macd.ewm(span=9, adjust=False).mean()
histogram = macd - signal

apds = [mpf.make_addplot(exp12,color='lime'),
        mpf.make_addplot(exp26,color='c'),
        mpf.make_addplot(histogram,type='bar',width=0.7,panel=1,
                         color='dimgray',alpha=1,secondary_y=False),
        mpf.make_addplot(macd,panel=1,color='fuchsia',secondary_y=True),
        mpf.make_addplot(signal,panel=1,color='b',secondary_y=True),
       ]

# For some reason, which i have yet to determine, MultiCursor somehow
# causes ymin to be set to zero for the main candlestick Axes, but we
# can correct that problem by passing in specific values:
ymin = min(df['Low'])  * 0.98
ymax = max(df['High']) * 1.02

fig, axlist = mpf.plot(df,type='candle',addplot=apds,figscale=1.1,figratio=(8,5),title='\nMACD', ylim=(ymin,ymax),
                       style='blueskies',volume=True,volume_panel=2,panel_ratios=(6,3,2),returnfig=True)

multi = MultiCursor(fig.canvas, axlist, horizOn=True, vertOn=True, color='r', lw=1.2)

p1p2 = fig.ginput(2)

p1 = p1p2[0]
p2 = p1p2[1]

print('p1p2=',p1p2)
print('p1=',p1,'p2=',p2)

d1 = df.index[ round(p1[0]) ]
d2 = df.index[ round(p2[0]) ]

print('d1=',d1,'d2=',d2)

aline = [(d1,p1[1]),(d2,p2[1])]

fig, axlist = mpf.plot(df,type='candle',addplot=apds,figscale=1.1,figratio=(8,5),title='\nMACD', ylim=(ymin,ymax),
                       alines=aline,
                       style='blueskies',volume=True,volume_panel=2,panel_ratios=(6,3,2),returnfig=True)

multi = MultiCursor(fig.canvas, axlist, horizOn=True, vertOn=True, color='r', lw=1.2)

mpf.show()
