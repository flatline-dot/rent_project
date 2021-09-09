from bs4 import BeautifulSoup
from utils import read_links_csv, write_data_csv, read_proxies, get_html
#from datetime import datetime, timedelta, date
# import locale
# import platform


# if platform.system() == 'Windows':
#     locale.setlocale(locale.LC_ALL, "russian")
# else:
#     locale.setlocale(locale.LC_TIME, 'ru_RU')


# def parse_cian_date(date_):
#     if 'сегодня' in date_:
#         today = datetime.now()
#         date_str = date_.replace('сегодня', today.strftime('%d %B %Y'))
#     elif 'вчера' in date_:
#         yesterday = datetime.now() - timedelta(days=1)
#         date_str = date_.replace('вчера', yesterday.strftime('%d %B %Y'))
#     try:
#         return datetime.strptime(date_, '%d %B %Y в %H:%M')
#     except ValueError:
#         return datetime.now()


def deposit_check(deposit):
    new_deposit = deposit.split(',')[0].split()
    return new_deposit[1] + new_deposit[2]


def commission_check(commission):
    new_commission = commission.split(',')[1].split()[1]
    if '%' in new_commission:
        return new_commission.replace('%', '')
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


def area_check(area):
    if ',' in area:
        return area.replace(',', '.')
    else:
        return area


def get_data(html, link):
    soup = BeautifulSoup(html, 'html.parser')
    rooms_ = soup.find('div', class_='a10a3f92e9--container--fX4cE').find('h1', class_='a10a3f92e9--title--2Widg').text
    rooms = rooms_.split()[0].split('-')[0] 
    area = area_check(soup.find('div', class_='a10a3f92e9--container--fX4cE').find('h1', class_='a10a3f92e9--title--2Widg').text.split()[2])
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
    # date_str = soup.find('div', class_='a10a3f92e9--offer_meta_main--3HPXd').find('div', class_='a10a3f92e9--container--3nJ0d').text
    # date_str = str(parse_cian_date(date_str))


    data_ = {
        'link': link,
        'num_rooms': rooms,
        'area': area,
        'district': district,
        'metro': metro,
        'floor': floor,
        'price': price,
        'material': material,
        'street': street,
        'commission': commission_check(commission),
        'deposit': deposit_check(commission),
        #'date': date_str
    }
    print(data_)
    if data_['material']:
        write_data_csv(data_, 'data_cian.csv')


def main():
    links = read_links_csv('example.csv')
    proxies = read_proxies()
    for link in links:
        try:
            html = get_html(link=link, proxies=proxies)
            get_data(html=html, link=link)
            get_data.raise_for_status()
            print('Страница', links.index(link) + 1)
        except Exception as err:
            print(err, link, 'Страница:', links.index(link) + 1)


if __name__ == '__main__':
    main()
