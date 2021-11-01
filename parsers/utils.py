import csv
import time
import traceback
from fake_useragent import UserAgent
import requests

from random import choice, random, randint


def write_links_csv(links, file_name):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        for item in links:
            writer.writerow([item])


def read_links_csv(file):
    with open(file, 'r') as f:
        links = f.read().split()
        return links


def write_data_csv(data, file):
    with open(file, 'a', newline='', encoding='utf=8') as f:
        fieldnames = [
            'num_rooms', 'floor', 'material', 'metro', 'district',
            'street', 'area', 'price', 'commission', 'deposit', 'link'
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writerow(data)


def get_html(link, proxies):
    try:
        time.sleep(randint(1, 10))
        ua = UserAgent()
        headers = {'UserAgent': ua.random}
        proxy = {'http': 'http://' + choice(proxies)}
        html = requests.get(link, headers=headers, proxies=proxy)
        result = html.text
        return result
    except Exception as err:
        print(err, traceback.format_exc())


def read_proxies():
    with open('list_proxies.txt', 'r', newline='', encoding='utf=8') as f:
        proxy = []
        for line in f.readlines():
            proxy.append(line.strip())
        return proxy


def all_links(proxy, num_pages, url, get_link):                        # get ads links and write on csv
    for page in range(1, num_pages):
        link = url + str(page)
        try:
            html = get_html(link, proxy)
            get_link(html)
            print(link)
        except Exception as err:
            print(err, url)
