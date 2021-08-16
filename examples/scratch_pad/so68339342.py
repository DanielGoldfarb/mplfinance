import matplotlib.pyplot as plt
from   mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
import datetime as dt

plt.style.use('ggplot')

# Extracting Data for plotting
data = pd.read_csv('NG.L.csv')
ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close', ]]
ohlc['Date'] = pd.to_datetime(ohlc['Date'])
ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
ohlc = ohlc.astype(float)

# Creating Subplots
fig, ax = plt.subplots()
candlestick_ohlc(ax, ohlc.values, width=0.8, colorup='green', colordown='red', alpha=0.8)

# Setting labels & titles
ax.set_xlabel('TIMELINE of NG.L')
ax.set_ylabel('PRICE IN GBP POUND STERLING')
fig.suptitle('NATIONAL GRID PLC - 2 JUNE 2021 - 9 JULY 2021')

# Formatting Date
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()
fig.tight_layout()
plt.show()
