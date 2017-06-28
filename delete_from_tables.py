import sys
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import datetime
import sqlite3
import time



conn = sqlite3.connect('csgo.db')
c = conn.cursor()

ls = c.execute("SELECT MatchID, MapName, MatchDate FROM maps")


for entry in ls.fetchall():
    if "-" not in entry[2]:
        print(entry)
        c.execute("DELETE FROM maps WHERE MatchID = ? AND MapName = ?", (entry[0], entry[1]))

conn.commit()

conn.close()
