import requests
import json
import os

espn_swid = os.environ.get("ESPN_SWID_COOKIE", " ")
espn_s2 = os.environ.get("ESPN_S2_COOKIE", " ")
# eventually the league ID will be a CLI supplied argument or something similar
espn_ff_league_id = os.environ.get("ESPN_FF_LEAGUE_ID", " ")

cookies = {"SWID": espn_swid, "espn_s2": espn_s2}
url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/{espn_ff_league_id}"
params = {"view": "mMatchup"}  # or whatever

# big ups here: https://stmorse.github.io/journal/espn-fantasy-v3.html

schedule_resp = requests.get(url, params=params, cookies=cookies)
schedule = r.json()["schedule"]
## get weekly results
first_week = list()
for game in schedule[:6]:  # 12 team league -> 6 games
    first_week.append(game["away"]["teamId"], game["away"]["totalPoints"])
    first_week.append(game["home"]["teamId"], game["home"]["totalPoints"])

teams_exp_record = dict.fromkeys(team_mapping.keys(), 0)
for idx, team in enumerate(first_week):
    teams_exp_record[team_mapping[team[0]]] += idx


###################
###  Team Info  ###
###################
params = {"view": "mTeams"}
team_resp = requests.get(url, params=params, cookies=cookies)

teams_info = team_resp.json()["teams"]
team_mapping = {
    team["id"]: (team["location"] + " " + team["nickname"]) for team in teams_info
}
team_records = {
    team["id"]: (team["record"]["overall"]["wins"], team["record"]["overall"]["losses"])
    for team in teams_info
}

###################
### League Week ###
###################

params = {"view": "mSchedule"}
league_schedule_resp = requests.get(url, params=params, cookies=cookies)
league_schedule = league_schedule_resp.json()
current_week = league_schedule["status"]["currentMatchupPeriod"]

# for week in range of weeks
# filter down to relevant week
# get team id and score for each game in the week
# from list of games, pull out all scores
# sort by score ascending
# get number of matchups won (index?)
# reduce that down to each teams # won

[
    (game[team]["teamId"], game[team]["totalPoints"])
    for team in ["home", "away"]
    for week_num in range(1, current_week + 1)
    for game in filter(lambda matchup: matchup["matchupPeriodId"] == week_num, schedule)
]