#!/usr/bin/env python
# coding: utf-8

import pandas     as pd
import datetime   as datetime
import matplotlib.dates as mdates

def date_to_mdate(date):
    """Convert a `date` to a matplotlib date:
    
    Input: `date` may be any of:
        (1) parseble string containing a date or datetime as a string,
        (2) python `datetime.date` or `datetime.datetime`,object
        (3) pandas.Timestamp object
    
    Returns a Matplotlib Date: floating point number of days from 01-Jan-0001, plus one day.
    """
    if isinstance(date,str):
        pydt = pd.to_datetime(date).to_pydatetime()
    elif isinstance(date,pd.Timestamp):
        pydt = date.to_pydatetime()
    elif isinstance(date,(datetime.datetime,datetime.date)):
        pydt = date
    else:
        return None
    return mdates.date2num(pydt)

def date_to_loc(dtindex,date):
    if not isinstance(dtindex,pd.DatetimeIndex):
        raise TypeError('dtindex must be a `pandas.DatetimeIndex` object')
    dtseries = dtindex.to_series()
    d1s = dtseries.loc[date:]
    if len(d1s) < 1:
        sdtrange = str(dtseries[0])+' to '+str(dtseries[-1])
        raise ValueError('Specified date "'+str(date)+'" is beyond '+
                         '(greater than) range of datetime index ('+sdtrange+').')
    d1 = d1s.index[0]
    d2s = dtseries.loc[:date]
    if len(d2s) < 1:
        sdtrange = str(dtseries[0])+' to '+str(dtseries[-1])
        raise ValueError('Specified date "'+str(date)+'" is before '+
                         '(less than) range of datetime index ('+sdtrange+').')
    d2 = d2s.index[-1]
    # If there are duplicate dates in the series, for example in a renko plot
    # then .get_loc(date) will return a slice containing all the dups, so:
    loc1 = dtseries.index.get_loc(d1)
    if isinstance(loc1,slice): loc1 = loc1.start
    loc2 = dtseries.index.get_loc(d2)
    if isinstance(loc2,slice): loc2 = loc2.stop - 1
        
    if loc1 == loc2:
        return float(loc1)

    # convert dates to matplotlib dates which are
    # floats and thus permit basic math (+-*/) in
    # order to be able to linearly interpolate:
    mpd1 = date_to_mdate(d1)
    mpd2 = date_to_mdate(d2)
    mpd  = date_to_mdate(date)
        
    slope   = (loc2 - loc1) / (mpd2 - mpd1)
    yitrcpt = loc1 - (slope*mpd1)
    
    x = (slope)*mpd + yitrcpt
    return x

# Test the code:

# Generate a datetime index with a point every 15 minutes:
ix = pd.date_range('5/7/2021 09:30','5/7/2021 16:00',freq='15T')

print('datetime index=')
print(ix,'\n')

# Check some dates that fall on and around one of the datetime index points:
checkdates = ['2021-05-07 11:43','2021-05-07 11:44','2021-05-07 11:45',
              '2021-05-07 11:46','2021-05-07 11:55','2021-05-07 11:50']
for date in checkdates:
    loc = date_to_loc(ix,date)
    print('date=',date, ' loc=',loc,)
