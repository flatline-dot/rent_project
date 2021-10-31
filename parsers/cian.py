import traceback

from bs4 import BeautifulSoup
from utils import read_links_csv, write_links_csv, read_proxies, all_links, get_html, write_data_csv


def deposit_check(deposit):
    new_deposit = deposit.split(',')[0].split()
    return new_deposit[1] + new_deposit[2]


def commission_check(commission):
    new_commission = commission.split(',')[1].split()[1]
    if '%' in new_commission:
        return new_commission.replace('%', '')
    else:
        return 0


def area_check(area):
    if ',' in area:
        return area.replace(',', '.')
    else:
        return area


def get_link(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    href = soup.find('div', class_='_93444fe79c--wrapper--E9jWb')
    href = href.contents
    for i in href:
        link = i.find('div', class_='_93444fe79c--container--2Kouc _93444fe79c--link--2-ANY').find('a').get('href')
        print(link)
        links.append(link)
    write_links_csv(links, 'C:\\Project\\rent_project\\aggregation\\data\\cian_links.csv')


def get_data(html, link):
    def get_data(links, proxy):
        for link in links:
            try:
                soup = BeautifulSoup(html, 'html.parser')
                rooms = soup.find('div', class_='a10a3f92e9--container--fX4cE').find('h1', class_='a10a3f92e9--title--2Widg').text[0]
                area = area_check(soup.find('div', class_='a10a3f92e9--container--fX4cE').find('h1', class_='a10a3f92e9--title--2Widg').text.split()[2])
                district = soup.find('div', class_='a10a3f92e9--geo--18qoo').find('address', class_='a10a3f92e9--address--140Ec').find_all('a', class_='a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr')[2].text
                district = district.split('р-н')[1].replace(' ', '')
                metro = soup.find('a', class_='a10a3f92e9--underground_link--AzxRC').text
                floor = soup.find('div', class_="a10a3f92e9--info-block--3cWJy").contents[3].find('div', class_="a10a3f92e9--info-value--18c8R").text
                floor = floor.split(' ')[0]
                price = soup.find('span', class_='a10a3f92e9--price_value--1iPpd').contents[0].get('content').split(' ')
                price = price[0] + price[1]
                material = soup.find('div', class_='a10a3f92e9--column--2oGBs').contents[1].find('div', class_='a10a3f92e9--value--38caj').text
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
                    write_data_csv(data, 'C:\\Project\\rent_project\\aggregation\\data\\cian.csv')
                    print('Страница', links.index(link) + 1, 'Успешно!')
            except Exception as err:
                print(err, f'on {link}', f'Страница {links.index(link) + 1}', 'STR', traceback.format_exc())


def main():
    proxy = read_proxies()
    all_links(proxy, 3, f'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=', get_link)
    links = read_links_csv('C:\\Project\\rent_project\\aggregation\\data\\cian_links.csv')
    get_data(links, proxy)


if __name__ == '__main__':
    main()
