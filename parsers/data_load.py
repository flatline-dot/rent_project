import csv
import sys
import os


basedir = os.path.abspath(os.path.dirname(__file__))
direct = os.path.join(basedir, '..')
sys.path.append(direct)


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
    for row in csv_data:
        try:
            flat = Flat(
                num_rooms=int(row['num_rooms']),
                floor=int(row['floor']),
                link=row['link'],
                area=int(row['area']),
                material=row['material'],
                metro=row['metro'],
                district=row['district'],
                street=row['street'],
                price=int(row['price']),
                commission=int(row['commission']),
                deposit=int(row['deposit'])
            )
            db.session.add(flat)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)


def main():
    app = create_app()
    with app.app_context():
        data_save_db(read_csv(os.path.join(basedir, 'data', 'domofond.csv')))
        data_save_db(read_csv(os.path.join(basedir, 'data', 'avito.csv')))


if __name__ == '__main__':
    main()
