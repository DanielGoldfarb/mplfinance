from datetime import datetime, timedelta, date
import pandas_datareader as pdr
import mplfinance as mpf
import pandas as pd
    
df_history = pdr.get_data_yahoo(symbols='GOLD', 
                                    start=datetime(2020, 8, 30), 
                                    end=datetime(2021, 2, 23))
    

# Today is: 24.02.2021
two_points  = [(datetime(2020, 8, 30),28.72),(datetime(2021, 3, 26),23.49)]
mpf.plot(df_history, type='candle')
mpf.plot(df_history, type='candle', alines=two_points, show_nontrading=True)


dfa = df_history.iloc[0:1].copy()
dfa.index = [datetime(2020, 8, 30)]


dfb = df_history.iloc[-2:-1].copy()
dfb.index = [datetime(2021, 3, 26)]


#  df_new = dfa.append(df_history)
#  df_new = df_new.append(dfb)

df_new = pd.concat([dfa,df_history,dfb])

mpf.plot(df_new, type='candle', alines=two_points)

