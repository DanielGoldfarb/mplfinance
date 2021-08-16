import pandas as pd
import mplfinance as mpf

chartData = {
         'o': [5.589310029183743, 5.610726267831264, 5.6097540855407715, 5.594677448272705, 5.564507322870441, 5.490811827389135], 
         'c': [5.610726267831264, 5.6097540855407715, 5.594677448272705, 5.564507322870441, 5.490811827389135, 5.49099588394165], 
         'h': [5.610831260681152, 5.610726267831264, 5.6097540855407715, 5.594677448272705, 5.564507322870441, 5.49099588394165], 
         'l': [5.57621750831604, 5.608160018920898, 5.582586765289307, 5.5580267906188965, 5.485752105712891, 5.490811827389135], 
         'v': [90.34457968175411, 5.964259386062622, 27.667950868606567, 101.91513729095459, 273.24095344543457, 4.425440788269043], 
         't': [1625720400, 1625721000, 1625721600, 1625722200, 1625722800, 1625723400]}

df = pd.DataFrame(chartData)
df.columns = ['Open', 'Close', 'High', 'Low', 'Volume', 'Date']
data = df.loc[:, ['Open', 'Close', 'High', 'Low', 'Volume', 'Date']]
data['Date'] = pd.to_datetime(data['Date'], unit='s', origin='unix')
data.index = pd.DatetimeIndex(data['Date'])

#fg1, _ = mpf.plot(data, type='candle',

customstyle =  mpf.make_mpf_style(base_mpf_style='yahoo',y_on_right=False,facecolor='w')

mpf.plot(data, type='candle',
              title="PolyVertex Price",
              ylabel='Price',
              ylabel_lower='Volume',
              #figsize=(20,10),
              #returnfig=True,
              style='yahoo',
              volume=True,
              )
mpf.plot(data, type='candle',
              title="PolyVertex Price",
              ylabel='Price',
              ylabel_lower='Volume',
              #figsize=(20,10),
              #returnfig=True,
              style=customstyle,
              volume=True,
              )

#fg1.savefig('text1.jpg')
