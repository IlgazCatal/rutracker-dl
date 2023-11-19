'''
rutracker-dl - An Easy And Efficient Downloader for rutracker.org
Created by Ilgaz Çatal - github.com/IlgazCatal
License - idk now
'''

'''
TODO:
[X] Make bs4 access the links 
[] Implement a way to get and download the magnet link using qbittorrent's api. Optionally, implement a viewer for the download.
'''

from bs4 import BeautifulSoup
import sys
import qbittorrentapi
import requests
from urllib.parse import urlparse, parse_qs, unquote

## qbittorrent client instantiation, edit to your needs!!
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


arg = sys.argv[1] if len(sys.argv) < 2 else '+'.join(sys.argv[1:]) # Search queries use "+" to seperate words.
link = f"https://html.duckduckgo.com/html/?q={arg}" + '+site:rutracker.org'

response = requests.get(link,headers={'user-agent': 'my-app/0.0.1'})

with open("res.html",'w+') as f: # Saves the text of the response to a html file.
    f.write(response.text)
    f.close()

def get_rutracker():
    with open("res.html") as resp:
        soup = BeautifulSoup(resp,"html5lib")

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
        soup = BeautifulSoup(r,"html5lib")
    
    magnet_url = [node.get('href') for node in soup.find_all("a")]
    magnet_list = [item for item in magnet_url if 'magnet:' in str(item)]
    
    #Download 
    qb.torrents_add(urls=str(magnet_list[0]))

    #View info 
    torrent_list = dict(qb.torrent_info())
    for k,v in torrent_list:
        if k == "name" and v == "Agalloch":
            print(k,v)
    
get_rutracker()
get_magnet()
