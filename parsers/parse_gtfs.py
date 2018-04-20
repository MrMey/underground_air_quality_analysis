# coding: utf8
import pandas as pd

base_path = 'horaires/'
stops_path = '/stops.txt'
stop_time_path = '/stop_times.txt'
stations = {'Châtelet':'chatelet',
            'Châtelet-Les Halles':'chatelet',
            'Franklin-Roosevelt':'franklin',
            'Auber':'auber',
            'Havre-Caumartin':'auber',
            'Opéra':'auber'}
lignes = ['1','3','4','7','8','9','11','14','a','b']



data = pd.DataFrame(columns=['trip_id','arrival_time',
                             'departure_time','stop_id',
                             'stop_sequence','station','ligne'])
for ligne in lignes:
    print()
    stops = pd.read_csv(base_path + ligne + stops_path)
    stop_time = pd.read_csv(base_path + ligne + stop_time_path)
    for key,station in stations.items():
        stop_ids = stops['stop_id'][stops['stop_name'] == key]

        for stop_id in stop_ids:
            stop_at_station = stop_time[stop_time['stop_id'] == stop_id]
            stop_at_station['station'] = station
            stop_at_station['ligne'] = ligne
            stop_at_station = stop_at_station.drop(labels = ['stop_headsign', 'shape_dist_traveled'], axis = 1)
            data = pd.concat([data,stop_at_station], axis = 0)

data.to_csv('horaires.csv', index = None)