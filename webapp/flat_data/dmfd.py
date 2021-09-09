import re
import traceback

from bs4 import BeautifulSoup
from utils import read_links_csv, write_links_csv, read_proxies, all_links, get_html, write_data_csv


def get_link(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.find('div', class_='search-results__itemCardList___RdWje')
    href = href.contents
    for i in href:
        if i.get('href'):
            link = 'https://www.domofond.ru' + i.get('href')
            links.append(link)
    write_links_csv(links, 'domofond_links.csv')


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
    full_material = ''
    for i in ['Кирпичный', 'Монолитный', 'Панельный']:
        if material in i:
            full_material = i
            return full_material
    return material


def get_data(links, proxy):
    for link in links:
        try:
            html = get_html(link, proxy)
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
            street = soup.find('a', class_='information__address___1ZM6d').text.split(',')
            street = street[1].strip() + ', ' + street[2].strip()
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
                write_data_csv(data, 'domofond.csv')
                print('Страница', links.index(link) + 1, 'Успешно!')
        except Exception as err:
            print(err, f'on {link}', f'Страница {links.index(link) + 1}', 'STR', traceback.format_exc())


def main():
    proxy = read_proxies()
    all_links(proxy, 70, f'https://www.domofond.ru/arenda-kvartiry-moskva-c3584?RentalRate=Month&PublicationTimeRange=OneWeek&Page=', get_link)
    links = read_links_csv('domofond_links.csv')
    get_data(links, proxy)


if __name__ == '__main__':
    main()
