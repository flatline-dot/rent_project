from random import choice
import csv
import time
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def read_proxies():
    with open('list_proxies.txt', 'r', newline='', encoding='utf=8') as f:
        proxy = []
        for line in f.readlines():
            proxy.append(line.strip())
        return proxy


def read_list_links():
    with open('list_links_cian.csv', newline='', encoding='utf-8') as f:
        reads = f.read().split()
        return reads


def write_csv(result):
    with open('data_cian.csv', 'a', newline='', encoding='utf=8') as f:
        fieldnames = [
            'num_rooms', 'floor', 'material', 'metro', 'district',
            'street', 'area', 'price', 'comission', 'deposit', 'link'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writerow(result)


def deposit_check(deposit):
    new_deposit = deposit.split(',')[0].split()
    return new_deposit[1] + new_deposit[2]


def commission_check(commission):
    new_commission = commission.split(',')[1]
    if new_commission.isdigit():
        new_commission.replace('%', '')
        return new_commission
    else:
        return 0


def material_check(material):
    if material == 'Монолитный':
        return 'Монолит'
    elif material == 'Кирпичный':
        return 'Кирпич'
    elif material == 'Панельный':
        return 'Панель'
    else:
        return False


def get_html(link, proxies):
    time.sleep(1)
    ua = UserAgent()
    headers = {'UserAgent': ua.random}
    proxy = {'http': 'http://' + choice(proxies)}
    html = requests.get(link, headers=headers, proxies=proxy)
    result = html.text
    return result


def get_data(html, link):
    soup = BeautifulSoup(html, 'html.parser')
    rooms = soup.find('div', class_='a10a3f92e9--container--fX4cE').find('h1', class_='a10a3f92e9--title--2Widg').text[0]
    area = soup.find('div', class_='a10a3f92e9--container--fX4cE').find('h1', class_='a10a3f92e9--title--2Widg').text.split()[2]
    district = soup.find('div', class_='a10a3f92e9--geo--18qoo').find('address', class_='a10a3f92e9--address--140Ec').find_all('a', class_='a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr')[2].text
    district = district.split('р-н')[1].replace(' ', '')
    metro = soup.find('a', class_='a10a3f92e9--underground_link--AzxRC').text
    floor = soup.find('div', class_="a10a3f92e9--info-block--3cWJy").contents[3].find('div', class_="a10a3f92e9--info-value--18c8R").text
    floor = floor.split(' ')[0]
    price = soup.find('span', class_='a10a3f92e9--price_value--1iPpd').contents[0].get('content').split(' ')
    price = price[0] + price[1]
    material = material_check(soup.find('div', class_='a10a3f92e9--column--2oGBs').contents[1].find('div', class_='a10a3f92e9--value--38caj').text)
    street = soup.find('address', class_='a10a3f92e9--address--140Ec').text.split(',')[3]

    commission = soup.find('div', class_='a10a3f92e9--info-container--3JwEv').find('p', class_='a10a3f92e9--description--2xRVn').text
    commission = commission.split('\xa0')
    commission = ' '.join(commission)
    data = {
        'link': link,
        'num_rooms': rooms,
        'area': area,
        'district': district,
        'metro': metro,
        'floor': floor,
        'price': price,
        'material': material,
        'street': street,
        'comission': commission_check(commission),
        'deposit': deposit_check(commission)
    }
    if data['material']:
        write_csv(data)


def main():
    links = read_list_links()
    proxies = read_proxies()
    for link in links:
        try:
            html = get_html(link=link, proxies=proxies)
            get_data(html=html, link=link)
            print('Страница', links.index(link) + 1)
        except Exception as err:
            print(err, link, 'Страница:', links.index(link) + 1)


if __name__ == '__main__':
    main()
