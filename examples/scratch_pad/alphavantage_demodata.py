
import json
import pandas as pd
import mplfinance as mpf

with open('alphavantage_demodata.json','r') as f:
    json_string = f.read()

json_data = json.loads(json_string)

tsjson   = json_data['Time Series (5min)']
metadata = json_data['Meta Data']

# convert dict of dicts to list of dicts:
dfdata = [v for v in tsjson.values()]  

df = pd.DataFrame(dfdata)                  # list of dicts to dataframe
df.index = pd.DatetimeIndex(tsjson.keys()) # dict keys to dataframe index

df.columns = ['Open','High','Low','Close','Volume']

# convert string columns to numeric:
for col in df.columns:
    df[col] = pd.to_numeric(df[col],errors='coerce')

df = df.iloc[::-1]  # reverse data (make oldest first in df)

#df.to_csv('alphavantage_demodata.csv')

dfs = df.iloc[0:180]

print('head=')
print(dfs.head())
print('tail=')
print(dfs.tail())
mpf.plot(dfs,type='candle',tight_layout=True)

dfs = dfs.iloc[60:150]

print()
print('head=')
print(dfs.head())
print('tail=')
print(dfs.tail())
mpf.plot(dfs,type='candle',tight_layout=True)

'''
head=
                         Open      High       Low     Close  Volume
2022-04-18 13:50:00  124.7373  124.7588  124.6304  124.6995   25566
2022-04-18 13:55:00  124.6798  124.7560  124.5909  124.7489   27784
2022-04-18 14:00:00  124.7885  124.9860  124.7785  124.8082   53736
2022-04-18 14:05:00  124.8181  124.8971  124.5711  124.6699   64928
2022-04-18 14:10:00  124.6699  124.7736  124.6600  124.7440   28838
tail=
                         Open      High       Low     Close  Volume
2022-04-19 11:15:00  126.1517  126.2406  126.1122  126.2245   48848
2022-04-19 11:20:00  126.2406  126.2918  126.0826  126.0826   66230
2022-04-19 11:25:00  126.0974  126.1418  125.9146  126.0628  103707
2022-04-19 11:30:00  126.0875  126.2159  126.0529  126.2159   39508
2022-04-19 11:35:00  126.2209  126.3592  126.1221  126.2604   82500
'''

dfs = dfs.loc['2022-04-18 15:30':'2022-04-19 10:00',:]

print('dfs=')
print(dfs)

mpf.plot(dfs,type='candle',tight_layout=True)
