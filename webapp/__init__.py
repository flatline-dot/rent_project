from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from webapp.model import db, User
from webapp.ads.veiws import blueprint as ads_blueprint
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.register_blueprint(ads_blueprint)
    app.register_blueprint(user_blueprint)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def user_load(user_id):
        return User.query.get(user_id)
    return app
