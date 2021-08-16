#!/usr/bin/env python
# coding: utf-8

# ---------------------
# Text on Plot Example:
# ---------------------

import pandas as pd
import mplfinance as mpf

# Read in the Data:
intraday = pd.read_csv('../data/SP500_NOV2019_IDay.csv',index_col=0,parse_dates=True)
intraday = intraday.drop('Volume',axis=1) # Volume is zero anyway for this intraday data set
intraday = intraday.loc['2019-11-07 09:30':'2019-11-08 16:00',:] # only need part of the data.

# Resample, to every 5 minutes:
rmap = {'Open':'first', 'High':'max', 'Low':'min', 'Close':'last'}
df5m = intraday.resample( '5T').agg(rmap).dropna()

print('len(df5m)=',len(df5m))

fig, axlist = mpf.plot(df5m,type='candle',mav=(10,30),style='yahoo',figscale=1.5,
                       title='\nPlot Title',ylabel='5 Minute Prices', returnfig=True)

axlist[0].text(len(df5m)-30, 3095, 'This text is in\nthe Upper Right\ncorner.')
axlist[0].text(          10, 3075, 'This text is in\nthe Lower Left\ncorner.')

fig.savefig('df5m.png')
