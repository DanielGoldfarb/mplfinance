import mplfinance as mpf
import pandas as pd

# AAPL call volume %
# Selecting specifics mentioning AAPL
#AAPL_df = naster_df[master_df['ticker'] == 'AAPL'][[
#             'ticker', 'date', 'call_volume', 'put_volume', 
#             'call_ratio', 'put_ratio', 'open', 'low',
#             'high', 'close','volume']]


AAPL_df = pd.read_csv('so70418851_data.csv',index_col=0,parse_dates=True)

# MPF requires DateTimeIndex for plotting
#AAPL_df = AAPL_df.set_index('date')

# Dropping NA's, Not sure if needed so commented out
AAPL_df.dropna()

# Plotting call ratio with close price and volume
# MPF package requires volume to be explicitly named
# Dropping share volume as calculation is already made
# Renaming call volume to volume
AAPL_df = AAPL_df.drop(
                 'volume', axis = 1).rename(
                                     columns = {'call_volume':'volume'})

# Adding a call ratio (in %) as the bottom panel secondary y axis
ap = mpf.make_addplot((AAPL_df['call_ratio']), panel = 1, linestyle = 'dotted', ylabel = 'Options % ratio')#, color='black')

# Plotting AAPL share price with Open, High, Low, Close candles
# call_volume = volume

mpf.plot(AAPL_df, 
         type = 'candle', 
         volume = True, 
         addplot = ap,  
         ylabel = 'AAPL share price',
         ylabel_lower = 'Call Volume',
         style='binance',
         #figscale=1.3,
         fontscale=.77,
         savefig=dict(fname='issue486.png',dpi=300))

mpf.plot(AAPL_df, 
         type = 'candle', 
         volume = True, 
         addplot = ap,  
         ylabel = 'AAPL share price',
         ylabel_lower = 'Call Volume',
         #figscale=1.3,
         fontscale=.77,
         style='binance')
