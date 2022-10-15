import pandas as pd

data=pd.read_csv('https://www.dropbox.com/s/fcpt5lejcf60n2e/SDG_Data_File_Daily.csv?dl=1')
output=data[data['Ticker'].isin(['AMG','PHM','HON','BMY','WMB','KO','SLG','OMC','NEE'])]
output.to_csv('output.csv')