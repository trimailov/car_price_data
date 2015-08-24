#!/usr/bin/python3
import csv

from bs4 import BeautifulSoup
import matplotlib.dates as dt
import matplotlib.pyplot as plt

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

def is_euro(price):
    "Removes euro symbol from price"
    price = price[0].contents[0]
    if price.endswith('€'):
        # remove two last chars and spaces
        return int(price[:-2].replace(' ', ''))
    # at this moment we do not want to save non-euro prices
    return None


def parse_data(soup):
    "Parses price and date data from html page"
    auto_list = soup.select('ul.auto-list li')
    prices = []
    dates = []
    for auto in auto_list:
        if not auto.select('div.item div.price-list-promo'):
            price = auto.select('div.price-list p.fl strong')
            date = auto.select('div.param-list span[title^=Pagaminimo]')
        if all((price, date)) and is_euro(price):
            prices.append(is_euro(price))
            dates.append(date[0].contents[0])
    return dates, prices


def scrape():
    page = 1
    result = []
    while True:
        print('Parsing page {}'.format(page))

        r = requests.get(build_link(43, 193, page))
        r.encoding = 'utf-8'
        html = r.text

        soup = BeautifulSoup(html, 'html.parser')

        dates, prices = parse_data(soup)

        # if no data is retrieved - stop scraping
        if not any((dates, prices)):
            break

        z = zip(dates, prices)
        result.extend(list(z))
        page += 1

    return result


def create_csv(data):
    with open('data.csv', 'w', newline='') as data_file:
        writer = csv.writer(data_file)
        writer.writerow(['Date', 'Price, EUR'])
        for row in data:
            writer.writerow(row)


def plot(data):
    dates, prices = zip(*data)
    num_dates = []
    # convert dates into numbers which can be plotted
    for date in dates:
        num_dates.append(dt.datestr2num(date))
    plt.plot_date(num_dates, prices)
    plt.show()


if __name__ == '__main__':
    data = scrape()
    create_csv(data)
    plot(data)
