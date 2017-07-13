import sys



import re
import pandas as pd

from datetime import datetime, timedelta
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

tmpidx = ['MatchID',
  'MapName',
  'Event',
  'MatchDate',
  'GOTV_link',
  'TeamLeft',
  'TeamRight',
  'TeamLeftFirstKills',
  'TeamRightFirstKills',
  'TeamLeftClutches',
  'TeamRightClutches',
  'TeamLeftWinPistol',
  'TeamRightWinPistol',
  'TeamLeftTElims',
  'TeamRightTElims',
  'TeamLeftCTElims',
  'TeamRightCTElims',
  'TeamLeftBombDefusals',
  'TeamRightBombDefusals',
  'TeamLeftBombExploded',
  'TeamRightBombExploded',
  'TeamLeftTWins',
  'TeamRightTWins',
  'TeamLeftCTWins',
  'TeamRightCTWins',
  'TeamLeftTotalRounds',
  'TeamRightTotalRounds'
]



def getMonthPerformance(team, match_date):
    md = match_date.isoformat()[:10]
    md_1month = (match_date - timedelta(days = 31)).isoformat()[:10]
    md_3month = (match_date - timedelta(days = 30*3)).isoformat()[:10]
    md_6month = (match_date - timedelta(days = 30*6)).isoformat()[:10]

    maps_1m = c.execute("SELECT * FROM maps WHERE (TeamLeft = ? OR TeamRight = ?) AND MatchDate > ?  AND MatchDate < ?", (team, team, md_1month, md)).fetchall()

    if maps_1m == []:
        TRounds_1m = "NA"
        CTRounds_1m = "NA"
        TotalRounds_1m = "NA"
        Wins_1m = "NA"
        TRoundsRate_1m = "NA"
        CTRoundsRate_1m = "NA"
        TotalRoundsRate_1m = "NA"
        WinsRate_1m = "NA"
    else:
        TRounds_1m = 0
        CTRounds_1m = 0
        TotalRounds_1m = 0
        Wins_1m = 0
        count = 0
        for m in maps_1m:
            count += 1
            if m[idx['TeamLeft']] == team:
                TRounds_1m += m[idx['TeamLeftTWins']]
                CTRounds_1m += m[idx['TeamLeftCTWins']]
                TotalRounds_1m += m[idx['TeamLeftTotalRounds']]
                Wins_1m += (1 if (m[idx['TeamLeftTotalRounds']] >= 16) else 0)
            else:
                TRounds_1m += m[idx['TeamRightTWins']]
                CTRounds_1m += m[idx['TeamRightCTWins']]
                TotalRounds_1m += m[idx['TeamRightTotalRounds']]
                Wins_1m += (1 if (m[idx['TeamRightTotalRounds']] >= 16) else 0)
        TRoundsRate_1m = TRounds_1m / count
        CTRoundsRate_1m = CTRounds_1m / count
        TotalRoundsRate_1m = TotalRounds_1m / count
        WinsRate_1m = Wins_1m / count

    maps_3m = c.execute("SELECT * FROM maps WHERE (TeamLeft = ? OR TeamRight = ?) AND MatchDate > ?  AND MatchDate < ?", (team, team, md_3month, md)).fetchall()

    if maps_3m == []:
        TRounds_3m = "NA"
        CTRounds_3m = "NA"
        TotalRounds_3m = "NA"
        Wins_3m = "NA"
        TRoundsRate_3m = "NA"
        CTRoundsRate_3m = "NA"
        TotalRoundsRate_3m = "NA"
        WinsRate_3m = "NA"
    else:
        TRounds_3m = 0
        CTRounds_3m = 0
        TotalRounds_3m = 0
        Wins_3m = 0
        count = 0
        for m in maps_3m:
            count += 1
            if m[idx['TeamLeft']] == team:
                TRounds_3m += m[idx['TeamLeftTWins']]
                CTRounds_3m += m[idx['TeamLeftCTWins']]
                TotalRounds_3m += m[idx['TeamLeftTotalRounds']]
                Wins_3m += (1 if (m[idx['TeamLeftTotalRounds']] >= 16) else 0)
            else:
                TRounds_3m += m[idx['TeamRightTWins']]
                CTRounds_3m += m[idx['TeamRightCTWins']]
                TotalRounds_3m += m[idx['TeamRightTotalRounds']]
                Wins_3m += (1 if (m[idx['TeamRightTotalRounds']] >= 16) else 0)
        TRoundsRate_3m = TRounds_3m / count
        CTRoundsRate_3m = CTRounds_3m / count
        TotalRoundsRate_3m = TotalRounds_3m / count
        WinsRate_3m = Wins_3m / count

    maps_6m = c.execute("SELECT * FROM maps WHERE (TeamLeft = ? OR TeamRight = ?) AND MatchDate > ?  AND MatchDate < ?", (team, team, md_6month, md)).fetchall()

    if maps_6m == []:
        TRounds_6m = "NA"
        CTRounds_6m = "NA"
        TotalRounds_6m = "NA"
        Wins_6m = "NA"
        TRoundsRate_6m = "NA"
        CTRoundsRate_6m = "NA"
        TotalRoundsRate_6m = "NA"
        WinsRate_6m = "NA"
    else:
        TRounds_6m = 0
        CTRounds_6m = 0
        TotalRounds_6m = 0
        Wins_6m = 0
        count = 0
        for m in maps_6m:
            count += 1
            if m[idx['TeamLeft']] == team:
                TRounds_6m += m[idx['TeamLeftTWins']]
                CTRounds_6m += m[idx['TeamLeftCTWins']]
                TotalRounds_6m += m[idx['TeamLeftTotalRounds']]
                Wins_6m += (1 if (m[idx['TeamLeftTotalRounds']] >= 16) else 0)
            else:
                TRounds_6m += m[idx['TeamRightTWins']]
                CTRounds_6m += m[idx['TeamRightCTWins']]
                TotalRounds_6m += m[idx['TeamRightTotalRounds']]
                Wins_6m += (1 if (m[idx['TeamRightTotalRounds']] >= 16) else 0)
        TRoundsRate_6m = TRounds_6m / count
        CTRoundsRate_6m = CTRounds_6m / count
        TotalRoundsRate_6m = TotalRounds_6m / count
        WinsRate_6m = Wins_6m / count

    return {'TRounds_1m' : TRounds_1m, 'TRoundsRate_1m' : TRoundsRate_1m, \
        'CTRounds_1m' : CTRounds_1m, 'CTRoundsRate_1m' : CTRoundsRate_1m, \
        'TotalRounds_1m': TotalRounds_1m, 'TotalRoundsRate_1m':TotalRoundsRate_1m, \
        'Wins_1m' : Wins_1m, 'WinsRate_1m' : WinsRate_1m, \
        'TRounds_3m' :  TRounds_3m, 'TRoundsRate_3m': TRoundsRate_3m, \
        'CTRounds_3m' : CTRounds_3m, 'CTRoundsRate_3m' : CTRoundsRate_3m,\
        'TotalRounds_3m' : TotalRounds_3m, 'TotalRoundsRate_3m' : TotalRoundsRate_3m,\
        'Wins_3m' : Wins_3m, 'WinsRate_3m' : WinsRate_3m, \
        'TRounds_6m' : TRounds_6m, 'TRoundsRate_6m' : TRoundsRate_6m, \
        'CTRounds_6m' : CTRounds_6m, 'CTRoundsRate_6m' : CTRoundsRate_6m, \
        'TotalRounds_6m' : TotalRounds_6m, 'TotalRoundsRate_6m' : TotalRoundsRate_6m, \
        'Wins_6m' : Wins_6m, 'WinsRate_6m' : WinsRate_6m}


