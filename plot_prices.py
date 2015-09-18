#!/usr/bin/python3
import csv
import datetime

import matplotlib.dates as dt
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit


plt.style.use('dark_background')


def read_csv(maker_name, model_name):
    maker_name = maker_name.replace('/', '')
    model_name = model_name.replace('/', '')
    filename = "results/data/{}_{}.csv".format(maker_name, model_name)
    with open(filename, 'r', newline='') as data_file:
        data = [tuple(row) for row in csv.reader(data_file)]
    # do not return csv header
    return data[1:]


def ready_data(data):
    dates, prices = zip(*data)
    number_prices = list(map(int, prices))
    number_dates = []
    # convert dates into numbers which can be plotted
    for date in dates:
        # num_dates.append(dt.datestr2num(date))
        if len(date) > 4:
            number_dates.append(datetime.datetime.strptime(date, '%Y-%m').date())
        else:
            number_dates.append(datetime.datetime.strptime(date, '%Y').date())

    return number_dates, number_prices


def get_min_max_dates(dates):
    "Founds the outer limits of min and max years"
    date_min = min(dates)
    date_max = max(dates)

    year_min = date_min.year
    year_max = date_max.year + 1

    return year_min, year_max


def exp_func(x, a, b, c):
    return a * np.exp(b * x) + c


def poly_func(x, a, b, c):
    return a * x ** 2 + b * x + c


def fit_prices(dates, prices, fit_func):
    number_dates = dt.date2num(dates)

    # normalize dates to have smaller numbers in range from 0 to 1
    min_date = min(number_dates)
    temp_number_dates = number_dates - min_date
    max_date = max(temp_number_dates)
    norm_number_dates = temp_number_dates / max_date
    del temp_number_dates

    popt, pcov = curve_fit(fit_func, norm_number_dates, prices)

    # calculate prices, from normalized dates upon exp_func()
    fitted_dates = np.linspace(min(norm_number_dates),
                               max(norm_number_dates),
                               1000)
    fitted_prices = [fit_func(date, popt[0], popt[1], popt[2])
                     for date in fitted_dates]

    # denormlaize dates
    denorm_number_dates = (fitted_dates + min_temp_date) * max_date

    return denorm_number_dates, fitted_prices


def plot(data, maker, model):
    # every which year major tick should be placed
    YEAR_TICK = 3

    dates, prices = ready_data(data)

    fitted_dates, fitted_prices = fit_prices(dates, prices, exp_func)
    # fitted_dates_poly, fitted_prices_poly = fit_prices(dates, prices, poly_func)

    year_min, year_max = get_min_max_dates(dates)

    # min and max years should be exactly on major tick for better looks
    year_min = YEAR_TICK * (year_min // YEAR_TICK)
    year_max = YEAR_TICK * (year_max // YEAR_TICK)

    plt.gca().xaxis.set_major_formatter(dt.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(dt.YearLocator(YEAR_TICK))

    plt.plot_date(dates, prices)
    plt.plot_date(fitted_dates, fitted_prices, fmt='-', linewidth=2)
    # plt.plot_date(fitted_dates_poly, fitted_prices_poly, fmt='-', linewidth=2)
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
