from utils import get_html, read_proxies, write_links_csv, read_links_csv, write_data_csv
import config
from bs4 import BeautifulSoup
import traceback


def get_link(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('div', class_='items-items-38oUm').find_all('div', class_='iva-item-root-G3n7v photo-slider-slider-3tEix iva-item-list-2_PpT iva-item-redesign-1OBTh iva-item-responsive-1z8BG items-item-1Hoqq items-listItem-11orH js-catalog-item-enum')
    for element in data:
        link = 'https://www.avito.ru/' + element.find('a', class_='iva-item-sliderLink-2hFV_').get('href')
        links.append(link)
    write_links_csv(links, 'avito_links.csv')


def all_links(proxy):                        # get ads links and write on csv
    for page in range(50):
        try:
            html = get_html(config.avito_url, proxy)
            get_link(html)
            print('Страница', page)
        except Exception as err:
            print(err, '({page})')


def get_data(links, proxy):
    for link in links:
        try:
            html = get_html(link, proxy)
            soup = BeautifulSoup(html, 'html.parser')

            head_data = soup.find('span', class_='title-info-title-text').text.split(',')
            if head_data[0][0].isdigit():
                num_rooms = int(head_data[0][0])
            else:
                num_rooms = int(0)

            area = int(head_data[1].split()[0])

            floor = int(head_data[2][1])

            price = int(soup.find('span', class_='js-item-price').get('content'))
            pay_data = soup.find('div', class_='item-price-sub-price').text.split(',')
            deposit_count = ''
            for i in pay_data[0]:
                if i.isdigit():
                    deposit_count += i

            if deposit_count:
                deposit = int(deposit_count)
            else:
                deposit = int(0)

            if len(pay_data) > 1 and ('без комиссии' not in pay_data[1]):
                commission_count = ''
                for i in pay_data[1]:
                    if i.isdigit():
                        commission_count += i
                commission = int(int(commission_count) * 100 / price)
            else:
                commission = int(0)

            metro = soup.find('span', class_='item-address-georeferences-item__content').text

            street_data = soup.find('span', class_='item-address__string').text.split()

            street = ' '.join(street_data[1:])

            district = ''
            try:
                material = soup.find(text='Тип дома: ').parent.parent.text.split()[2].title()
            except Exception:
                material = ''

            link = link

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
            write_data_csv(data, 'avito.csv')
            print('Страница', links.index(link) + 1, 'Успешно!')
        except Exception as err:
            print(err, f'on {link}', f'Страница {links.index(link) + 1}', 'STR', traceback.format_exc())

    print(data)


def main():
    proxy = read_proxies()
    all_links(proxy)
    links = read_links_csv('avito_links.csv')
    get_data(links, proxy)


if __name__ == '__main__':
    main()
