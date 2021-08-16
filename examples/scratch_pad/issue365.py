#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import mplfinance as mpf

df = pd.read_csv('../data/gbpusd_yf20210401-0407.csv',index_col=0,parse_dates=True)
df.index = df.index.tz_localize(None)
print('df.shape=',df.shape)
print(df.head())
print(df.tail())

# Extract unique dates from the intraday data:
# Don't take the last date, because yfinances ends last day early.
dates = pd.Series([d.date() for d in df.index]).unique()

# generate a list of open and close times, from the unique dates.
# also color the opens and the closes differently.
octimes = []
colors  = []
for d in dates:
    dt = pd.Timestamp(d)
    octimes.append(dt.replace(hour=9,minute=30))
    octimes.append(dt.replace(hour=16,minute=0))
    colors.append('b')
    colors.append('r')

# Plot with vertical lines at the market open and close times:
# mc = mpf.make_marketcolors(base_mpf_style='yahoo')
# s  = mpf.make_mpf_style(base_mpf_style='nightclouds',marketcolors=mc)
# mpf.plot(df,type='candle',vlines=dict(vlines=octimes,colors=colors),style=s)
mpf.plot(df,type='candle',vlines=dict(vlines=octimes,colors=colors),title='\nGBP/USD')
