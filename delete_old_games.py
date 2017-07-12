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

# maps = c.execute("SELECT TeamLeftTotalRounds, TeamRightTotalRounds, MatchID FROM maps")
#
# for m in maps.fetchall():
#     if m[0] + m[1] < 15:
#         x = c.execute("SELECT * FROM maps WHERE MatchID = ?", (m[2],)).fetchall()
#         # c.execute("DELETE FROM maps WHERE MatchID = ?", (m[2],))
#         print(x)
#     conn.commit()

maps = c.execute("SELECT * FROM maps")

for m in maps.fetchall():
    if m[1] in MAPS_TLAS:
        print('deleting', m)
        c.execute("DELETE FROM maps WHERE MatchID = ? AND MapName = ?", (m[0] , m[1]) )
        n = list(m)
        n[1] = MAPS_TLAS[n[1]]
        print('adding', tuple(n) )
        c.execute("INSERT INTO maps VALUES(?,?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,? )", n)

conn.commit()
