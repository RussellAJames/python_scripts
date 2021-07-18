import ast
import json
import os
import re
import urllib
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.request import urlopen

#table.article-table:first-of-type img

url = 'https://leagueoflegends.fandom.com/wiki/Summoner_spell'

champion_raw_data = urlopen(url)
unparsed_html = champion_raw_data.read()
html = BeautifulSoup(unparsed_html , 'html.parser')
html_sum_img = html.select("table.article-table:first-of-type img")


summoner_img_dict = {}
for i in range(0,len(html_sum_img)-1):
    summoner_img_dict[html_sum_img[i]['alt']]=html_sum_img[i]['data-src']

try: 
    os.mkdir('./LOL-Summoner-Images')

except:
    print('Folder Previously Created...Overwriting')

for i in summoner_img_dict:
    url = summoner_img_dict[i]
    Champion_Name = i
    urllib.request.urlretrieve(url, f"./LOL-Summoner-Images/{Champion_Name}.jpg")

print(f'{len(html_sum_img)} Summoner Portraits added to folder LOL-Summoner-Images')
