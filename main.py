import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime
from filestack import Client, Filelink, Security
import pytz

URL = "https://app.ue.poznan.pl/Schedule/Home/GetTimeTable?dep=101&cyc=2&year=1&group=10121001&type=2&_=1665996847096"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
cal = Calendar()

client = Client('AukpHJ5NSrKVyaO8hmo1Az')

for e in soup.find_all(class_='div_hover'):
    if e.find('b').string is not None:
        numerZjazdu = e.find('b').string[1:2].replace('\n', '')
        data = e.find('b').string[4:14]
        for p in e.find_all('p'):
            godzinaRozpoczecia = int(p.string.split('\n')[1][0:2])
            minutaRozpoczecia = int(p.string.split('\n')[1][3:5])
            godzinaZakonczenia = int(p.string.split('\n')[1][6:8])
            minutaZakonczenia = int(p.string.split('\n')[1][9:11])
            nazwaPrzedmiotu = p.string.split('\n')[2].replace('\r', '')
            sala = ' '.join((p.string.split('\n')[3].split(' '))[0:2])
            lokalizacja = ''.join((p.string.split('\n')[3].split(' '))[2:4])
            prowadzacy = p.string.split('\n')[4].replace('\r', '')

            event = Event()
            rok = int(data[0:4])
            miesiac = int(data[5:7])
            dzien = int(data[8:10])

            event.name = f'{nazwaPrzedmiotu}, {sala}, {lokalizacja}'

            # Dodanie strefy czasowej Europe/Warsaw
            tz = pytz.timezone('Europe/Warsaw')
            event.begin = tz.localize(datetime(rok, miesiac, dzien, godzinaRozpoczecia, minutaRozpoczecia))
            event.end = tz.localize(datetime(rok, miesiac, dzien, godzinaZakonczenia, minutaZakonczenia))

            event.description = f"Zjazd: {numerZjazdu} Prowadzący: {prowadzacy}"
            cal.events.add(event)

open('universitySchedule.ics', 'w', newline='', encoding='utf-8').writelines(cal)

sec = Security({'expiry': 1761826998, "call": ["write"]}, secret='J7XONYZOC5AL3MPEFHNC7THK6A')
createdFile = Filelink('24HbcuyuQ7SRSAbCQQxB')

createdFile.overwrite(filepath='universitySchedule.ics',security=sec)
