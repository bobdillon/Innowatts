import pandas as pd
from datetime import datetime
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go


#5. Plot  TODAY_LOAD, PREV_DAY_LOAD, ADJ_LOAD (3 series) onto Y-axis and 2/14-2/24 (Hourly) onto X-Axis

df = pd.read_csv('./innowatts/plot.csv').dropna()
#print(df.head(5))

# write a function that takes two column names,
# then gets proper dates, and assigns to arrays for 
def get_time(date, hour):
    x=[]
    #timeparser expects 0-23, not 1-24
    foo=(date.astype(str)+' '+((hour.astype(int)) -1.0).astype(str))
    for item in foo:
        #ditch '.0', again for time parser
        item = item[:-2]
        dt1 = datetime.strptime(item, '%m/%d/%Y %H')
        x.append(dt1)
    return x

#write a function to narrow the date range in the x domain
def to_unix_time(dt):
    epoch =  datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000

#define X and Y data
x1 = get_time(df['FORECAST_DT'], df['HOUR_NUM'])
x2 = get_time(df['FORECAST_DT.1'], df['HOUR_NUM.1'])
x3 = get_time(df['FORECAST_DT.2'], df['HOUR_NUM.2'])

y1 = df['TODAY_LOAD'].tolist()
y2 = df['PREV_DAY_LOAD'].tolist()
y3 = df['ADJ_LOAD'].tolist()

trace1 = go.Scatter(x=x1, y=y1, 
                    name='TODAY_LOAD',
                    mode = 'markers',
                    marker = dict(
                    color = '#C262D3',
                    size = 5,
                    line = dict(
                    color = 'rgb(231, 99, 250)',
                    width = 3)
                    ))
trace2 = go.Scatter(x=x2, y=y2, 
                    name='PREV_DAY_LOAD',
                    mode = 'markers',
                    opacity = 0.5,
                    marker = dict(
                    color = '#BC38D3',
                    size = 5)                   
                    )
trace3 = go.Scatter(x=x3, y=y3,
                    name='ADJ_LOAD',
                    mode = 'markers',
                    marker = dict(
                    color = '#8F04A8',
                    size = 5)  
                    )

data=go.Data([trace1, trace2, trace3])
layout = go.Layout(title='<b>Load, Feb 14th Through Feb 24th</b>',
                   titlefont=dict(
                   family='Helvetica',
                   size=30,
                   color='#9932CC'
                   ),
                   xaxis = dict(
                   range = [to_unix_time(datetime(2018, 2, 14, 0)),
                            to_unix_time(datetime(2018, 2, 24, 0))],
                   rangeselector=dict(
                       buttons=list([
                           dict(count=3,
                                label='3 Hour Spread',
                                step='hour',
                                stepmode='todate'),
                           dict(step='all',
                                label='Full Dataset Range')
                        ])
                    ),
                    rangeslider=dict(
                        visible = False
                    ),
                    type='date'

             ))
    
fig = go.Figure(data = data, layout = layout)
py.iplot(fig, filename='innoplot')
