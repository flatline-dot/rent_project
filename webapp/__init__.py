from flask import Flask, render_template
from webapp.model import db, Flat
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/index')
    def index():
        flats = Flat.query.all()
        num_offer = len(flats)
        return render_template('index.html', flats=flats, num_offer=num_offer)
