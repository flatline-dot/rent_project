import csv
import time
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import domofond_url


def get_html(url):
    ua = UserAgent()
    headers = {'UserAgent': ua.random}
    html = requests.get(url, headers=headers)
    return html.text


def write_csv(link):
    with open('links_list.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([link])


def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.find('div', class_='search-results__itemCardList___RdWje')
    href = href.contents
    for i in href:
        if i.get('href'):
            link = 'https://www.domofond.ru' + i.get('href')
            write_csv(link)


def main():
    for page in range(1, 150):
        url = domofond_url
        time.sleep(1)
        try:
            html = get_html(url)
            get_links(html)
            print('Страница', page)
        except (ValueError, TypeError) as err:
            print(err, page)


if __name__ == '__main__':
    main()
