from flask_sqlalchemy import SQLAlchemy, orm

db = SQLAlchemy()


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metro = db.Column(db.String)
    district = db.Column(db.String)
    street = db.Column(db.String)
    flat = orm.relationship('Flat')

    def __repr__(self):
        return f'''metro = {self.metro},
                   district = {self.district},
                   street = {self.street}>'''


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    deposit = db.Column(db.Integer)
    flat = orm.relationship('Flat')

    def __repr__(self):
        return f'''price = {self.price},
                   commision = {self.commission},
                   deposit = {self.deposit}>'''


class Flat(db.Model):

    BRICK, MONOLITE, PANEL = range(1, 4)

    MATERIALS_NAMES = {
        BRICK: 'Кирпич',
        MONOLITE: 'Монолит',
        PANEL: 'Панель',
    }

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey(Payment.id), nullable=False)
    num_rooms = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    is_studio = db.Column(db.Boolean, default=False, nullable=False)
    link = db.Column(db.String, unique=True)
    area = db.Column(db.Integer)
    material = db.Column(db.Integer)
    payment = orm.relationship('Payment', lazy='joined')
    location = orm.relationship('Location', lazy='joined')

    def __repr__(self):
        return f'<Flat id={self.id}, link={self.link}>'
