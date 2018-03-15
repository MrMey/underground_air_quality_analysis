import pandas as pd

def process_horaires():
    # processing horaires
    horaires = pd.read_csv('horaires.csv')

    horaires['hour'], horaires['minute'], horaires['second'] = horaires['arrival_time'].str.split(':').str
    horaires['hour'] = horaires['hour'].astype(int)
    horaires['minute'] = horaires['minute'].astype(int)
    horaires['second'] = horaires['second'].astype(int)

    horaires['hour'] = horaires['hour'] % 24

    horaires['day'] = 1
    horaires['month'] = 1
    horaires['year'] = 2018


    horaires['time'] = pd.to_datetime(horaires[['year','month','day','hour','minute','second']])

    horaires = horaires.drop(labels = ['arrival_time',
                                       'departure_time',
                                       'year','month','day','hour','minute','second',
                                       'trip_id','stop_sequence'],
                  axis = 1)
    # Grouping per hour and type
    horaires = horaires.groupby([horaires['time'].dt.to_period('H'), 'ligne', 'station']).count()
    horaires = horaires.drop(labels = ['time'], axis = 1)
    horaires = horaires.reset_index()
    return horaires

def process_meteo():
    # processing meteo
    meteo = pd.read_csv('meteo_paris.csv')
    meteo['date'] = pd.to_datetime(meteo['date'], format='%d/%m/%Y').dt.strftime(date_format='%Y-%m-%d')
    return meteo

def process_air_quality():
    # processing air_quality
    air_quality = pd.read_csv('air_quality.csv')
    air_quality = air_quality.drop(labels = ['year-month','year','month','day'], axis = 1)

    return air_quality

meteo = process_meteo()

horaires = process_horaires()
horaires['time'] = horaires['time'].dt.strftime(date_format='%H:%M:%S')

air_quality = process_air_quality()

data = air_quality.merge(right = meteo, how = 'left', on = ['date'], left_index= False, right_index= False)
data = data.merge(right = horaires, how = 'inner', on = ['time','station'], left_index= False, right_index= False)

data.to_csv('all_data.csv', index = False)