from operator import and_
from flask import Flask, render_template, request
from webapp.model import db, Flat
from flask_migrate import Migrate
from sqlalchemy import and_

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/index')
    def index():
        flats = Flat.query.all()
        num_offer = len(flats)
        #return render_template('index.html', flats=flats, num_offer=num_offer)
        return render_template('ex.html', flats=flats)
    
    @app.route('/rep', methods=["POST", "GET"])
    def rep():
        num_rooms = [0, 1, 2, 3, 4, 5]
        material = ['Кирпичный', 'Панельный', 'Монолитный', 'Блочный', 'Деревянный']
        if request.method == 'POST':
            if request.form.getlist('num_rooms'):
                num_rooms = [int(i) for i in request.form.getlist('num_rooms')]
                print(num_rooms)
            if request.form.get('from'):
                price_from = request.form.get('from')
            else:
                price_from = 0
            
            if request.form.get('to'):
                price_to = request.form.get('to')
            else:
                price_to = 1000000

            if request.form.get('commission'):
                commission = 0
            else:
                commission = 100
            
            if request.form.get('deposit'):
                deposit = 0
            else:
                deposit = 1000000
            
            if request.form.getlist('material'):
                material = request.form.getlist('material')
            
            if request.form.get('min'):
                area_min = request.form.get('min')
            else:
                area_min = 0
            
            if request.form.get('max'):
                area_max = request.form.get('max')
            else:
                area_max = 1000
            query = Flat.query.filter(Flat.num_rooms.in_(num_rooms),
                                      and_(Flat.price <= price_to, price_from <= Flat.price),
                                      Flat.commission <= commission,
                                      Flat.deposit <= deposit,
                                      and_(Flat.area <= area_max, Flat.area >= area_min)).all()
            return render_template('ex.html', flats=query)
        query = Flat.query.all()
        print(request.method)
        return render_template('ex.html', flats=query)
    return app
