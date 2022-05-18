#!/usr/bin/env python
# coding: utf-8

# ### Uses for DateIlocTransform
# 
# #### All uses are for `show_nontrading=False` only:
# 
# - `.to_date()` - location *to* date: for tick label formatting.
# - `.to_iloc()` - date *to* location: for `xticks` placement.
# - `.to_iloc()` - date *to* location: for `xlim` placement.
# - `.to_iloc()` - date *to* location: for `lines` placement.
# 
# ---
# 
# - It seems to me that  
#   - **interpolation** may be better using the actual datetime series (rather than the linear formula), whereas 
#   - **extrapolation** *may require* the linear formula.
#     - Or for "known" cases may be able to use **date calculations**, for example:
#       - quartile(0.65) == quartile(0.50) == quartile(0.35) == "known" frequency.
#       - intraday with consistent trading hours in data
#       - daily with weekends missing (maybe someday allow users to supply holidays)
#       - weekly, monthly, yearly, etc. are simple?
#   - need to run some tests to see which, if either, is better.
# - Keep in mind, while testing, that `xlim` values will affect `xticks` placement.
# 

import pandas as pd
import numpy  as np

class TimeSeriesFrequency:
    ''' Class that contains all frequency info needed to generate a Pandas DatetimeIndex
    for typical trading/market situations.  For example, this class contains a both
    "day" frequency and an "itraday" frequency to allow for intraday data (per hour,
    or per minute, etc) that occurs only on trading days (for example, Mon-Fri).
    This class also contains an open time and close time for market trading hours.
    '''
    def __init__(self,dfreq='B',ifreq='H',weekmask=None,open_time='09:30',close_time='16:00'):
        self._dfreq  = dfreq
        self._ifreq  = ifreq
        self._wmask  = weekmask
        self._topen  = pd.Timestamp(open_time)
        self._tclose = pd.Timestamp(close_time)

    @property
    def dfreq(self):
        return self._dfreq

    @property
    def ifreq(self):
        return self._ifreq

    @property
    def weekmask(self):
        return self._wmask

    @property
    def topen(self):
        return self._topen.time()

    @property
    def tclose(self):
        return self._tclose.time()

    def __repr__(self):
        s  = self.__class__.__name__
        s += "(d='"+str(self._dfreq)+"'"
        s += ", i='"+str(self._ifreq)+"'"
        s += ", w='"+str(self._wmask)+"'"
        s += ", o='"+str(self._topen.strftime('%H:%M:%S'))+"'"
        s += ", c='"+str(self._tclose.strftime('%H:%M:%S'))+"'"
        s += ")"
        return s
    
    
