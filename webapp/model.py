from flask_sqlalchemy import SQLAlchemy

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
