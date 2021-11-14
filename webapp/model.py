from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Flat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    num_rooms = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    link = db.Column(db.String, unique=True)
    area = db.Column(db.Integer)
    material = db.Column(db.String)
    metro = db.Column(db.String)
    district = db.Column(db.String)
    street = db.Column(db.String)
    price = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    deposit = db.Column(db.Integer)
    user = relationship('User')

    def __repr__(self):
        return f'<Flat id={self.id}, link={self.link}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    role = db.Column(db.String)
    flat = relationship('Flat')

    def __repr__(self):
        return f'User {self.username}'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