class DateIlocTransform:
    '''Create a transform object that can transform from a Datetime to an index location, 
    and/or from index location to Datetime.  
    - Requires a Pandas DatetimeIndex object (as input) upon creation.
    
    This class also contains utilities, that it uses and that you can use, for:
    - Generating a Pandas DatetimeIndex given a TimeSeriesFrequency object
    - Inferring the TimeSeriesFrequency of a Pandas DatetimeIndex object
    
    If `date` does not exactly match a date in the series then interpolate between two dates.
    If `date` is outside the range of dates in the series, then extrapolate.
    
    The are two ways to extrapolate.  The preferred way is to determine the frequency of the
    input DatetimeIndex, and extrapolate the DatetimeIndex itself.  Then we treat the extrapolated
    DatetimeIndex as if it were the original index and just match or interpolate as needed.
    If we cannot determine the frequency of the original DatetimeIndex then we determine, via least
    squares fit, a linear relationship between the dates and the index locations, and use that linear
    equation to extrapolate.

    By default, to save calculation time, we do not extrapolate at all, but simply fail to transform
    if the caller requests transformation of data outside the range of the input DatetimeIndex.
    Another way to say this is that, by default, the extrapolation limits are set to the limits 
    (start and end) of the inputted DatetimeIndex.

    The user optionally can call `.set_extrapolation_limits()` which will trigger frequency inference
    and extrapolation of the DatetimeIndex (or, if the frequency cannot be inferred, trigger the least 
    squares linear fit mentioned above).  The user can than transform data within the newly specified 
    extrapolation limits.

    Alternatively, maybe we don't force the user to expand the extrapolation limits, but automatically
    expand them if a date is requested that requires us to go outside the current limits.
    '''
    
    def __init__(self,dtindex):
        if not isinstance(dtindex,pd.DatetimeIndex):
            raise TypeError('Need `pandas.DatetimeIndex`, but got "'+str(type(dtindex))+'"')
        if not len(dtindex) > 1:
            raise ValueError('`dtindex` must have length of at least 2.')
        self._inferred_frequency = DateIlocTransform.infer_frequency(dtindex)
        
        self._extrapolation_limits = (0,len(dtindex))
        
        ixlist = [float(x) for x in range(len(dtindex))]
        self._to_iloc_series = pd.Series(ixlist,index=dtindex)
        self._to_date_series = pd.Series(dtindex.values,index=ixlist)
        #dtseries = dtindex.to_series()
        #self._lsslope, self._lsyicpt = self._lsq_linear(dtseries)
        #self._epslope, self._epyicpt = self._ep_linear(dtseries)

    def to_iloc(self,date):
        i1s = self._to_iloc_series.loc[:date]
        i1  = i1s[-1] if len(i1s) > 0 else float('nan') # else need to extrapolate
        i2s = self._to_iloc_series.loc[date:]
        i2  = i2s[ 0] if len(i2s) > 0 else float('nan') # else need to extrapolate
        #print('\ndate,i1,i2=',date,i1,i2)
        loc1 = i1
        loc2 = i2
        d1 = self._to_date_series.iloc[int(round(i1,0))]
        d2 = self._to_date_series.iloc[int(round(i2,0))]
        #print('date,i1,i2,d1,d2=',date,i1,i2,d1,d2)
        # if iloc is between two dates, linearly interpolate between those dates:
        loc = ((date-d1)/(d2-d1))*(loc2-loc1) + loc1 if d1 != d2 else loc1
        #print('loc1,loc2,loc=',loc1,loc2,loc)
        return loc
    
    def to_datetime(self,iloc):
        #self._to_date_series = pd.Series(dtindex.values,index=range(len(dtindex))) 
        d1s = self._to_date_series.loc[:iloc]
        print('len(d1s)=',len(d1s))
        d1  = d1s.iloc[-1] if len(d1s) > 0 else float('nan') # else should extrapolate
        d2s = self._to_date_series.loc[iloc:]
        print('len(d2s)=',len(d2s))
        d2  = d2s.iloc[ 0] if len(d2s) > 0 else float('nan') # else should extrapolate
        if d1 == d2:
            return d1
        print('d1,d2=',d1,d2)
        loc1 = int(round(self._to_iloc_series.loc[d1],0))
        loc2 = int(round(self._to_iloc_series.loc[d2],0))
        #print('\nd1,d2=',d1.date().day,d2.date().day,
        #      ' iloc,loc1,loc2=',iloc,loc1,loc2)
        #print('\nd1,d2,(d2-d1),type(d2-d1)=',d1,d2,d2-d1,type(d2-d1))
        # d1,d2= 8 11  iloc,loc1,loc2= 5.333333333333333 5 6
        # d1,d2,(d2-d1)= 2019-11-08 00:00:00 2019-11-11 00:00:00 3 days 00:00:00
        # Timestamp('2019-11-08 23:59:59.999999999')
        # d = ((iloc-loc1)/(loc2-loc1))*(d2-d1) + d1
        d = ((iloc-loc1)*(d2-d1)) + d1
        return d.round('s')            

    @staticmethod
    def timedelta_to_freqabbr(td):
        '''
        Convert a Pandas.Timedelta object into a frequency
        abbreviation string.
        This method used by `infer_frequency()`.
        '''
        if not isinstance(td,pd.Timedelta): return None
        hours   = int(round(td.seconds/(60*60)))
        minutes = int(round(td.seconds%(60*60)/60))
        seconds = int(round(td.seconds%60))
        if td.microseconds/1000 >= 500:
            seconds += 1.
        # If only one of hours, minutes, or seconds is
        # non-zero, then we can use an abbreviation.
        if minutes == seconds == 0:
            freq = str(hours)+'H'
        elif hours == seconds == 0:
            freq = str(minutes)+'T'
        elif hours == minutes == 0:
            freq = str(seconds)+'S'
        else:
            freq = None
        return freq
    
    @staticmethod
    def infer_weekmask(ix):
        '''
        Infer the weekmask of a pandas.DatetimeIndex

        Args:
            ix: pandas DatetimeIndex

        Returns
            weekmask: list of seven bools, corresponding
                      to Mon,Tue,Wed,Thu,Fri,Sat,Sun.
        '''
        weekdaydf = pd.DataFrame(dict(date=ix,dayofweek=[d.dayofweek for d in ix]))
        weekdays  = weekdaydf.groupby('dayofweek').count()
        c = weekdays.columns[0]
        cutoff = 0.25 * weekdays[c].max()
        days = weekdays[ weekdays[c] > cutoff].index.values
        #print('days=',days)
        weekmask = [day in days for day in range(7)]
        #print('weekmask=',weekmask)
        return weekmask
    
    @staticmethod
    def infer_open_close_times(ix):
        '''
        Infer the open and close times of intraday data
        '''
