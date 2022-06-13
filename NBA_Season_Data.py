from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re
import time
import pandas as pd
from pathlib import Path

Year_Dict = {
    "2020_Season": "https://www.basketball-reference.com/leagues/NBA_2020_totals.html",
        "2021_Season":"https://www.basketball-reference.com/leagues/NBA_2021_totals.html",
        "2022_Season":"https://www.basketball-reference.com/leagues/NBA_2022_totals.html",
}

for season in Year_Dict:

    filename = '/home/russelljames/vscode/python_scripts/NBA_Season_Data_{Year}.csv'.format(Year = season)

    filepath = Path(filename)

    raw_data = urlopen(Year_Dict[season])
    unparsed = raw_data.read()
    Nba_soup = soup(unparsed, 'html.parser')

    string = Nba_soup.select("#totals_stats > tbody")

    ### First Group: Regular Names ex. Stephen Curry, Second Group: First name capitalized ex. JT Thor, 
    ### Third Group: First letter capitalized followed by period ex. P.J. Tucker, Fourth Group: First letter capitalized
    ### followed by apostrophe ex. D'Angelo Russell, Fifth Group: Special character following first letter ex. Dāvis Bertāns
    pattern_name = r'.html\">([A-Z][a-z].+?)\<|.html\">([A-Z]{2}\ [A-Z][a-z].+?)\<|.html\">([A-Z]\.[A-Z].\ [A-Z][a-z].+?)\<|.html\">([A-Z]\'[A-Z].+?)\<|.html\">([A-Z]\w[a-z].+?)\<'

    ### First Group: Regular capitalized team names, Second Group: Culmination of players teams ex. TOT
    pattern_team = r'.html\">([A-Z]{3})\<|data\-stat\=\"team_id\"\>([A-Z]{3})\<'

    ### Player's position and season stats
    pattern_pos = r'data\-stat\=\"pos\"\>(\w+)'
    pattern_games = r'data\-stat\=\"g\"\>([0-9]+)\<'
    pattern_mp = r'data\-stat\=\"mp\"\>([0-9]+)\<'
    pattern_age = r'data\-stat\=\"age\"\>([0-9]+)\<'
    pattern_fg = r'data\-stat\=\"fg\"\>([0-9]+)\<'
    pattern_fga = r'data\-stat\=\"fga\"\>([0-9]+)\<'
    pattern_pts = r'data\-stat\=\"pts\"\>([0-9]+)\<'
    pattern_tov = r'data\-stat\=\"tov\"\>([0-9]+)\<'
    pattern_ast = r'data\-stat\=\"ast\"\>([0-9]+)\<'
    pattern_orb = r'data\-stat\=\"orb\"\>([0-9]+)\<'
    pattern_drb = r'data\-stat\=\"drb\"\>([0-9]+)\<'
    pattern_trb = r'data\-stat\=\"trb\"\>([0-9]+)\<'
    pattern_stl = r'data\-stat\=\"stl\"\>([0-9]+)\<'
    pattern_ft = r'data\-stat\=\"ft\"\>([0-9]+)\<'
    pattern_fta = r'data\-stat\=\"fta\"\>([0-9]+)\<'
    pattern_blk = r'data\-stat\=\"blk\"\>([0-9]+)\<'

    # Lists for removing blanks from different groups
    name_noblanks = []
    team_noblanks = []


    name = re.findall(pattern_name,str(string))
    team = re.findall(pattern_team,str(string))
    position = re.findall(pattern_pos,str(string))
    games = re.findall(pattern_games,str(string))
    minutes_played = re.findall(pattern_mp,str(string))
    age = re.findall(pattern_age,str(string)) 
    field_goals = re.findall(pattern_fg,str(string))          
    field_goal_attempts = re.findall(pattern_fga,str(string))
    points = re.findall(pattern_pts,str(string))
    turnovers = re.findall(pattern_tov,str(string))
    assists = re.findall(pattern_ast,str(string))
    offensive_rebounds = re.findall(pattern_orb,str(string))
    defensive_rebounds = re.findall(pattern_drb,str(string))
    total_rebounds = re.findall(pattern_trb,str(string))
    steals = re.findall(pattern_stl,str(string))
    freethrows = re.findall(pattern_ft,str(string))
    freethrow_attempts = re.findall(pattern_fta,str(string))
    blocks = re.findall(pattern_blk,str(string))

    # Removing blanks from non-found groups
    for i in name:
        
        for f in i:
            if len(f) !=0:
                name_noblanks.append(f)

    for i in team:
        for f in i:
            if len(f) !=0:
                team_noblanks.append(f)





    # Adding to dictionary
    Season_data = {"Player name" :name_noblanks, "Team":team_noblanks,"Position" : position,"Games":games,"Minutes Played":minutes_played,
    "Age":age,"Field Goals":field_goals,"Field Goal Attempts":field_goal_attempts, "Points":points,"Turnover":turnovers,"Assists":assists,
    "Offensive Rebounds":offensive_rebounds,"Defensive Rebounds" :defensive_rebounds, "Total Rebounds":total_rebounds, "Steals":steals,
    "Freethrows":freethrows,"Freethrow Attempts":freethrow_attempts,"Blocks":blocks}

    NBA_df = pd.DataFrame(Season_data)

    # Exporting DataFrame to csv
    NBA_df.to_csv(filepath)