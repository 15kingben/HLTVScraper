import sys
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import datetime
import sqlite3
import time

MIN_MAP_COUNT = 5

BASE_URL = 'http://www.hltv.org/stats/players'
SITE_URL = 'http://hltv.org'

request_params = {'vod' : 'false', 'intersect' : 'false', 'highlight': 'false', 'stats' : 'true', 'demo' : 'false' , 'offset' : '0', 'daterange' : '2017-03-04 to 2017-03-05'}

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

session = requests.Session()

currentDate = datetime.date(2012, 9, 6)

conn = sqlite3.connect('csgo_backup.db')
c = conn.cursor()

while currentDate < datetime.date.today() - datetime.timedelta(days = 2*30):


    startDate = currentDate
    endDate = currentDate + datetime.timedelta(days = 1*30)

    midDate = currentDate + datetime.timedelta(days = .5*30)
    # midDate = midDate + datetime.timedelta(days=15)

    r = session.get(BASE_URL + "?startDate=" + str(startDate.isoformat()) + '&endDate=' + str(endDate.isoformat()) + '&minMapCount=' + str(MIN_MAP_COUNT), headers={'User-Agent' : USER_AGENT})

    print('poop')

    soup_team_ratings = BeautifulSoup(r.text, 'lxml')
    team_ratings = soup_team_ratings.find(class_='player-ratings-table').find_all('tr')

    for i in range(1, len(team_ratings)):
        row = team_ratings[i]
        cols = row.find_all('td')

        player_name = cols[0].a['href'].split('?')[0]
        if cols[1].a != None:
            team_name = cols[1].a['href'].split('?')[0]
        else:
            team_name = "no_team"
        num_maps = cols[2].text
        kd_diff = cols[3].text
        kd_ratio = cols[4].text
        team_rating = cols[5].text

        entry = (player_name, team_name, midDate, num_maps, kd_diff, kd_ratio, team_rating  )
        print(entry)
        c.execute("INSERT INTO player_history VALUES(?, ?, ?, ?, ?, ?, ? )", entry)



    print(currentDate.isoformat())
    conn.commit()
    currentDate += datetime.timedelta(days = 30*1)
    time.sleep(5)

conn.close()
