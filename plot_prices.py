#!/usr/bin/python3
import csv
import datetime

import matplotlib.dates as dt
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit


def read_csv(maker_name, model_name):
    maker_name = maker_name.replace('/', '')
    model_name = model_name.replace('/', '')
    filename = "results/data/{}_{}.csv".format(maker_name, model_name)
    with open(filename, 'r', newline='') as data_file:
        data = [tuple(row) for row in csv.reader(data_file)]
    # do not return csv header
    return data[1:]


def exp_func(x, a, b, c):
    return a * np.exp(b * x) + c


def fit_plot(dates, prices):
    number_dates = dt.date2num(dates)
    number_prices = list(map(int, prices))
    popt, pcov = curve_fit(exp_func, number_dates, number_prices)
    pass


def plot(data, maker, model):
    # every which year major tick should be placed
    YEAR_TICK = 3

    dates, prices = zip(*data)
    num_dates = []
    # convert dates into numbers which can be plotted
    for date in dates:
        # num_dates.append(dt.datestr2num(date))
        if len(date) > 4:
            num_dates.append(datetime.datetime.strptime(date, '%Y-%m').date())
        else:
            num_dates.append(datetime.datetime.strptime(date, '%Y').date())

    fit_plot(num_dates, prices)

    date_min = min(dates)
    date_max = max(dates)

    if len(date_min) > 4:
        year_min = datetime.datetime.strptime(date_min, '%Y-%m').year
    else:
        year_min = datetime.datetime.strptime(date_min, '%Y').year

    if len(date_max) > 4:
        year_max = datetime.datetime.strptime(date_max, '%Y-%m').year + 1
    else:
        year_max = datetime.datetime.strptime(date_max, '%Y').year + 1

    # min and max years should be exactly on major tick for better looks
    year_min = YEAR_TICK * (year_min // YEAR_TICK)
    year_max = YEAR_TICK * (year_max // YEAR_TICK)

    plt.gca().xaxis.set_major_formatter(dt.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(dt.YearLocator(YEAR_TICK))

    plt.plot_date(num_dates, prices)
    plt.grid(True)

    plt.gca().set_xlim(
        datetime.date(year_min, 1, 1),
        datetime.date(year_max, 1, 1)
    )

    plt.title('{} {}'.format(maker, model))
    plt.xlabel('Year of manufacture')
    plt.ylabel('Price, EUR')

    plt.xticks(rotation=30)

    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    # data = scrape(maker_id, model_id)
    # plot(data)
    maker = 'Volkswagen'
    model = 'Passat'
    data = read_csv(maker, model)
    plot(data, maker, model)
