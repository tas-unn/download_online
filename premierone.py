import json
import os
import requests
showname='zhenskij-stendap'
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
for numseason in range(1,20):
  for numser in range(1, 100):
    site='https://premier.one/uma-api/metainfo/tv/'+showname+'/video/?type=6&limit=1&origin__type=hwi%2Crtb&page=1&sort=series_a&season='+str(numseason)+'&episode='+str(numser)
    res = requests.get(site)
    data = json.loads(res.text)

    try:
      videourl=str(data['results'][0]['video_url'][:-1])
    except:
      break
    videourl=videourl[videourl.rfind('/')+1:]

    s = requests.session()
    '''
    Если Вы хотите скачивать по подписке
    1) Устанавливаем расширение Chrome https://chromewebstore.google.com/detail/copy-as-python-requests/dpmidpbjjakkboiogkpjcfmafjljenhe?hl=ru&pli=1
    2) Авторизуемся на сайте, заходим в любое видео
    3) Открываем расширение. Там должно быть много строчек
    4) Нажимаем кнопку Copy
    5) Копируем в блокнот. Ищем в поиске следующую строку
    https://premier.one/api/play/options/
    6) Копируем строку всю строку, начиная с первой запятой и до конца. 
    7) Вставляем на 52ю строку скрипта. Пример в этой строке есть
    
    Если не хотите скачивать по подписке, тогда ничего не трогайте
    P.S. можете всегда регистироваться по промокодам, получая бесплатный смс по "левому" номеру, например https://getfreesmsnumber.com/
    '''
    res=s.get("https://premier.one/api/play/options/"+videourl+"/"
    , params={"format": "json", "no_404": "true", "referer": "https%3A%2F%2Fpremier.one%2Fshow%2Fzhenskij-stendap%2Fseason%2F5%2Fepisode%2F1%3Ffullscreen%3Dtrue"}, headers={"authorization": "JWTBearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNzI3NjM0LCJqdGkiOiI1OGNhYzQ2Yjg2NWQ0ZmI3Yjc0ZTAwMGFjYWMyOTQ0NiIsInVzZXJfaWQiOjIzNjY4MjI5LCJwbV9pZCI6IkVMT25VZ2JJVHYySFJwNWV5R1l4bkEifQ.uRb8lAzCxqmVxP_rpi5omrqmvGDpiBV4JKyqEBZlpbg", "expires": "0"}, cookies={"rst-uid": "0", "_ym_uid": "1675408651790058718", "_ym_d": "1679478930", "cleanerUTM": "true", "session_id": "95244599791700321055_1700121055031", "uwyii": "349b499d-1875-b629-ba5a-b37222d728c8", "oxxfgh": "bb841c2c-be6a-4290-9201-eca468fa915d%233%231800000%235000%231800000%2322821", "uact": "1700122835", "dtCookie": "v_4_srv_66_sn_546327D3850D6ABDF3114074499FEF45_perc_100000_ol_0_mul_1_app-3A72711a4540df540a_0", "rxVisitor": "1701122096611R0CQRPP565CPA3K1F0244R4SJSMIU8GE", "auth": "%7B%22deviceId%22%3A%227d26abf4-4a4b-48dd-bdbd-818c2f8b38cc%22%2C%22premierAccessToken%22%3A%2259ee9b272a1f161fc7b5ff991352c03cb7da8c718d3dbaa1a7e9935936959497%22%2C%22premierRefreshToken%22%3A%22cd535a96acb19e96226a67262f103e99e6af0ec4153ed17f9256b193536dc20c%22%2C%22premierAccessTokenExpiredAt%22%3A%222023-11-23T08%3A20%3A34Z%22%2C%22userAgent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F119.0.0.0%20Safari%2F537.36%22%2C%22theme%22%3A%22%22%2C%22profileId%22%3A%228773237e-9c0e-4d11-aed7-1c37262b2234%22%7D", "uwyiert": "58afbe35-5687-9d6f-1f9b-1cfb4d2474f9", "dtPC": "66$322985184_634h1p66$322987169_12h1p61$323140037_320h1p66$323142430_409h1vDRQFKFPUFQARAJFAKOWIJEORNGUHAAGS-0e0", "uuid": "e35585c4-2b17-45ee-9d4d-b3f246be49e5"})
    data = json.loads(res.text)
    print(data)
    url = data["video_balancer"]["default"]
    filename = url[url.rindex("/") + 1:url.index("?")]
    download(url, "playlists", filename)
    f = open("playlists/" + filename)
    lines = f.readlines()
    resols = []
    pl = []
    for line in lines:
      if (line.count('RESOLUTION') > 0):
        resol = line[line.rindex('=') + 1:-1]
        spl = resol.split('x')
        resols.append(int(spl[0]) * int(spl[1]))

      if (line.count('https:') > 0):
        pl.append((line[:-1]))
    m = max(resols)
    for i in range(len(resol)):
      if m == resols[i]:
        links.append(pl[i])
        nm=str(numseason)
        if numseason<=9:
          nm='0'+nm
        ns = str(numser)
        if numser <= 9:
          ns = '0' + ns
        names.append(showname+'.s'+nm+'.WEB-DL.(1080p)/'+showname+'.s'+nm+'.e'+ns+'.WEB-DL.1080.25.mp4')
        break
file = open(showname+".cmd", "w")
for i in range(len(links)):
  file.write('yt-dlp.exe -o "'+names[i]+'" '+links[i]+'\n')
file.close()
print('Создан файл '+showname+".cmd")
