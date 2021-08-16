from dateutil import parser as dp


time_list = ['2021-02-04 02:40:00', '2021-02-04 02:41:00', '2021-02-04 02:42:00', '2021-02-04 02:44:00', '2021-02-04 03:01:00', '2021-02-04 03:02:00', '2021-02-04 03:03:00', '2021-02-04 03:04:00', '2021-02-04 03:05:00']

answer_list = []
start = None
end   = None
for dtm in time_list:
    d = dp.parse(dtm)
    if start is None:
        start = d
        hour  = d.hour
    elif hour == d.hour:
        end   = d
        continue
    else:
        answer_list.append(dict(start=str(start),end=str(end)))
        start = d
        hour  = d.hour
answer_list.append(dict(start=str(start),end=str(end)))

print(answer_list)


import pandas as pd

df = pd.DataFrame(dict(datetime=time_list),index=pd.DatetimeIndex(time_list))
df['Hour'] = [d.hour for d in df.index]

print(df.groupby('Hour').first())
print(df.groupby('Hour').last())

answer_list = []
gbh = df.groupby('Hour')
for start,end in zip(gbh.first().values,gbh.last().values):
    answer_list.append(dict(start=start[0],end=end[0]))
print('answer_list=\n',answer_list)

