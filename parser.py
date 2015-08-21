#!/usr/bin/python3

from bs4 import BeautifulSoup

import requests


def build_link(manufacturer_id, model_id, page):
    base_link = 'http://auto.plius.lt/skelbimai/naudoti-automobiliai'
    manufacturer = 'make_id={}'.format(manufacturer_id)
    model = 'model_id={}'.format(model_id)
    page = 'page_nr={}'

    link = '{base_link}?{manufacturer}&{model}&{page}'.format(
        base_link=base_link,
        manufacturer=manufacturer,
        model=model.format,
        page=page,
    )

    return link


def scrape():
    r = requests.get(build_link(43, 193, 1))
    r.encoding = 'utf-8'
    html = r.text

    soup = BeautifulSoup(html, 'html.parser')
    prices = [price.contents[0] for price in soup.select('p.fl strong')]
    dates = [date.contents[0] for date in soup.select('span[title^=Pagaminimo]')]

    z = zip(dates, prices)

    for i in z:
        print(i)


if __name__ == '__main__':
    scrape()
