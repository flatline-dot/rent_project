from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Flat(db.Model):

    BRICK, MONOLITE, PANEL = range(1, 4)

    MATERIALS_NAMES = {
        BRICK: 'Кирпич',
        MONOLITE: 'Монолит',
        PANEL: 'Панель',
    }

    id = db.Column(db.Integer, primary_key=True)
    num_rooms = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    link = db.Column(db.String, unique=True)
    area = db.Column(db.Integer)
    material = db.Column(db.Integer)
    metro = db.Column(db.String)
    district = db.Column(db.String)
    street = db.Column(db.String)
    price = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    deposit = db.Column(db.Integer)

    def __repr__(self):
        return f'<Flat id={self.id}, link={self.link}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __repr__(self):
        return f'User {self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
