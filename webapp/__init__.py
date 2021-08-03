from flask import Flask, render_template
from webapp.model import db
from webapp.flat.read_json import get_metro
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/search')
    def search():
        list_metro = get_metro()
        num_rooms = [0, 1, 2, 3, 4, 5, 6, 7]
        return render_template('search.html', num_rooms=num_rooms, list_metro=list_metro)

    @app.route('/result', methods=['POST'])
    def result():
        return render_template('no_result.html')
    return app
