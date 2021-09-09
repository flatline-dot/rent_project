import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import time


def get_html(url):  # Вызывает страницу html
    r = requests.get(url)
    r.raise_for_status()
    ua = UserAgent()
    headers = {'user-agent': ua.random}
    r = requests.get(url, headers=headers)
    return r.text


def disassemble(html): # разбор страницы
    list_ = []
    for number in range(0, 28):
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(3)
        try:
            soups = soup.find('div', class_="_93444fe79c--wrapper--E9jWb").contents[number]
            href = soups.find('div', class_="_93444fe79c--general--2SDGY").find('a').get('href')
            print(href)
            list_.append(href)
        except AttributeError:
            print('Ошибка объявления')    
        
        if number == 5:
            time.sleep(43)
    return list_

def lists_csv(main):
    with open('example.csv', 'a', newline='', encoding='utf-8') as File:
        writer = csv.writer(File)
        for row in main:
            writer.writerow([row])
def main():
    for page in range(1, 55):
        pages = f'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={page}&region=1&room1=1&type=4'
        html = get_html(pages)
        r = disassemble(html)
        lists_csv(r)

        time.sleep(3)

if __name__ == '__main__':
    main()