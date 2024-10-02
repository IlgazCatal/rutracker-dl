'''
rutracker-dl - An Easy And Efficient Downloader for rutracker.org
Created by Ilgaz Çatal - github.com/IlgazCatal
License - GPL v2.0
'''

'''
TODO:

[X] use regex to MATCH the album title 
[] cleanup code
[] add torrent viewer 

'''

import qbittorrentapi
import requests
from bs4 import BeautifulSoup
from sys import argv
from urllib.parse import urlparse, parse_qs, unquote
from os import listdir, unlink
from re import search

# instantiate qbittorrent client
conn_info = dict(
        host="localhost",
        port=8080,
        username="admin",
        password="adminadmin",
        )
qb = qbittorrentapi.Client(**conn_info)

try:
    qb.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e) # Check login creds


arg = argv[1] if len(argv) < 2 else '+'.join(argv[1:]) # Search queries use "+" to seperate words.
link = f"https://html.duckduckgo.com/html/?q={arg}" + '+site:rutracker.org'

response = requests.get(link,headers={'user-agent': 'my-app/0.0.1'})

with open("res.html",'w+') as f: # Saves the text of the response to a html file.
    if search(f"{arg}+",response.text):
        f.write(response.text)
        f.close()

def get_html():
    with open("res.html") as resp:
        soup = BeautifulSoup(resp,"lxml") # lxml is the fastest parser
        resp.close()

    links = [node.get('href') for node in soup.find_all("a")]
    url_obj = urlparse(links[2])
    parsed_url = parse_qs(url_obj.query).get('uddg', '')
    main_url = unquote(parsed_url[0]) 
    url_content = requests.get(main_url,headers={'user-agent': 'my-app/0.0.1'}).text

    with open("rutracker.html","w+") as f:
        f.write(url_content)
        f.close()

def get_magnet():
    with open("rutracker.html") as r:
        soup = BeautifulSoup(r,"lxml")
        r.close()

    #Retrieve magnet url from href tags
    magnet_url = [node.get('href') for node in soup.find_all("a")]
    magnet_list = [item for item in magnet_url if 'magnet:' in str(item)]

    #Download 
    qb.torrents_add(urls=magnet_list[0])

def cleanup():
    for h in listdir():
        if ".html" in h:
            unlink(h)

get_html()
get_magnet()
cleanup()
