#!/usr/bin/python3

from bs4 import BeautifulSoup

import requests

link = 'http://auto.plius.lt/skelbimai/naudoti-automobiliai?make_id=43&model_id=193'
r = requests.get(link)
r.encoding = 'utf-8'
html = r.text

soup = BeautifulSoup(html, 'html.parser')
prices = [price.contents[0] for price in soup.select('p.fl strong')]
dates = [date.contents[0] for date in soup.select('span[title^=Pagaminimo]')]

z = zip(dates, prices)

for i in z:
    print(i)
