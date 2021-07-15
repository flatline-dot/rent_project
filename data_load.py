import csv

from webapp.model import db, Payment, Location, Flat
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
        return data[1:]


def studio_check(num_rooms):
    if int(num_rooms) == 0:
        return True
    else:
        return False


def data_save_db(csv_data):
    map_materials = {
        'Кирпич': 1,
        'Монолит': 2,
        'Панель': 3,
    }
    for row in csv_data:
        try:
            payment = Payment(
                price=int(row['price']),
                commission=int(row['commission']),
                deposit=int(row['deposit']),
            )
            db.session.add(payment)
            db.session.flush()
            location = Location(
                metro=row['metro'],
                district=row['district'],
                street=row['street'],
            )
            db.session.add(location)
            db.session.flush()
            flat = Flat(
                num_rooms=int(row['num_rooms']),
                is_studio=studio_check(row['num_rooms']),
                floor=int(row['floor']),
                material=map_materials[row['material']],
                area=int(float(row['area'])),
                link=row['link'],
                payment_id=payment.id,
                location_id=location.id,
            )
            db.session.add(flat)
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
            raise Exception


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        data_save_db(read_csv('domofond_data.csv'))
