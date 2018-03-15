import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

def agregate_air_data():
    raw_data = pd.read_csv('qualite-de-lair-mesuree-dans-la-station-auber.csv',sep = ';')
    raw_data['station'] = 'auber'
    raw_data.columns = raw_data.columns.str.lower()

    data = raw_data
    raw_data = pd.read_csv('qualite-de-lair-mesuree-dans-la-station-chatelet.csv',sep = ';')
    raw_data['station'] = 'chatelet'
    raw_data.columns = raw_data.columns.str.lower()

    data = pd.concat([data,raw_data],axis = 0)

    raw_data = pd.read_csv('qualite-de-lair-mesuree-dans-la-station-franklin-d-roosevelt.csv',sep = ';')
    raw_data['station'] = 'franklin'
    raw_data.columns = raw_data.columns.str.lower()

    data = pd.concat([data,raw_data],axis = 0)

    data.to_csv('agregated_data.csv',index = False)


def open_air_data():
    data = pd.read_csv('agregated_data.csv')
    return data

data = open_air_data()
data['date/heure'] = data['date/heure'].str.split('+').str.get(0)

data['date/heure'] = pd.to_datetime(data['date/heure'],format="%Y-%m-%dT%H:%M:%S")
data['date'] = data['date/heure'].dt.date
data['time'] = data['date/heure'].dt.time
data['month'] = data['date/heure'].dt.month
data['year'] = data['date/heure'].dt.year
data['year-month'] =  data['year'].astype(str) + '/'+data['month'].astype(str)
data['day'] = data['date/heure'].dt.day

data = data.drop(labels = ['date/heure'], axis = 1)

data.to_csv("parsed_data.csv",index = None)

print(data.head())
def countplot_by_column(data,column, hue = None):
    ax = sns.countplot(x=column,data = data, hue = None)
    ax.set_title('number of occurence by {}'.format(column))
    ax.set_label()
#countplot_by_column(data,'station')



temp = data.loc[:,['year-month','month','year','co2','humi','no','no2','pm10','pm2.5']].groupby(['year-month','month','year']).agg(['mean'])

temp = temp.reset_index()
temp.columns = ["_".join(x) for x in temp.columns.ravel()]

temp.plot(x = 'year-month_', y = 'co2_mean')
