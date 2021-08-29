import csv

from webapp.model import db, Flat
from webapp import create_app


def read_csv(fieldname):
    with open(fieldname, 'r', encoding='utf-8') as f:
        fields = ['num_rooms', 'floor',
                  'material', 'metro',
                  'district', 'street',
                  'area', 'price',
                  'commission', 'deposit',
                  'link'
                  ]
        reader = csv.DictReader(f, fields, delimiter=';')
        data = [] 
        for row in reader:
            data.append(row)
        print(data)
        return data[1:]  # возвращ. список, где каждый элем. это строка с ключ-значен.из fields


def data_save_db(csv_data):
    BRICK, MONOLITE, PANEL = range(1, 4)

    MATERIALS_NAMES = {
        BRICK: 'Кирпич',
        MONOLITE: 'Монолит',
        PANEL: 'Панель',
    }
    for row in csv_data:
        try:
            flat = Flat(
                num_rooms = int(row['num_rooms']),
                floor = int(row['floor']),
                link = row['link'],
                area = (row['area']), 
                #material = MATERIALS_NAMES[row['material']],
                metro = row['metro'],
                district = row['district'],
                street = row['street'],
                price = int(row['price']),
                commission = int(row['commission']),
                deposit = int(row['deposit'])
            )
            db.session.add(flat)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)

def main(file):
    app = create_app()
    with app.app_context():
        data_save_db(read_csv(file))

if __name__=='__main__':
    main('C:\\project\\rent_project\\webapp\\flat_data\\data_cian.csv')