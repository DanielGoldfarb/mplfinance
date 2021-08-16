import mplfinance as mpf
import pandas as pd


# plt.style.use('ggplot')

# Extracting Data for plotting
data = pd.read_csv('NG.L.csv',index_col=0,parse_dates=True)

mpf.plot(data,type='candle',style='yahoo',
         #xlabel='TIMELINE of NG.L',
         ylabel='PRICE IN GBP POUND STERLING',
         title='NATIONAL GRID PLC - 2 JUNE 2021 - 9 JULY 2021',
         datetime_format='%d-%m-%Y')

