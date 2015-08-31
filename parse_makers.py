# coding: utf-8
import json

from bs4 import BeautifulSoup as BS
import requests


HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"}


def scrape_makers():
    "Scrapes makers' ids to be used to scrape their models"
    r = requests.get('http://auto.plius.lt/', headers=HEADERS)
    r.encoding = 'utf-8'
    html = r.text
    soup = BS(html, 'html.parser')
    maker_options = soup.select('#make_id option')

    for option in maker_options:
        maker_id = option['value']
        maker_name = option.contents[0]
        yield maker_id, maker_name


def scrape_models():
    """Scrapes makers and their models into JSON with form like this
    ::

        [
        {
            "model": "volkswagen",
            "id": 43,
            "models": [
                {
                    "model": "golf",
                    "id": 193
                },
                {
                    "model": "passat",
                    "id": 666
                }
            ]
        },
        {
            "model": "Audi",
            "id": 77,
            "models": [
                {
                    "model": "A6",
                    "id": 46
                },
                {
                    "model": "100",
                    "id": 100
                }
            ]
        }
        ]

    Scraping is done, by sending POST request, with correct data, which
    includes car model's id.

    This could be read in `http://auto.plius.lt/` `plus_main.js` file.
    There is a function `ajaxGetChildsTo`, which calls `apAJAX.send`
    """
    makers = []

    data = {
        'parent_id': '43',
        'target_id': 'model_id',
        'project': 'autoplius',
        'category_id': '2',
        'type': 'search',
        'my_anns': False,
        '__block': 'ann_ajax_0_plius',
        '__opcode': 'ajaxGetChildsTo'
    }

    for id, name in scrape_makers():
        print("Scraping {} models".format(name))
        data['parent_id'] = id
        r = requests.post('http://auto.plius.lt', headers=HEADERS, data=data)
        r.encoding = 'utf-8'
        html = r.text.replace('\\', '')
        soup = BS(html, 'html.parser')
        model_options = soup.select('option')
        models = []
        for option in model_options:
            model_id = option['value']
            model_name = option.contents[0]
            if not model_id:
                continue
            models.append({'model': model_name, 'id': model_id})
        makers.append({'maker': name, 'id': id, 'models': models})
    with open('makers.json', 'w') as makers_json:
        json.dump(makers, makers_json, indent=4)


if __name__ == '__main__':
    scrape_models()
