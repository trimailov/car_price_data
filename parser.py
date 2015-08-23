#!/usr/bin/python3

from bs4 import BeautifulSoup

import requests


def build_link(manufacturer_id, model_id, page_nr):
    base_link = 'http://auto.plius.lt/skelbimai/naudoti-automobiliai'
    manufacturer = 'make_id={}'.format(manufacturer_id)
    model = 'model_id={}'.format(model_id)
    page = 'page_nr={}'.format(page_nr)

    link = '{base_link}?{manufacturer}&{model}&{page}'.format(
        base_link=base_link,
        manufacturer=manufacturer,
        model=model,
        page=page,
    )

    return link


def parse_data(soup):
    "Parses price and date data from html page"
    auto_list = soup.select('ul.auto-list li')
    prices = []
    dates = []
    for auto in auto_list:
        if not auto.select('div.item div.price-list-promo'):
            price = auto.select('div.price-list p.fl strong')
            date = auto.select('div.param-list span[title^=Pagaminimo]')
        if all((price, date)):
            prices.append(price[0].contents[0])
            dates.append(date[0].contents[0])
    return prices, dates


def scrape():
    page = 1
    while True:
        r = requests.get(build_link(43, 193, page))
        r.encoding = 'utf-8'
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        dates, prices = parse_data(soup)

        # if no data is retrieved - stop scraping
        if not any((dates, prices)):
            break

        z = zip(dates, prices)

        for i in z:
            print(i)

        page += 1


if __name__ == '__main__':
    scrape()