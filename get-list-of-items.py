import ast
import json
import os
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.request import urlopen

# Grab the ItemData HTML and parse it
item_url = 'https://leagueoflegends.fandom.com/wiki/Module:ItemData/data'
item_raw_data = urlopen(item_url)
unparsed_html = item_raw_data.read()
html = BeautifulSoup(unparsed_html , 'html.parser')

## Get text in pre tag
pre = html.find_all('pre')
pre = str(pre)

# Remove some garbage text
item_data = pre.split('t;pre&gt;\nreturn ')[1]

# Remove left and right bracket from keys
pattern = r'\[|\]'
item_data = re.sub(pattern , '', item_data)

# Remove more garbage data and fix syntax for booleans
item_data = item_data.replace('=',':').replace('</pre>', '').replace('-- &lt;/pre&gt;', '').replace('true','True').replace('false', 'False')

# Turn into a dictionary from string
item_dictionary = ast.literal_eval(item_data)

# Turn item dictionary into list
item_list = []
for key, value in item_dictionary.items():
    item_list.append({**value, 'name': key})

# Turn any sets into lists
for item in item_list:
  for key, value in item.items():
    if type(value) is set:
      item[key] = list(value)

# Get username and password from env vars
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

if username is not None and password is not None:
  # Insert into MongoDB
  client = MongoClient(f"mongodb+srv://{username}:{password}@letmeteemo.i0xze.mongodb.net/LetMeTeemo?retryWrites=true&w=majority")
  db = client['LetMeTeemo']
  items = db['items']
  items.insert_many(item_list)
  client.close()
else:
  print("Username or password env variables are not set.")