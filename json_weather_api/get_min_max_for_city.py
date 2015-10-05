'''

Open Weather Api is a json weather api to get weather data for most major cities.

In this exercise we are going to populate a small local database with all the min and max temperatures for last 16 days for a city.

We will use a json api to get the data, then store parts of that data in sqlite, which is small sql database.

Steps:

1) First inspect what is returned in json_data. You can use python print statements also download and use the chrome json formatter: https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en 

2) The data returned has a key "list" which is an array of hashes (horray!). Each element in the array is one day's temp info.

3) Write a loop to print out each days "min" and "max" temp as well as the "dt" key. dt is short for datetime.

DB)

4) Create a table to store this information. The table should be able to store

- id sql field type - INTEGER PRIMARY KEY
- city_name  sql field type - text
- datetime (dt) sql field type - text
- min_temp  sql field type - real
- max_temp  sql field type- real

5) Refactor your loop so that instead of just printing it inserts new rows for each day into the table.

6) Write queries to find the day with lowest temperature and the highest.

7) Write a query to find the average temp.

Extension:

Expand the code to be able to ask a user for a city, then populate the db with that cities data. 
Then allow the user to find maxes for one city or across all cities.


Further Reading:

http://zetcode.com/db/sqlitepythontutorial/

'''

import requests
import sqlite3

#INSERT INTO songs VALUES ("My Way", "Greatest Hits", "Frank Sinatra")
def db_open(filename):
    return sqlite3.connect(filename)

def db_create(conn):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS weather")
    c.execute('''CREATE TABLE weather(id INTEGER PRIMARY KEY, city_name text, daytime text, min_temp real, max_temp real);''')
    conn.commit()

def db_insert(conn, city, time, min_, max_):
    c = conn.cursor()
    c.execute('''INSERT INTO weather(city_name,daytime,min_temp,max_temp) VALUES (\'%s\',%f,%f,%f);''' % (city, time, min_, max_))
    conn.commit()

def find_min_max_avg(conn):
	c=conn.cursor()
	min_ = c.execute('''SELECT daytime, MIN(min_temp) FROM weather;''').fetchall()[0][1]
	max_ = c.execute('''SELECT daytime, MAX(max_temp) FROM weather;''').fetchall()[0][1]
	min_avg = c.execute('''SELECT AVG(min_temp) FROM weather;''').fetchall()[0][0]
	max_avg = c.execute('''SELECT AVG(max_temp) FROM weather;''').fetchall()[0][0]
	avg = 0.5*(min_avg + max_avg)
	return min_, max_, avg

def db_close(conn):
    conn.close()

answer =''
while answer != 'q':
	answer = raw_input('Name the city: ')
	if answer == 'q':
		break
	url = "http://api.openweathermap.org/data/2.5/forecast/daily?mode=json&units=metric&q=%s&cnt=16" % answer
	json_data = requests.get(url).json()

	conn = db_open('weather.db')
	db_create(conn)

	for i in json_data['list']:
		db_insert(conn, answer, i['dt'], i['temp']['min'], i['temp']['max'])

	min_, max_, avg = find_min_max_avg(conn)

	print min_, max_, avg







