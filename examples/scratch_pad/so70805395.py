import mplfinance as mpf
import pandas as pd


df = pd.read_csv('../data/yahoofinance-SPY-20200901-20210113.csv',index_col=0,parse_dates=True)

jj = int(len(df)/3)

df = df.iloc[jj:-jj,:]

BACKGROUND_COLOUR = 'k'
LINE_COLOUR = 'gray'
TEXT_COLOUR = 'orange'

market_colours = mpf.make_marketcolors(up="g", down="r", edge=BACKGROUND_COLOUR, wick=LINE_COLOUR)
style = mpf.make_mpf_style(marketcolors=market_colours, facecolor=BACKGROUND_COLOUR, edgecolor=LINE_COLOUR,
                           figcolor=BACKGROUND_COLOUR, gridcolor=LINE_COLOUR, gridstyle="--")

#   mpf.plot(df,type='candle',style=style)
fig, axlist = mpf.plot(df,type='candle',style=style,returnfig=True)

ax = axlist[0]

ax.xaxis.label.set_color(TEXT_COLOUR)
ax.yaxis.label.set_color(TEXT_COLOUR)
for axis in ["left"]:  # modify borders
    ax.spines[axis].set_color(LINE_COLOUR)
    ax.spines[axis].set_linewidth(3)
for axis in ["top", "right", "bottom"]:  # remove borders
    ax.spines[axis].set_linewidth(0)
for axis in ["x", "y"]:
    ax.tick_params(axis=axis, colors=LINE_COLOUR, which="both", width=2)

mpf.show()
