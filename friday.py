import urllib

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import os
import requests


site='https://na-nozhah.friday.ru/'
req = Request(site)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")
seasonlinks=[]
seasonname=[]
print('Получаем ссылки на все сезоны')
for link in soup.findAll('a'):
  s = str(link.get('href'))
  if (s.count('#seasons') and str(link.text).count('Сезон')):
    seasonlinks.append(s)
    seasonname.append(str(link.text))
    #break # убрать решётку в начале строки, если необходимо скачать все сезоны, а не только последний
if len(seasonlinks)==0:
  seasonlinks.append(site+'/videos/s1#seasons')
  seasonname.append('Сезон 1')
print('Получено сезонов: ' + str(len(seasonlinks)))
episodelinks=[]
for season in range(len(seasonlinks)):
  req = Request(seasonlinks[season])
  html_page = urlopen(req)

  soup = BeautifulSoup(html_page, "lxml")
  for link in soup.findAll('div'):
    s = str(link.get('data-load-more-filter'))
    if (s.count('folder')>0):
      data = json.loads(s)
      page=0
      cou = 0
      while True:

        r=requests.post(site+'api/show/season-video', data={'action': 'get_new',
        'data[page]': str(page),
        'data[filter][name]': ''+data["name"]+'',
        'data[filter][folder]': ''+data["folder"]+'',
        'data[filter][is_num]': 'false',
        'data[filter][season]': ''+str(data["season"])+'',
        'data[filter][single]': 'false',
        'data[filter][hasTgb]': 'false'})
        data2=r.json()
        soup = BeautifulSoup(data2["data"]['results'], "lxml")
        for link in soup.findAll('a'):
          if (str(link.get('class')).count('_big')>0):
            if str(link.get('href'))!='None':
              s = str(link.get('href'))
              cou+=1
              episodelinks.append(s)
        if (data2["data"]["haveMorePages"]==False):
          break

        page+=1
      print('В ' + seasonname[season] + ' найдено серий: ' + str(cou))
print('Всего найдено эпизодов: '+str(len(episodelinks)))

def download(url: str, dest_folder: str,filename):
  if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)  # create folder if it does not exist
  file_path = os.path.join(dest_folder, filename)

  r = requests.get(url, stream=True)
  if r.ok:
    print("Скачан плейлист в ", os.path.abspath(file_path))
    with open(file_path, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024 * 8):
        if chunk:
          f.write(chunk)
          f.flush()
          os.fsync(f.fileno())
  else:  # HTTP status code 4XX/5XX
    print("Ошибка скачивания, код ошибки: {}\n{}".format(r.status_code, r.text))



links = []
names = []
for episode in episodelinks:
  if episode==None: continue;
  print('Скачиваем информацию о файле '+episode)
  names.append(episode.replace(site+'videos/','')+'.mp4')
  print(episode)
  req = Request(episode)
  html_page = urlopen(req)
  soup = BeautifulSoup(html_page, "lxml")
  for link in soup.findAll('iframe'):
    s=str(link.get('src'))
    s=s[s.rindex('/')+1:s.rindex('?')]
    s='https://uma.media/api/play/options/'+s+'/?format=json&no_404=true&referer=https%3A%2F%2Fweddings.friday.ru%2F'
    with urllib.request.urlopen(s) as url:
      data = json.loads(url.read().decode())
      url = data["video_balancer"]["default"]
      filename = url[url.rindex("/")+1:url.index("?")]
      download(url,"playlists",filename)
    f=open("playlists/"+filename)
    lines=f.readlines()
    resols=[]
    pl = []
    for line in lines:
      if (line.count('RESOLUTION')>0):
        resol=line[line.rindex('=')+1:-1]
        spl=resol.split('x')
        resols.append(int(spl[0])*int(spl[1]))

      if (line.count('https:') > 0):
        pl.append((line[:-1]))
    m=max(resols)
    for i in range(len(resol)):
      if m==resols[i]:
        links.append(pl[i])
        break
file = open("1.cmd", "w")


for i in range(len(links)):
  file.write('yt-dlp.exe -o "'+names[i]+'" '+links[i]+'\n')
file.close()
print('Создан файл 1.cmd')
