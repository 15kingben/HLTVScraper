import sys
from bs4 import BeautifulSoup
import urllib.request
import requests
import re

import datetime
import sqlite3
import time

MAPS_TLAS = { 'Overpass' : 'ovp',
'Cache' : 'cch',
'Nuke' : 'nuke',
'Train' : 'trn',
'Mirage' : 'mrg',
'Cobblestone' : 'cbl',
'Inferno' : 'inf',
'Dust2' : 'd2',
'Tuscan' : 'tcn',
'Season' : 'ssn'
}



# team lifetime winrate on map
conn = sqlite3.connect('csgo.db')
c = conn.cursor()

teams = c.execute("SELECT TeamLeft, TeamRight FROM maps")

all_teams = set()

for row in teams.fetchall():
    if row[0] not in all_teams:
        all_teams.add(row[0])
    if row[1] not in all_teams:
        all_teams.add(row[1])

# print(all_teams)




mapnames = MAPS_TLAS.values()


for team in all_teams:
    mapscore = {}
    for m in mapnames:
        print(mapnames)
        mapscore[m] = 0
        c.execute("SELECT TeamLeft, TeamRight, TeamLeftTotalRounds, TeamRightTotalRounds FROM maps WHERE MapName = ? AND (TeamLeft = ? OR TeamRight = ?)" , (m, team, team))
        print(len(c.fetchall()))
        count = 0
        for result in c:
            count+=1
            assert ((result[2]) >= 15 or (result[3]) >= 15)
            # count ties as .5 win
            if result[2] == result[3]:
                mapscore[m] += .5
            elif (result[2] > result[3] and result[0] == team) or (result[2] < result[3] and result[1] == team):
                mapscore[m] += 1

        if mapscore[m] <= 2:
            mapscore[m] = .5
        else:
            mapscore[m] /= float(count)
    print(team)
    print(mapscore)
    for m in mapscore:
        c.execute("INSERT INTO map_affinity VALUES(?,?,?)", (team, m, mapscore[m]))


conn.commit()


# MAPS_TLAS = { 'Overpass' : 'ovp',
# 'Cache' : 'cch',
# 'Nuke' : 'nuke',
# 'Train' : 'trn',
# 'Mirage' : 'mrg',
# 'Cobblestone' : 'cbl',
# 'Inferno' : 'inf',
# 'Dust2' : 'd2',
# 'Tuscan' : 'tcn',
# 'Season' : 'ssn'
# }
#
#
#
# # team lifetime winrate on map
# conn = sqlite3.connect('csgo.db')
# c = conn.cursor()
#
# teams = c.execute("SELECT DISTINCT Team_ID FROM team_history")
#
# mapnames = MAPS_TLAS.values()
#
#
# for t in teams.fetchall():
#     teamName = t[0].split('/')[-1]
#     print(teamName)
#     print(t[0])
#     c.execute("INSERT INTO team_names VALUES(?,?)", (teamName, t[0]))
#
# # conn.commit()
