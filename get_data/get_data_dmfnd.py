import re
import csv
import time
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def read_csv():
    with open('links_list_domofond.csv', 'r') as f:
        links = f.read().split()
        return links


def csv_writer(data):
    with open('domofond_data.csv', 'a', newline='', encoding='utf=8') as f:
        fieldnames = [
            'num_rooms', 'floor', 'material', 'metro', 'district',
            'street', 'area', 'price', 'commission', 'deposit', 'link'
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writerow(data)


def get_html(url):
    ua = UserAgent()
    headers = {'UserAgent': ua.random}
    html = requests.get(url, headers=headers)
    return html.text


def commission_check(commission):
    if commission == 'нет':
        return 0
    else:
        return commission.replace('%', '')


def deposit_check(deposit):
    if deposit == 'нет':
        return 0
    else:
        deposit = deposit.replace('₽', '')
        deposit = deposit.replace(' ', '')
        return deposit


def metro_check(metro):
    patern = r'(.+)\s\d'
    real_metro = re.findall(patern, metro)[0]
    print(real_metro)
    i = 0
    for alpha in real_metro.split()[0]:
        if alpha.isupper():
            i += 1
    if len(real_metro.split()[0]) == i:
        return real_metro[1:]
    return real_metro[i - 1:]


def material_check(material):
    if material in ['Кирпич', 'Монолит', 'Панель']:
        return material
    else:
        return False


def get_data(html, link):
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.find('div', class_='detail-information__wrapper___FRRqm')
    commission = commission_check(href.contents[1].find_next().find_next().text)
    deposit = deposit_check(href.contents[2].find_next().find_next().text)
    num_rooms = href.contents[3].find_next().find_next().text
    floor = href.contents[4].find_next().find_next().text.split('/')[0]
    area = href.contents[5].find_next().find_next().text.split()[0]
    price = href.contents[8].find_next().find_next().text.replace(' ', '').replace('₽', '')
    material = material_check(href.contents[10].find_next().find_next().text)
    metro = metro_check(soup.find('div', class_='information__metro___2zFqN').text)
    district = soup.find('a', class_='information__address___1ZM6d').text.split(',')[-2].strip()
    street = soup.find('a', class_='information__address___1ZM6d').text.split(',')[1].strip()
    data = {'commission': commission,
            'deposit': deposit,
            'num_rooms': num_rooms,
            'floor': floor,
            'area': area,
            'price': price,
            'material': material,
            'metro': metro,
            'district': district,
            'street': street,
            'link': link
            }
    if data['material']:
        csv_writer(data)


def main():
    links = read_csv()
    for link in links:
        time.sleep(1)
        try:
            html = get_html(link)
            get_data(html, link)
            print('Страница', links.index(link) + 1)
        except (TypeError, ValueError, AttributeError, IndexError) as err:
            print(err, links.index(link) + 1)


if __name__ == '__main__':
    main()