idx = {}

for i in tmpidx:
    idx[i] = tmpidx.index(i)


numRows = 0

dataMatrix = None 

# team lifetime winrate on map
conn = sqlite3.connect('csgo.db')
c = conn.cursor()

maps = c.execute("SELECT * FROM maps")

for m in maps.fetchall():
    # map affinity
    
    print( m[idx['TeamLeftTotalRounds']] , m[idx['TeamRightTotalRounds']] )
    if m[idx['TeamLeftTotalRounds']] > m[idx['TeamRightTotalRounds']]:
        y = 1
    elif m[idx['TeamLeftTotalRounds']] < m[idx['TeamRightTotalRounds']]:
        y = -1
    else:
        y = 0
        assert m[idx['TeamLeftTotalRounds']] == m[idx['TeamRightTotalRounds']]
        
    mapname = m[idx['MapName']]
    teamLeft = m[idx['TeamLeft']]
    teamRight = m[idx['TeamRight']]
    matchDate = m[idx['MatchDate']]
    matchDateText = matchDate.split()[0]
    matchTime = int(matchDate.split()[1][:2])  #hour digits of date
    matchDate = datetime.strptime(matchDate.split()[0] , "%Y-%m-%d")


    # team rating
    teamLeftRating = c.execute("SELECT * FROM team_history WHERE Team_ID = ?", (teamLeft,))
    closestDate = None
    closestEntry = None
    for entry in teamLeftRating.fetchall():
        d = datetime.strptime(entry[1], "%Y-%m-%d")
        if matchDate - d > timedelta(days=0):
            if closestDate is None:
                closestDate = d
                closestEntry = entry
            elif matchDate - d < matchDate - closestDate:
                closestDate = d
                closestEntry = entry
    if closestDate is None:
        teamLeftRating = 1.0
        teamLeftKD = 1.0
        teamLeftDiff = 0
    else:
        teamLeftRating = closestEntry[5]
        teamLeftKD = closestEntry[4]
        teamLeftDiff = closestEntry[3]


    teamRightRating = c.execute("SELECT * FROM team_history WHERE Team_ID = ?", (teamRight,))
    closestDate = None
    closestEntry = None
    for entry in teamRightRating.fetchall():
        d = datetime.strptime(entry[1], "%Y-%m-%d")
        if matchDate - d > timedelta(days=0):
            if closestDate is None:
                closestDate = d
                closestEntry = entry
            elif matchDate - d < matchDate - closestDate:
                closestDate = d
                closestEntry = entry
    if closestDate is None:
        teamRightRating = 1.0
        teamRightKD = 1.0
        teamRightDiff = 0
    else:
        teamRightRating = closestEntry[5]
        teamRightKD = closestEntry[4]
        teamRightDiff = closestEntry[3]


    # is new team
    newTeam = c.execute("SELECT MatchDate FROM maps WHERE TeamLeft = ? OR TeamRight = ? ORDER BY MatchDate ASC LIMIT 1", (teamLeft, teamLeft))
    x = newTeam.fetchone()
    if x is None:
        newTeamLeft = True
    else:
        if datetime.strptime(x[0].split()[0] , "%Y-%m-%d") - matchDate > timedelta(days=60):
            newTeamLeft = False
        else:
            newTeamLeft = True

    newTeam = c.execute("SELECT MatchDate FROM maps WHERE TeamLeft = ? OR TeamRight = ? ORDER BY MatchDate ASC LIMIT 1", (teamRight, teamRight))
    x = newTeam.fetchone()
    if x is None:
        newTeamRight = True
    else:
        if datetime.strptime(x[0].split()[0] , "%Y-%m-%d") - matchDate > timedelta(days=60):
            newTeamRight = False
        else:
            newTeamRight = True


    # time since last match
    lastMatch = c.execute("SELECT MatchDate FROM maps WHERE MatchDate < ? and ( TeamLeft = ? OR TeamRight = ? ) ORDER BY MatchDate DESC LIMIT 1", (matchDateText, teamLeft, teamLeft))
    x = lastMatch.fetchone()
    if x is None:
        teamLeftLastMatch = "NA"
    else:
        teamLeftLastMatch = (matchDate - datetime.strptime(x[0].split()[0] , "%Y-%m-%d")).days

    lastMatch = c.execute("SELECT MatchDate FROM maps WHERE MatchDate < ? and (TeamLeft = ? OR TeamRight = ?) ORDER BY MatchDate DESC LIMIT 1", (matchDateText, teamRight, teamRight))
    x = lastMatch.fetchone()
    if x is None:
        teamRightLastMatch = "NA"
    else:
        teamRightLastMatch = (matchDate - datetime.strptime(x[0].split()[0] , "%Y-%m-%d")).days


    #matches this week
    matchDateMinusWeek = (matchDate - timedelta(days=7)).isoformat()[:10]
    teamLeftThisWeek = c.execute("SELECT COUNT(*) FROM maps WHERE (TeamLeft = ? OR TeamRight = ?) AND MatchDate > ? and  MatchDate < ?",  (teamLeft, teamLeft, matchDateMinusWeek, matchDate)   ).fetchone()[0]
    teamRightThisWeek = c.execute("SELECT COUNT(*) FROM maps WHERE (TeamLeft = ? OR TeamRight = ?) AND MatchDate > ? and MatchDate < ?",  (teamRight, teamRight, matchDateMinusWeek, matchDate)   ).fetchone()[0]



    # map affinity
    map_affinity_left = c.execute("SELECT Winrate FROM map_affinity WHERE Team_ID = ? AND MapName = ?" , ( teamLeft, mapname)).fetchone()
    if map_affinity_left is None:
        map_affinity_left = .5
    else:
        map_affinity_left = map_affinity_left[0]
    map_affinity_right = c.execute("SELECT Winrate FROM map_affinity WHERE Team_ID = ? AND MapName = ?" , ( teamRight, mapname)).fetchone()
    if map_affinity_right is None:
        map_affinity_right = .5
    else:
        map_affinity_right = map_affinity_right[0]


    #map count
    teamLeftMapCount = int(c.execute("SELECT COUNT(*) FROM maps WHERE TeamLeft = ?", (teamLeft,)).fetchone()[0] ) + \
        int(c.execute("SELECT count(*) FROM maps WHERE TeamRight = ?", (teamLeft,)).fetchone()[0] )

    teamRightMapCount = int(c.execute("SELECT COUNT(*) FROM maps WHERE TeamLeft = ?", (teamRight,)).fetchone()[0] ) + \
        int(c.execute("SELECT COUNT(*) FROM maps WHERE TeamRight = ?", (teamRight,)).fetchone()[0] )



    teamLeftMonthlyPerf = getMonthPerformance(teamLeft, matchDate)
    teamRightMonthlyPerf = getMonthPerformance(teamRight, matchDate)

    prflen = len(teamLeftMonthlyPerf)

