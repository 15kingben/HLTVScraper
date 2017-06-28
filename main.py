import sys
from bs4 import BeautifulSoup
import urllib.request
import requests
import re

import datetime
import sqlite3
import time


def getRounds(ls):
    for i in range(0, len(ls)):
        ls[i] = ls[i].replace('(', "")
        ls[i] = ls[i].replace(')', "")
    team2TRounds = float(ls[1].split(':')[1])
    team1CTRounds = float(ls[1].split(':')[0])

    team2CTRounds = 0
    team1TRounds = 0

    if(len(ls)>2):  #16-0
        team2CTRounds = float(ls[2].split(':')[1])
        team1TRounds = float(ls[2].split(':')[0])

    team1Total = team1TRounds + team1CTRounds
    team2Total = team2TRounds + team2CTRounds

    if(len(ls) > 3): #OT
        team1Total += float(ls[3].split(':')[0])
        team2Total += float(ls[3].split(':')[1])

    team1TRatio = team1TRounds / (team1TRounds + team2CTRounds)
    team1CTRatio = team1CTRounds / (team1CTRounds + team2TRounds)
    team2TRatio = team2TRounds / (team2TRounds + team1CTRounds)
    team2CTRatio = team2CTRounds / (team2CTRounds + team1TRounds)

    return team1Total, team2Total, team1TRatio, team1CTRatio, team2TRatio, team2CTRatio

def getRoundsPistol(roundsDiv):
    imgs = roundsDiv.find_all('img')
    winPistol = 0
    half_divs = roundsDiv.find_all(class_='round-history-half')
    for half in half_divs:
        half_divs_imgs = half.find_all('img')
        if not 'empty' in half_divs_imgs[0]['src']:
            winPistol += 1

    numTElims = 0
    numCTElims = 0
    numBombDefuses = 0
    numExps = 0

    for img in imgs:
        if 'ct_win' in img['src'] or "stopwatch" in img['src']:
            numCTElims += 1
        elif "bomb_defused" in img['src']:
            numBombDefuses += 1
        elif "t_win" in img['src']:
            numTElims += 1
        elif "explod" in img['src']:
            numExps += 1

    return winPistol, numTElims, numCTElims, numBombDefuses, numExps




def parse_player_table(table):
    team_players = {}
    rows = table.find_all('tr')
    for i in range(1, len(rows)):
        skip=False
        row = rows[i]
        player_id = row.find(class_='st-player').a['href']
        player_stats = {}
        for td in row.find_all('td'):
            if td.text == '-':
                skip = True
                break
            else:
                player_stats[td['class'][0]] = td.text
        if skip:
            continue
        team_players[player_id] = player_stats

    return team_players



