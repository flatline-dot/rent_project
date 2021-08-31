from bs4 import BeautifulSoup
import re
import requests
from requests import exceptions
import csv


url = 'https://snipp.ru/handbk/mos-metro'


def get_html(url):
    try:
        html = requests.get(url)
        html.raise_for_status()
       # re.sub(r'>\s+<', '><', html.replace('\n', ''))
        return html.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка', exceptions)
        return False


def html_data_csv(data):
    with open('file.txt', 'a', encoding='utf-8') as f:
        f.write(data)
        return f 


def metro_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    list_metro = soup.find('div', class_ = 'snp_tabs-items').find('pre')
    result = ''
    for station in list_metro:
        result+=station.text
    return result

    
def main():
    all_station = metro_data(get_html(url))
    html_data_csv(all_station)


if __name__=='__main__':
    main()

