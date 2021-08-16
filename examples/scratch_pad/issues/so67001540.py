import pandas as pd
import mplfinance as mpf
import jdatetime as jd

from matplotlib.ticker import Formatter
class JalaliDateTimeFormatter(Formatter): 
    """
    Formatter for JilaliDate in mplfinance.  
    Handles both show_nontrading=False and show_nontradging=True.
    When show_nonntrading=False, then the x-axis is indexed by an
    integer representing the row number in the dataframe, thus:
    Formatter for axis that is indexed by integer, where the integers
    represent the index location of the datetime object that should be
    formatted at that lcoation.  This formatter is used typically when
    plotting datetime on an axis but the user does NOT want to see gaps
    where days (or times) are missing.  To use: plot the data against
    a range of integers equal in length to the array of datetimes that
    you would otherwise plot on that axis.  Construct this formatter
    by providing the arrange of datetimes (as matplotlib floats). When
    the formatter receives an integer in the range, it will look up the
    datetime and format it.  

    """
    def __init__(self, dates=None, fmt='%b %d, %H:%M', show_nontrading=False):
        self.dates = dates
        self.len   = len(dates) if dates is not None else 0
        self.fmt   = fmt
        self.snt   = show_nontrading

    def __call__(self, x, pos=0):
        '''
        Return label for time x at position pos
        '''
        if self.snt:
            jdate = jd.date.fromgregorian(date=mdates.num2date(x))
            formatted_date = jdate.strftime(self.fmt)
            return formatted_date

        ix = int(np.round(x))
         
        if ix >= self.len or ix < 0:
            date = None
            formatted_date = ''
        else:
            date = self.dates[ix]
            print('type(date)=',type(date))
            jdate = jd.date.fromgregorian(date=mdates.num2date(date))
            formatted_date = jdate.strftime(self.fmt)
        return formatted_date

#  ---------------------------------------------------

df = pd.read_csv('so_67001540.csv',index_col=0,parse_dates=True)

print(df)
mpf.plot(df,figratio=(16,9),type="candle",style='yahoo',ylabel='',xrotation=90)

print('=========================================')
df = pd.read_csv('so_67001540.csv',index_col=5,parse_dates=True)
print(df)
mpf.plot(df,figratio=(16,9),type="candle",style='yahoo',ylabel='',xrotation=90)