#       TODO: Fill out this function, and use it
#       TODO: to create TSFreq at bottom of infer_frequency!!!
        return ('09:30:00','16:00:00')


    @staticmethod
    def infer_frequency(data,trace=True):
        '''
        Infer the frequency of a pandas.DatetimeIndex
        even if that DatetimeIndex contains some gaps.
        
        Args:
            data:  DataFrame with a DatetimeIndex, or
                   Series with a DatetimeIndex, or
                   DatetimeIndex
    
        Returns:
            freq:  Inferred frequency of type `class TimeSeriesFrequency`
        '''
        if isinstance(data,(pd.core.frame.DataFrame,pd.core.frame.DataFrame)):
            if not isinstance(data.index,pd.core.indexes.datetimes.DatetimeIndex):
                raise TypeError('DataFrame or Series must have DatetimeIndex to infer frequency')
            dts = data.index.to_series()
        elif isinstance(data,pd.core.indexes.datetimes.DatetimeIndex):
            dts = data.to_series()
        else:
            raise TypeError('Input must be DataFrame, Series, or DatetimeIndex')
            
        # At this point `dts` is a datetime series
        
        if not dts.is_monotonic: dts = dts[::-1]
        if not dts.is_monotonic: raise ValueError('data is not monotonic!')
        diff = dts.diff(1)
        vc = diff.value_counts()
        basefreq = vc.idxmax()
        ifreq = None
        if trace:
            print('basefreq=',basefreq)
            print('basefreq.days=',basefreq.days)
            mask = DateIlocTransform.infer_weekmask(dts.index)
            print('weekmask=',mask)
        if basefreq.days < 1:
            abbr  = DateIlocTransform.timedelta_to_freqabbr(basefreq)
            ifreq = basefreq if abbr is None else abbr
            dfreq = 'B'
            print(dts.iloc[[0,1,2,-3,-2,-1]])
            mask = DateIlocTransform.infer_weekmask(dts.index)
        elif basefreq.days == 1:
            dfreq = 'B'
            # infer weekmask:
            mask = DateIlocTransform.infer_weekmask(dts.index)
        elif basefreq.days >= 6 and basefreq.days <= 8:
            dfreq = 'W'
        elif basefreq.days >= 28 and basefreq.days <= 31:
            dfreq = 'M'
        elif basefreq.days >=(3*28) and basefreq.days <= (3*31):
            dfreq = 'Q'
        elif basefreq.days >=(12*28) and basefreq.days <= (12*31):
            dfreq = 'Y'
        else:
            dfreq = None
        if trace:
            print('\nvc(value counts)=')
            print(vc)
            print('ifreq =',ifreq,'\n')
            print('dfreq =',dfreq,'\n')
        # __init__(self,dfreq='B',ifreq='H',weekmask=None,open_time='09:30',close_time='16:00'):

    #        if dfreq == 'B':
    #            wm = DateIlocTransform.infer_weekmask(dts.index)
    #            if wm.count(True) < 5


        # if ifreq is not None, try to determine open_time and close_time.
        # if span > 1 day and dfreq == 'B' try to determine weekmask

        return TimeSeriesFrequency(ifreq=ifreq,dfreq=dfreq,weekmask=mask)

    @staticmethod
    def time_series_index(start=None,end=None,freq=TimeSeriesFrequency()):
        '''
        Generate a Pandas.Datetime index from a TimeSeriesFrequency object.
        Args:
            start: start pd.Timestamp object  (default: today)
            end:   end   pd.Timestamp object  (default: today+1)
            freq:  TimeSeriesFrequency object (default: TimeSeriesFrquency())

        Returns:
            Pandas.DatetimeIndex
        '''
        from pandas.tseries.holiday import USFederalHolidayCalendar
        if not isinstance(freq,TimeSeriesFrequency):
            raise TypeError('`freq` must be of type TimeSeriesFrequency')
        if start is None: start = pd.Timestamp.today()
        if end   is None: end   = start + pd.Timedelta(days=1)
        if isinstance(start,str): start = pd.Timestamp(start)
        if isinstance(end  ,str): end   = pd.Timestamp(end)
        if not isinstance(start,pd.Timestamp):
            raise TypeError('`start` must be of type pd.Timestamp, or type str parseable to pd.Timestamp')
        if not isinstance(end,pd.Timestamp):
            raise TypeError('`end` must be of type pd.Timestamp, or type str parseable to pd.Timestamp')
        if not start < end:
            raise ValueError('`start` must be less than `end`.')
    
        bday_freq  = freq.dfreq
        iday_freq  = freq.ifreq
        weekmask   = freq.weekmask
        if weekmask is not None:
            if weekmask == [True,True,True,True,True,False,False]:
                if bday_freq != 'B':
                    raise ValueError('Weekmask says bday_freq should be "B"')
                weekmask = None
            else:
                bday_freq = 'C'
        open_time  = freq.topen
        close_time = freq.tclose
    
        print('start=',start,' end=',end)
        print('bday_freq=',bday_freq,' iday_freq=',iday_freq,' weekmask=',weekmask)
        print('open_time=',open_time,' close_time=',close_time)
    
        #topen  = pd.Timestamp(open_time)
        #tclose = pd.Timestamp(close_time)

        #print('topen=',topen,'tclose=',tclose)
        
        #if bday_freq == 'B':
        #    bday_freq = pd.offsets.CustomBusinessDay(calendar=USFederalHolidayCalendar())
        daily = []
        dates =  pd.bdate_range(start=start,end=end,freq=bday_freq,weekmask=weekmask)
        if iday_freq is None:
            return dates
    
        for d in dates:
            topen = open_time
            if d.date() == start.date():
                if start.time() >= open_time and start.time() <= close_time:
                    topen = start.time()
                elif start.time() > close_time:
                    continue

            d1 = d.replace(hour=topen.hour,minute=topen.minute)

            tclose = freq.tclose
            if d.date() == end.date():
                if end.time() >= open_time and end.time() <= close_time:
                    tclose = end.time()
                elif end.time() < open_time:
                    continue

            d2 = d.replace(hour=tclose.hour,minute=tclose.minute)

            print('topen=',topen,'tclose=',tclose)
            print('d1=',d1,'d2=',d2,'iday_freq=',iday_freq)
            daily.append(pd.date_range(d1,d2,freq=iday_freq))
       
        index = daily[0].union_many(daily[1:])
        return index
    
