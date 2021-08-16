import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
## import talib
plt.style.use('fivethirtyeight')

#Collecting Data from Yahoo Finance

stock= 'COALINDIA.NS'
df= yf.download(stock,period='1mo', interval='1d')

#Using talib library to find instances where DOJI Candlestick Pattern showed up

#doji = talib.CDLDOJI(df['Open'], df['High'], df['Low'], df['Close'])
#df['Doji']= doji

#Using a variable to store all instances where the DOJI Candlestick Pattern was true (i.e. value > 0)

#DojiSignal=[]
#
#for i in range(0, len(df['Doji'])):
#    if df['Doji'][i] > 0:
#        DojiSignal.append(df['Doji'][i])

#Plotting Close price of the stock along with the days where DOJI Candlestick Pattern showed up (i.e. was TRUE)

figure, ax = plt.subplots(figsize=(13, 6))
plt.plot(df['Close'])#, markevery= DojiSignal)
plt.show()
