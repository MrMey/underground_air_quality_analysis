import requests
import bs4
import pandas as pd

base = "http://www.historique-meteo.net/france/ile-de-france/paris/"

def get_html(url):
	req = requests.get(url)
	soup = bs4.BeautifulSoup(req.text,'lxml')
	result = soup.find('table',attrs = {'class':u'table table-striped'})
	return result

def makelist(table):
  result = []
  allrows = table.findAll('tr')
  for row in allrows:
    result.append([])
    allcols = row.findAll('td')
    for col in allcols:
      thestrings = [unicode(s) for s in col.findAll(text=True)]
      thetext = ''.join(thestrings)
      result[-1].append(thetext)
  return result

def process_html_table(result):
	table = makelist(result)

	table = pd.DataFrame(table)
	table = table.drop(labels = [0],axis = 0)
	table = table.drop(labels = [1,4],axis = 1)
	table['temperature'],table['precipitation'] = table[2].str.split('Pr',1).str

	table['temperature'] = table['temperature'].apply(lambda x: x.split(':')[-1])
	table['temp_min'],table['temp_max'] = table['temperature'].str.split('/',1).str
	table['temp_min'] = table['temp_min'].apply(lambda x: x[:-2])
	table['temp_max'] = table['temp_max'].apply(lambda x: x[:-2])


	table['precipitation'] = table['precipitation'].apply(lambda x: x.split(':')[-1])
	table['precipitation'] = table['precipitation'].apply(lambda x: x[:-2])

	table['date'] = table[0]
	table = table.drop(labels = [0,2,3,'temperature'], axis = 1)
	return table

data = pd.DataFrame()

for year in range(2013,2017):
	for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
		url = base + '/' + str(year) + '/' + month + '/'
		print(url)
		html = get_html(url)

		print(html)
		table = process_html_table(html)
		data = pd.concat([data,table])

print(data)
data.to_csv('meteo_paris.csv',index = False)