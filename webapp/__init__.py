from flask import Flask
from webapp.model import db
from flask_migrate import Migrate
from webapp.ads.veiws import blueprint as ads_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.register_blueprint(ads_blueprint)
    migrate = Migrate(app, db)

    return app
