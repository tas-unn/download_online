import urllib

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

import requests

site='https://www.u-tv.ru/shows/zhduli/'
req = Request(site)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")
names=[]
links=[]
for x in soup.findAll('a'):
    if x.text.count('сезон')==1 and x.text.count('серия')==1:
        link = str(x.get('href'))
        r = requests.get(url=link)
        f=False
        for st in r.text.split('\n'):
            if st.count('<title>')==1:
                title = re.sub(r"<[^>]+>", "", st, flags=re.S).strip()


            if f:
                names.append(title)
                link2=st.split('"')[1]
                if link2.count('rutube.ru')==1:
                    links.append('https://rutube.ru/video/'+link2.split('/')[5].split('?')[0])
                r1 = requests.get(url=link2)
                for st in r1.text.split('\n'):
                    if st.count('m3u8') == 1 :
                        links.append(st.split('"')[3])

                break
            if st.count('id="gplayer"')==1:
                f=True

file = open("1.cmd", "w")


for i in range(len(links)):
  print('yt-dlp.exe -o "'+names[i]+'" '+links[i])
  file.write('yt-dlp.exe -o "'+names[i]+'" '+links[i]+'\n')
file.close()
print('Создан файл 1.cmd')