def parse_map_page(soup_map_page, url, mapname):

    match_map_id = str(re.search('matches/[0-9]*', url).group(0))
    match_map_id = match_map_id.split('/')[1]
    if match_map_id == "":
        match_map_id = str(re.search('matches/mapstatsid/[0-9]*', url).group(0))
        match_map_id = match_map_id.split('/')[2]
    matchInfoBox = soup_map_page.find(class_='match-info-box')

    eventBox = matchInfoBox.a
    eventName = eventBox.text
    eventLink = eventBox['href']


    metaDataBox = matchInfoBox.find(class_='small-text')
    metaDataBox = metaDataBox.find_all('span')
    date_time = metaDataBox[0].text

    team_left = {}
    team_right = {}

    team_left['name'] = soup_map_page.find(class_='team-left').a['href']   #.img['title']
    team_right['name'] = soup_map_page.find(class_='team-right').a['href']    #.img['title']

    print(team_left['name'] + ' vs. ' + team_right['name'])
    print(match_map_id)
    print(eventName)
    print(eventLink)
    print(date_time)
    print(mapname)


    # team1Total, team2Total, team1TRatio, team1CTRatio, team2TRatio, team2CTRatio = getRounds(divText[8])
    match_info_rows = soup_map_page.find_all(class_='match-info-row')
    if len(match_info_rows) >= 4:  #multi-map
        first_kills = match_info_rows[2]
        clutches = match_info_rows[3]
    else:
        first_kills = match_info_rows[1]
        clutches = match_info_rows[2]

    first_kills = first_kills.div.text.split(':')
    clutches = clutches.div.text.split(':')

    team_left['first_kills'] = int(first_kills[0])
    team_right['first_kills'] = int(first_kills[1])
    team_left['clutches'] = int(clutches[0])
    team_right['clutches'] = int(clutches[1])


    print(team_left, team_right)



    roundsDiv = soup_map_page.find_all(class_='round-history-team-row')
    if roundsDiv == [] or roundsDiv == None: #probably a forfeit, technical difficulties
        print('skipping' + match_map_id)
        return

    count=0
    team1Pistol, team2Pistol, team1TElims, team2TElims, team1CTElims, team2CTElims, team1BombDefusals, team2BombDefusals, team1Exps, team2Exps = 0,0,0,0,0,0,0,0,0,0


    for roundDiv in roundsDiv:
        winPistol, numTElims, numCTElims, numBombDefuses, numExps = getRoundsPistol(roundDiv)
        # team1Pistol += winPistol
        # team2Pistol += 1 - winPistol
        if count == 0:
            team_left['win_pistol'] = winPistol
            team_left['T_elims'] = numTElims
            team_left['CT_elims'] = numCTElims
            team_left['bomb_defused'] = numBombDefuses
            team_left['bomb_exp'] = numExps
            team_left['CT_wins'] = numCTElims + numBombDefuses
            team_left['T_wins'] = numTElims + numExps
            team_left['total_rounds'] = numTElims + numExps + numCTElims + numBombDefuses
        else:
            team_right['win_pistol'] = winPistol
            team_right['T_elims'] = numTElims
            team_right['CT_elims'] = numCTElims
            team_right['bomb_defused'] = numBombDefuses
            team_right['bomb_exp'] = numExps
            team_right['CT_wins'] = numCTElims + numBombDefuses
            team_right['T_wins'] = numTElims + numExps
            team_right['total_rounds'] = numTElims + numExps + numCTElims + numBombDefuses
        count+=1

    print("Pistols: ", team_left['win_pistol'], ":", team_right['win_pistol'])
    print(team_left, team_right)

    team_stats_tables = soup_map_page.find_all(class_='stats-table')

    team_left_player_stats = parse_player_table(team_stats_tables[0])
    team_right_player_stats = parse_player_table(team_stats_tables[1])

    print(team_left_player_stats, team_right_player_stats)


    for i in team_left_player_stats:
        l = team_left_player_stats
        entry = (match_map_id, mapname, i, team_left['name'], float(l[i]['st-adr']) , int(l[i]['st-kddiff']) , int( l[i]['st-kills'].split()[0]) ,  float(l[i]['st-kdratio'].replace("%" , ""))/100 ,  int(l[i]['st-assists']) , float(l[i]['st-rating']) , int(l[i]['st-deaths']) )

        c.execute("INSERT INTO player_score VALUES(?,?,?,?,?,?,?,?,?,?,?)" , entry)

    for i in team_right_player_stats:
        l = team_right_player_stats
        entry = (match_map_id, mapname, i, team_right['name'], float(l[i]['st-adr']) , int(l[i]['st-kddiff']) , int( l[i]['st-kills'].split()[0]) ,  float(l[i]['st-kdratio'].replace("%" , ""))/100 ,  int(l[i]['st-assists']) , float(l[i]['st-rating']) , int(l[i]['st-deaths']) )

        c.execute("INSERT INTO player_score VALUES(?,?,?,?,?,?,?,?,?,?,?)" , entry)



    entry = (match_map_id, mapname, eventLink, date_time, "unused", \
        team_left['name'], team_right['name'], team_left['first_kills'], team_right['first_kills'],\
        team_left['clutches'], team_right['clutches'], team_left['win_pistol'], team_right['win_pistol'], \
        team_left['T_elims'], team_right['T_elims'], team_left['CT_elims'], team_right['CT_elims'], \
        team_left['bomb_defused'], team_right['bomb_defused'], team_left['bomb_exp'], team_right['bomb_exp'],\
        team_left['T_wins'], team_right['T_wins'], team_left['CT_wins'], team_right['CT_wins'],\
        team_left['total_rounds'], team_right['total_rounds'])
    c.execute("INSERT IfNTO maps VALUES(?,?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,? )", entry)
    conn.commit()



def parse_simple_map_page(soup_match_page, url):
    match_id_base = url.split('/')[2]

    teamBox = soup_match_page.find(class_="teamsBox")
    if teamBox == None:  # page deleted
        print("skipping", url)
        return
    timeEventBox = teamBox.find(class_="timeAndEvent")
    teamLeftBox = teamBox.find_all(class_="team")[0]
    teamRightBox = teamBox.find_all(class_="team")[1]

    date_time = timeEventBox.find(class_="date").text
    date_time = date_time.replace("th", "").replace('st', "").replace("rd", "").replace("nd", "").replace("of ", "").replace('Augu', 'August')
    time = timeEventBox.find(class_="time").text

    date_time = datetime.datetime.strptime(date_time + " " + time + ":00", "%d %B %Y %X")
    date_time = date_time.isoformat().replace("T", " ")[:-3]

    eventLink = timeEventBox.find(class_="event").a['href']

    teamLeft = teamLeftBox.find(class_="team1-gradient").a['href']
    teamRight = teamRightBox.find(class_="team2-gradient").a['href']

    # Forgetting about the different naming structure and team histories starting over -- maybe it will help it be resistant to roster changes


    print(match_id_base)


    print(date_time, eventLink, teamLeft, teamRight)


    mapholder = soup_match_page.find_all(class_="mapholder")

    count = 0
    for m in mapholder:


        count+=1
        if m.find(class_="optional") != None:
            continue
        mapname = m.find(class_="mapname").text
        if mapname == "Default":
            continue
        spans = m.find(class_="results")
        if spans != None:
            spans = spans.find_all("span")
        else:
            return
        if spans == None:
            return
        for s in spans:
            if s.text == "; -:-":
                return

        teamLeftTRounds = 0
        teamRightTRounds = 0
        teamLeftCTRounds = 0
        teamRightCTRounds = 0

        if spans[4].class_ == 't':
            teamLeftTRounds += int(spans[4].text)
            teamLeftCTRounds += int(spans[8].text)
            teamRightCTRounds += int(spans[6].text)
            teamRightTRounds += int(spans[10].text)
        else:
            teamLeftCTRounds += int(spans[4].text)
            teamLeftTRounds += int(spans[8].text)
            teamRightTRounds += int(spans[6].text)
            teamRightCTRounds += int(spans[10].text)

        teamLeftTotalRounds = teamLeftTRounds + teamLeftCTRounds
        teamRightTotalRounds = teamRightTRounds + teamRightCTRounds



        match_map_id = match_id_base + '_'  + str(count)

        entry = (match_map_id, mapname, eventLink, date_time, "unused", \
            teamLeft, teamRight, -1, -1,\
            -1, -1, -1, -1, \
            -1, -1,-1,-1, \
            -1,-1,-1,-1,\
            teamLeftTRounds, teamRightTRounds, teamLeftCTRounds, teamRightCTRounds,\
            teamLeftTotalRounds, teamRightTotalRounds)
        print(entry)
        if c.execute("SELECT * FROM maps WHERE MatchID = ? and MapName = ?", (match_map_id, mapname)).fetchone() != None:
            print("skipping")
        else:
            c.execute("INSERT INTO maps VALUES(?,?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?,?, ?,? )", entry)







    conn.commit()





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



