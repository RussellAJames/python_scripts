import ast
import json
import os
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.request import urlopen

# Grab the ChampionData HTML and parse it
champion_url = 'https://leagueoflegends.fandom.com/wiki/Module:ChampionData/data'
champion_raw_data = urlopen(champion_url)
unparsed_html = champion_raw_data.read()
html = BeautifulSoup(unparsed_html , 'html.parser')

## Get text in pre tag
pre = html.find_all('pre')
pre = str(pre)

# Remove some garbage text
champion_data = pre.split('t;pre&gt;\nreturn ')[1]

# Remove left and right bracket from keys
pattern = r'\[|\]'
champion_data = re.sub(pattern , '', champion_data)

# Remove more garbage data
champion_data = champion_data.replace('=',':').replace('</pre>','').replace('-- Category:Lua','').replace('-- &lt;/pre&gt;','')

# Turn into a dictionary from string
champion_dictionary = ast.literal_eval(champion_data)

# Turn champion dictionary into list
champion_list = []
for key, value in champion_dictionary.items():
    champion_list.append({**value, 'name': key})

# Turn any sets into lists
for champion in champion_list:
  for key, value in champion.items():
    if type(value) is set:
      champion[key] = list(value)

# Serialize object to json formatted string
champion_list = json.dumps(champion_list)

# Turn into a dictionary from string
champion_list = ast.literal_eval(champion_list)

# Get username and password from env vars
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

if username is not None and password is not None:
  # Insert into MongoDB
  client = MongoClient(f"mongodb+srv://{username}:{password}@letmeteemo.i0xze.mongodb.net/LetMeTeemo?retryWrites=true&w=majority")
  db = client['LetMeTeemo']
  champions = db['champions']
  champions.insert_many(champion_list)
  client.close()
else:
  print("Username or password env variables are not set.")