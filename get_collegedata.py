
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_top_college_data ():
    base_url = 'https://www.sports-reference.com'
    player_url = []
    set_urls = set()
    with open("collegedata.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        for elmnt in soup.find_all('td', {'class': 'who'}) :
            child = elmnt.find("a" , recursive=False)
            url = base_url + child['href']
            if url not in set_urls:
                set_urls.add(url)
                player_url.append(url)
    
    frames = []
    print(len(player_url))
    for i, url in enumerate(player_url) :
        web = requests.get(url)
        soup = BeautifulSoup(web.content, 'html.parser')
        player_info  = soup.find(id='meta')
        name = player_info.find('h1', {'itemprop' : 'name'}).find('span').getText()
        weight = player_info.find('span', {'itemprop' : 'weight'}).getText()
        height = player_info.find('span', {'itemprop' : 'height'}).getText()

        tables = pd.read_html(url)
        college_stats = tables[0].iloc[-1].copy()
        college_stats['name'], college_stats['weight'], college_stats['height'] = name, weight, height
        frames.append(college_stats)
        print(i)
    return pd.DataFrame(frames)

top_college_data = get_top_college_data()
top_college_data.to_csv('top_college_data.csv', encoding='utf-8')
