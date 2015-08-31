#!/usr/bin/python3
import csv
import json
import time

from bs4 import BeautifulSoup
import matplotlib.dates as dt
import matplotlib.pyplot as plt

import requests


HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"}


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


def scrape(maker_id, model_id):
    page = 1
    result = []
    while True:
        print('Scraping page {}'.format(page))

        r = requests.get(build_link(maker_id, model_id, page), headers=HEADERS)
        if r.status_code != 200:
            continue

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


def create_csv(data, maker_name, model_name):
    maker_name = maker_name.replace('/', '')
    model_name = model_name.replace('/', '')
    filename = "data/{}_{}.csv".format(maker_name, model_name)
    with open(filename, 'w', newline='') as data_file:
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


def gather_all_data():
    "Scrapes price data for all makers and their models"
    with open('makers.json', 'r') as makers_json:
        makers = json.load(makers_json)

    maker_name_start = 'Citroen'
    model_name_start = 'DS5'
    past_start = False

    for maker in makers:
        maker_id = maker['id']
        maker_name = maker['maker']
        for model in maker['models']:
            if maker_name_start == maker_name and model_name_start == model_name:
                past_start = True
            model_id = model['id']
            model_name = model['model']

            if past_start:
                print('Scraping data for: {} {}'.format(maker_name, model_name))
                data = scrape(maker_id, model_id)
                create_csv(data, maker_name, model_name)
                time.sleep(3)


if __name__ == '__main__':
    data = scrape(maker_id, model_id)
    #plot(data)
