# coding: utf-8

import os
import pandas as pd
import re

# command used to parse pdf : pdftotext -layout horaires.pdf

def horaire_lines_to_table(table):
    all_station = {}
    for line_idx in range(len(horaire_lines)):
        if re.match(r'(Chatelet-Les Halles|Auber)', table[line_idx]):
            if re.match(r'Chatelet-Les Halles', table[line_idx]):
                horaire_string = re.sub(r'Chatelet-Les Halles','',table[line_idx])
                station = 'chatelet'
            if re.match(r'Auber', table[line_idx]):
                horaire_string = re.sub(r'Auber', '', table[line_idx])
                station = 'auber'

            horaire_string = horaire_string.lstrip().rstrip('\n')
            horaire_list = re.findall(r"([0-9]+)",horaire_string)

            hour_list = horaire_list[0::2]
            minute_list = horaire_list[1::2]
            horaire_list = [ x[0] + ":" + x[1] for x in zip(hour_list,minute_list)]
            all_station[station] = horaire_list


    return all_station

ligne = 'B'
file = 'horaires_B_direction_charles_de_gaulle'
if ligne == 'A':
    with open(file + '.txt','r') as horaire_file:
        auber_horaire = []
        chatelet_horaire = []


        for i in range(18):
            line = horaire_file.readline()
            while line != '         CIRCULATION\n':
                line = horaire_file.readline()

            horaire_lines = []
            line = horaire_file.readline()
            while line != '\n':
                line = horaire_file.readline()
                horaire_lines.append(line)
            horaire = horaire_lines_to_table(horaire_lines)
            auber_horaire += horaire['auber']
            chatelet_horaire += horaire['chatelet']

        data = pd.DataFrame(data = {'station':['auber']*len(auber_horaire)+['chatelet']*len(chatelet_horaire),
                             'time':auber_horaire+chatelet_horaire,
                             'jour':'semaine'},
                            columns = ['station','time','jour'])
        auber_horaire = []
        chatelet_horaire = []

        for i in range(12):
            line = horaire_file.readline()
            while line != '         CIRCULATION\n':
                line = horaire_file.readline()
                print(line)

            horaire_lines = []
            line = horaire_file.readline()
            while line != '\n':
                line = horaire_file.readline()
                horaire_lines.append(line)
            horaire = horaire_lines_to_table(horaire_lines)
            auber_horaire += horaire['auber']
            chatelet_horaire += horaire['chatelet']

        data2 = pd.DataFrame(data = {'station':['auber']*len(auber_horaire)+['chatelet']*len(chatelet_horaire),
                             'time':auber_horaire+chatelet_horaire,
                             'jour':'ferie'},
                            columns = ['station','time','jour'])
        data = pd.concat((data,data2),axis = 0)
        data.to_csv(file + '.csv', index = False)

if ligne == 'B':
    with open(file + '.txt', 'r') as horaire_file:
        chatelet_horaire = []

        for i in range(16):
            line = horaire_file.readline()
            while not re.search(r'CIRCULATION',line):
                line = horaire_file.readline()

            horaire_lines = []
            line = horaire_file.readline()
            while not re.search(r'Horaires',line):
                line = horaire_file.readline()

                horaire_lines.append(line)
            horaire = horaire_lines_to_table(table =  horaire_lines)

            chatelet_horaire += horaire['chatelet']

        data = pd.DataFrame(data={'station': ['chatelet'] * len(chatelet_horaire),
                                  'time': chatelet_horaire,
                                  'jour': 'semaine',
                                  'period':'nov_2017'},
                            columns=['station', 'time', 'jour','period'])

        for i in range(16):
            line = horaire_file.readline()
            while not re.search(r'CIRCULATION',line):
                line = horaire_file.readline()

            horaire_lines = []
            line = horaire_file.readline()
            while not re.search(r'Horaires',line):
                line = horaire_file.readline()

                horaire_lines.append(line)
            horaire = horaire_lines_to_table(table =  horaire_lines)

            chatelet_horaire += horaire['chatelet']

        data = pd.DataFrame(data={'station': ['chatelet'] * len(chatelet_horaire),
                                  'time': chatelet_horaire,
                                  'jour': 'semaine',
                                  'period':'jan_2018'},
                            columns=['station', 'time', 'jour','period'])

        chatelet_horaire = []

        for i in range(13):
            line = horaire_file.readline()
            while not re.search(r'CIRCULATION',line):
                line = horaire_file.readline()


            horaire_lines = []
            line = horaire_file.readline()
            while not re.search(r'Horaires',line) and line != '':
                line = horaire_file.readline()
                print(line)
                horaire_lines.append(line)
            horaire = horaire_lines_to_table(table =  horaire_lines)

            chatelet_horaire += horaire['chatelet']
        data2 = pd.DataFrame(data={'station': ['chatelet'] * len(chatelet_horaire),
                                   'time': chatelet_horaire,
                                   'jour': 'ferie',
                                   'period':'nov_2017'},
                             columns=['station', 'time', 'jour','period'])

        data = pd.concat((data, data2), axis=0)
        data.to_csv(file + '.csv', index=False)