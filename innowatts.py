import pandas as pd
import numpy as np

df1 = pd.read_csv('./innowatts/NOP_LOAD_FORECAST_20180214_04_input.csv')
#print(df1.columns)

df2 = df1.groupby(['CONGESTION_ZONE', 'FORECAST_DT', 'HOUR_NUM'],as_index=False)['VOLUME'].agg('sum')
df3 = df2.rename(columns ={'VOLUME':'TODAY_LOAD'})
#print(df3.head(5))
file1 = df3.filter(items=['CONGESTION_ZONE', 'FORECAST_DT', 'HOUR_NUM'])
#print(file1.head(5))

######begin file number 2##########
df4 = pd.read_csv('./innowatts/NOP_LOAD_FORECAST_20180213_11_input.csv')
#print(df4.columns)

df5 = df4.groupby(['CONGESTION_ZONE', 'FORECAST_DT', 'HOUR_NUM'],as_index=False)['VOLUME'].agg('sum').rename(columns ={'VOLUME':'PREV_DAY_LOAD'})
#print(df5.head(5))

# slice assign based on boolean match date string in dt column. 
# slightly faster than calling pd datetime object, way faster than iterating through all columns or elements.
df6 = df5[df5.FORECAST_DT != '2/13/2018']
#print(df6.head(5))
file2 = df6.filter(items=['CONGESTION_ZONE', 'FORECAST_DT', 'HOUR_NUM'])
#print(file2.head(5))

######begin file 3 operations########

df7 = pd.read_csv('./innowatts/LFG_ST_Hourly_20180213_input.csv')
#print(df3.columns)

df8 = df7.groupby(['CONGESTION_ZONE_CD', 'Forecast_Dt', 'Hour_num'],as_index=False)['UNADJ_LOAD',
       'DISTRIB_LOSS_LOAD', 'TRANSMISSION_LOSS_LOAD'].agg('sum')

df8['ADJ_LOAD'] = (df8['UNADJ_LOAD'] +df8['DISTRIB_LOSS_LOAD']+df8['TRANSMISSION_LOSS_LOAD'])
#print(df8.head(5))
file3 = df8.filter(items=['CONGESTION_ZONE_CD', 'Forecast_Dt', 'Hour_num']).rename(columns ={'CONGESTION_ZONE_CD':'CONGESTION_ZONE','Forecast_Dt':'FORECAST_DT','Hour_num':'HOUR_NUM'})
#print(file3.head(5))

### create output csv DF ####
#concat all 3 by CONGESTION_ZONE, FORECAST_DT, HOUR_NUM
frames = [file1, file2, file3]
result = pd.concat(frames).reset_index(drop=True)
#print(result.head(10))

#concat TODAY_LOAD, PREV_DAY_LOAD, ADJ_LOAD  to sides as unique columns per csv directions ###
# make outputcsv 
'''finalcsv = pd.concat([result, df3['TODAY_LOAD'], df5['PREV_DAY_LOAD'], df8['ADJ_LOAD']], axis=1).reset_index(drop=True)
finalcsv.to_csv('./innowatts/output.csv', index=False)'''

#### set up plot #########
# make better csv for plotting
'''plotcsv = pd.concat([file1, df3['TODAY_LOAD'], file2, df5['PREV_DAY_LOAD'], file3, df8['ADJ_LOAD']], axis=1).reset_index(drop=True)
plotcsv.to_csv('./innowatts/plot.csv')'''