#    print(mapname, teamLeft, teamRight, matchDateText, matchTime, teamLeftRating , \
#        teamRightRating, teamLeftKD, teamLeftDiff, newTeamLeft, newTeamRight, \
#        teamLeftLastMatch, teamRightLastMatch, teamLeftThisWeek, map_affinity_left, teamLeftMapCount)


    print(numRows)
    numRows += 1


    if dataMatrix is None:
        columns = ['mapname', 'matchTime', 'teamLeftRating', 'teamRightRating', 'teamLeftKD', 'teamRightKD', \
            'teamLeftDiff', 'teamRightDiff', 'newTeamLeft', 'newTeamRight', \
            'teamLeftLastMatch', 'teamRightLastMatch', 'teamLeftThisWeek', 'teamRightThisWeek', \
            'map_affinity_left', 'map_affinity_right']

        columns += ['teamLeft' + i for i in teamLeftMonthlyPerf]
        columns += ['teamRight' + i for i in teamRightMonthlyPerf]
        columns += ['winner']
        dataMatrix = []

    datarow = [mapname, matchTime,  teamLeftRating ,  teamRightRating ,  teamLeftKD ,  teamRightKD , \
         teamLeftDiff ,  teamRightDiff ,  newTeamLeft ,  newTeamRight , \
         teamLeftLastMatch ,  teamRightLastMatch ,  teamLeftThisWeek ,  teamRightThisWeek , \
         map_affinity_left ,  map_affinity_right]

    datarow += [teamLeftMonthlyPerf[i[8:]] for i in columns[16:16+prflen]]
    datarow += [teamRightMonthlyPerf[i[9:]] for i in columns[16+prflen:-1]]
    datarow += [y]
    dataRow = dict(zip(columns, datarow))
    dataMatrix.append(dataRow)



dataMatrix =pd.DataFrame(dataMatrix) 
    
print(dataMatrix)
import pickle
pickle.dump(dataMatrix, open('dataMatrix', 'wb'), pickle.HIGHEST_PROTOCOL)
