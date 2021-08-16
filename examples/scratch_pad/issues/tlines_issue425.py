import yfinance as yf
import pandas as pd
import mplfinance as mpf

#tickername = "AMC"
#Ticker = yf.Ticker(tickername)
#df = Ticker.history(period='1d', interval='1m', start='2021-07-22', end='2021-07-28')

df = pd.read_csv('AMC_20210722_20210728.csv',index_col=0,parse_dates=True)

print()
print(df.head())
print()
print(df.tail())
print()

datapairs = [('2021-07-22 09:38:00-04:00', '2021-07-22 09:58:00-04:00'), ('2021-07-22 09:58:00-04:00', '2021-07-22 10:02:00-04:00'), ('2021-07-22 10:02:00-04:00', '2021-07-22 10:15:00-04:00'), ('2021-07-22 10:15:00-04:00', '2021-07-22 10:24:00-04:00'), ('2021-07-22 10:24:00-04:00', '2021-07-22 10:33:00-04:00'), ('2021-07-22 10:33:00-04:00', '2021-07-22 10:36:00-04:00'), ('2021-07-22 10:36:00-04:00', '2021-07-22 11:22:00-04:00')]

#datapairs = [('2021-07-22 09:38:00', '2021-07-22 09:58:00'), ('2021-07-22 09:58:00', '2021-07-22 10:02:00'), ('2021-07-22 10:02:00', '2021-07-22 10:15:00'), ('2021-07-22 10:15:00', '2021-07-22 10:24:00'), ('2021-07-22 10:24:00', '2021-07-22 10:33:00'), ('2021-07-22 10:33:00', '2021-07-22 10:36:00'), ('2021-07-22 10:36:00', '2021-07-22 11:22:00')]

import itertools
dp = list(itertools.chain(*datapairs))
dx = pd.DatetimeIndex(dp)
it = iter(list(dx))
dp2 = [ (d,next(it)) for d in it ]


#mpf.plot(df, tz_localize=False, tlines=[dict(tlines=datapairs,tline_use='high',colors='g')])
#mpf.plot(df, tz_localize=False, tlines=[dict(tlines=datapairs,tline_use='high',colors='g')])

print(dp2)

mpf.plot(df, tlines=[dict(tlines=dp2,tline_use='high',colors='g')])