BASE_URL = 'http://www.hltv.org/results'
SITE_URL = 'http://hltv.org'
REQUEST_URL = 'http://www.hltv.org/?pageid=324&filter=1&clean=1'

request_params = {'vod' : 'false', 'intersect' : 'false', 'highlight': 'false', 'stats' : 'true', 'demo' : 'false' , 'offset' : '0', 'daterange' : '2017-03-04 to 2017-03-05'}

conn = sqlite3.connect('csgo.db')
c = conn.cursor()

session = requests.Session()

count = 0
for offset in range(24100, 24500, 100):
    print("offset = ", offset)
    r = session.get(BASE_URL + "?offset=" + str(offset), headers={'User-Agent' : 'Definitely Not Scraping'})

    print(r.status_code)
    print(r.url)
    soup = BeautifulSoup(r.text, 'lxml')
    sublists = soup.find_all(class_='results-sublist')

    for dateList in sublists:
        dateItem = dateList.find(class_="standard-headline")
        matchDate  = dateItem.text
        print(matchDate)

        matches = dateList.find_all(class_="result-con")
        for match in matches:
            link = match.a['href']
            print(link)






            if c.execute("SELECT * FROM matches WHERE Link = ?" , (link,)).fetchone() != None and offset != 11400:
                print('skipping' + link)
                continue
            else:
                if offset != 11400:
                    c.execute('INSERT INTO matches VALUES(?)', (link,))




            resp = session.get(SITE_URL + link)
            soup_match_page = BeautifulSoup(resp.text, 'lxml')
            # gotv_demo_page = session.get(SITE_URL + gotv_demo_link).text

            # soup_match_page = BeautifulSoup(gotv_demo_page, 'lxml')



            if offset >= 11400:
                # Old style
                url = link
                parse_simple_map_page(soup_match_page, url)

                continue


            for l in soup_match_page.find_all('a'):
                if 'GOTV' in l.text:
                    gotv_demo_link = l['href']

            detailed_stats = soup_match_page.find(class_=re.compile('stats-detailed-stats'))
            if(detailed_stats == None): # Forfeit maybe?
                print('skipping' + link)
                continue
            else:
                detailed_stats = detailed_stats.a['href']


            print("detailed_stats = " + detailed_stats)
            match_link = detailed_stats.split('/')
            match_link = '/'.join( match_link[len(match_link) - 2:] )
            print(match_link)

            map_names = soup_match_page.find(class_='mapholder').find_all(class_='mapname')


            detailed_stats_response = session.get(SITE_URL + detailed_stats)
            soup_detailed_stats_page = BeautifulSoup( detailed_stats_response.text, 'lxml')

            print(detailed_stats_response.url)

            maps = soup_detailed_stats_page.find(class_='stats-match-maps')


            if maps.text == "":
                mapname = map_names[0].text # m.find(class_='stats-match-map-result-mapname').text
                mapname = MAPS_TLAS[mapname]
                parse_map_page(soup_detailed_stats_page, detailed_stats_response.url, mapname)
            else:
                maps = maps.find_all(class_='stats-match-map')
                for i in range(1, len(maps)):   # skip match summary
                    m = maps[i]
                    if m.text == "":
                        continue
                    mapname = m.find(class_='stats-match-map-result-mapname').text
                    resp = session.get(SITE_URL + m['href'])
                    url = resp.url
                    soup_map_page = BeautifulSoup( resp.text, 'lxml')
                    parse_map_page(soup_map_page, url, mapname)
            time.sleep(5)

    conn.commit()

conn.close()
