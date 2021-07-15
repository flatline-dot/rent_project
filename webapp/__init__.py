from flask import Flask, render_template, request
from webapp.model import db, Flat, Payment, Location
from webapp.flat.read_json import get_metro


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/search')
    def search():
        list_metro = get_metro()
        num_rooms = [0, 1, 2, 3, 4, 5, 6, 7]
        return render_template('search.html', num_rooms=num_rooms, list_metro=list_metro)

    @app.route('/result', methods=['POST'])
    def result():
        rooms = [0, 1, 2, 3, 4, 5, 6, 7]
        price_from = 0
        price_to = 500000
        commission = 100
        deposit = 500000
        result = request.form

        user_rooms = []

        for key in result:
            if key.isdigit():
                user_rooms.append(int(result[key]))

        if user_rooms:
            rooms = user_rooms

        if result['от'] != "":
            price_from = int(result['от'])

        if result['до'] != "":
            price_to = int(result['до'])

        if 'commission' in result:
            commission = 0

        if 'no_deposit' in result:
            deposit = 0

        if result['metro'] == 'Метро':
            metro = get_metro()
        else:
            metro = [result['metro']]

        query = Flat.query.join(Flat.payment,
                                Flat.location).order_by(Payment.price).filter(Flat.num_rooms.in_(rooms),
                                                                              price_from <= Payment.price,
                                                                              Payment.price <= price_to,
                                                                              Payment.commission <= commission,
                                                                              Payment.deposit <= deposit,
                                                                              Location.metro.in_(metro)).all()

        if query:
            return render_template('result.html', flats=query, num_offer=len(query))
        else:
            return render_template('no_result.html')
    return app
